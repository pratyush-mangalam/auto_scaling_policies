import math
from transformation import get_summation_of_messages, get_average_of_messages

AutoScalingGroupConfiguration = [
    {
        "autoscaling_group_name": "",
        "autoscaling_group_queue_name": [""],
        "transformation_policy": get_summation_of_messages,
        "minimum_number_of_desired_capacity": 1,
        "scaling_policy":
            [
                {
                    "lower_scale": 0,
                    "higher_scale": 25000,
                    "desired_capacity": 1
                },
                {
                    "lower_scale": 25000,
                    "higher_scale": 100000,
                    "desired_capacity": 2
                },
                {
                    "lower_scale": 100000,
                    "higher_scale": 500000,
                    "desired_capacity": 4
                },
                {
                    "lower_scale": 500000,
                    "higher_scale": 1000000,
                    "desired_capacity": 6
                },
                {
                    "lower_scale": 1000000,
                    "higher_scale": math.inf,
                    "desired_capacity": 8
                }

            ]
    }
]
