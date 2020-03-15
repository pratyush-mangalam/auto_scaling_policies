import argparse
from autoscalingclasses import AutoScaleUpDown

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--scaleupdown", help="Please give argument as 'SCALEUP' or 'SCALEDOWN'")
args = parser.parse_args()

if args.scaleupdown == "SCALEUP":
    auto_scaling_up_class_object = AutoScaleUpDown()
    auto_scaling_up_class_object.set_desire_capacity_of_autoscale_group()
elif args.scaleupdown == "SCALEDOWN":
    auto_scaling_down_class_object = AutoScaleUpDown()
    auto_scaling_down_class_object.set_desire_capacity_to_minimum()
else:
    print("Invalid argument: either SCALEUP OR SCALEDOWN applicable")
