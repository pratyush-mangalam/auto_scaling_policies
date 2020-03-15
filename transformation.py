from autoscalingclasses import AWSSQSAutoScalingConnection

aws_sqs_auto_scaling_connection = AWSSQSAutoScalingConnection()


def get_summation_of_messages(**kwargs):
    return kwargs.get("queue_message_size")


def get_average_of_messages(**kwargs):
    return kwargs.get("queue_message_size") / kwargs.get("number_of_queues")