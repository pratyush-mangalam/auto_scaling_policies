import boto3
import setting
from config import AutoScalingGroupConfiguration

try:
    BOTO_SESSION = boto3.Session(**setting.AWS_ACCESS_CREDENTIAL)
except ConnectionError as e:
    print("unable to connect to boto session, error: {}".format(e))


class AWSSQSAutoScalingConnection:
    autoscaling = None
    response = None

    @staticmethod
    def _get_aws_service_connection(service_id):
        return BOTO_SESSION.client(service_id)

    def get_queue_url(self, queue_name, account_id):
        client = self._get_aws_service_connection('sqs')
        return client.get_queue_url(
            QueueName=queue_name,
            QueueOwnerAWSAccountId=account_id
        )

    def set_desired_capacity_based_on_queue_message(self, auto_scaling_group_name, desired_capacity):
        client = self._get_aws_service_connection('autoscaling')
        client.set_desired_capacity(
            AutoScalingGroupName=auto_scaling_group_name,
            DesiredCapacity=desired_capacity,
            HonorCooldown=setting.HONORCOOLDOWN,
        )

    def get_number_of_messages_in_queue(self, queue_name):
        client = self._get_aws_service_connection('sqs')
        response = client.get_queue_attributes(
            QueueUrl=self.get_queue_url(queue_name=queue_name, account_id=setting.ACCOUNT_ID).get(
                "QueueUrl"),
            AttributeNames=["ApproximateNumberOfMessages"])
        return int(response.get("Attributes").get("ApproximateNumberOfMessages"))


class AutoScaleUpDown(AWSSQSAutoScalingConnection):
    def __init__(self):
        super(AutoScaleUpDown, self).__init__()

    def set_desire_capacity_of_autoscale_group(self):
        transformation_info_dict = {}
        for auto_scaling_group_detail_dict in AutoScalingGroupConfiguration:
            queue_message_size = 0
            for queue in auto_scaling_group_detail_dict.get("autoscaling_group_queue_name"):
                queue_message_size += self.get_number_of_messages_in_queue(queue)
            transformation_info_dict["queue_message_size"] = queue_message_size
            transformation_info_dict["number_of_queues"] = len(
                auto_scaling_group_detail_dict.get("autoscaling_group_queue_name"))
            transformation_method = auto_scaling_group_detail_dict.get("transformation_policy")
            message_size_for_scaling = transformation_method(transformation_info_dict)
            auto_scaling_group_name = auto_scaling_group_detail_dict.get("autoscaling_group_name")
            for min_max_dict in auto_scaling_group_detail_dict.get("scaling_policy"):
                if min_max_dict.get("lower_scale") <= message_size_for_scaling <= min_max_dict.get("higher_scale"):
                    self.set_desired_capacity_based_on_queue_message(auto_scaling_group_name,
                                                                     min_max_dict.get("desired_capacity"))
                    break

    def set_desire_capacity_to_minimum(self):
        for auto_scaling_group_detail_dict in AutoScalingGroupConfiguration:
            self.set_desired_capacity_based_on_queue_message(
                auto_scaling_group_detail_dict.get("autoscaling_group_name"),
                auto_scaling_group_detail_dict.get("minimum_number_of_desired_capacity"))
