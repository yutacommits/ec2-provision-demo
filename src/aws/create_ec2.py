"""
Create a t2.micro instance with a Ubuntu 24 AMI ``ami-020cba7c55df1f615``

A predefined security group must be defined with the tag ``boto3`` with
an empty value

The response is saved at ``/tmp/ec2_response.json``, responses will be
overwritten
"""
import datetime
import json
import logging

from botocore.exceptions import ClientError
import boto3

from utils import logger

keypair_name = "test-key-pair"
client = boto3.client("ec2")


def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def get_public_ip(instance_id):
    reservations = client.describe_instances(InstanceIds=[instance_id]).get(
        "Reservations"
    )

    for reservation in reservations:
        for instance in reservation["Instances"]:
            logger.info(instance.get("PublicIpAddress"))


ubuntu_24_ami = "ami-020cba7c55df1f615"
logger.info(f"Ubuntu 24 AMI: {ubuntu_24_ami}")
ec2_response_outfile = "/tmp/ec2_response.json"

sgs = client.describe_security_groups(Filters=[{"Name": "tag:boto3", "Values": [""]}])
sgs_filtered = sgs["SecurityGroups"]
if len(sgs_filtered) != 1:
    logger.info("Failed to find exactly one security group with the tag 'boto3'")
    exit(1)
sg_id = sgs_filtered[0]["GroupId"]

response = client.describe_key_pairs()
keypairs = response["KeyPairs"]
logger.info(f"Found {len(keypairs)} keypairs")

for keypair in keypairs:
    kp = keypair["KeyName"]
    logger.info(f"Processing keypair: {kp}")
    if kp == keypair_name:
        logger.info(f"Found {keypair_name}")
        break
else:
    logger.info(f"{keypair_name} not found. Exiting.")
    exit(1)

config = {
    "ImageId": ubuntu_24_ami,
    "MinCount": 1,
    "MaxCount": 1,
    "InstanceType": "t2.micro",
    "KeyName": keypair_name,
    "SecurityGroupIds": [sg_id],
}
logger.info(f"Attempting to create instance,..\n{config}")
run_response = client.run_instances(**config)

with open(ec2_response_outfile, "w") as f:
    f.write(json.dumps(run_response, default=serialize_datetime, indent=2))
    logger.info(f"Wrote ec2 response at {ec2_response_outfile}")
logger.info("Waiting for instance to run.")
waiter = client.get_waiter("instance_running")

instance_id = run_response["Instances"][0]["InstanceId"]
waiter.wait(InstanceIds=[instance_id])
logger.info("Instance is now running.")

ip_addr = client.describe_instances(InstanceIds=[instance_id])["Reservations"][0][
    "Instances"
][0]["PublicIpAddress"]
logger.info(f"ip addr: {ip_addr}")
