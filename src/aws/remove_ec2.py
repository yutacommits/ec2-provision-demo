"""
Terminate ALL ec2 instances that do not have the status ``terminated``
"""
from botocore.exceptions import ClientError
import boto3

from utils import logger

ec2 = boto3.resource("ec2")

non_terminated_filter = [
    {
        "Name": "instance-state-name",
        "Values": ["pending", "running", "shutting-down", "stopping", "stopped"],
    }
]

# when running `instances.all()`, terminated state also shows
# so make sure to filter these out before running `terminate()` again
for instance in ec2.instances.filter(Filters=non_terminated_filter):
    logger.info(f"Instance id: {instance.instance_id}")
    logger.info(f"Instance type: {instance.instance_type}")
    logger.info(f"Instance ipv4: {instance.public_ip_address}")
    logger.info("Terminating instance,...")
    instance.terminate()
    logger.info("Waiting until terminated...")
    instance.wait_until_terminated()
    logger.info("Done.")

# sanity check
logger.info("Checking for instances that haven't terminated.")
for instance in ec2.instances.filter(Filters=non_terminated_filter):
    logger.info(f"Instance id is {instance.instance_id}")
    logger.info(f"Instance type is {instance.instance_type}")
else:
    logger.info("No instances found.")
