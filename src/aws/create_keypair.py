"""
Create a key pair ``test-key-pair`` and store the private key
at ``/tmp/test-key-pair.pem``

If the keypair ``test-key-pair`` exists, delete the keypair
"""
import datetime
import json
import os
import logging

import boto3

from utils import logger


def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


ec2_client = boto3.client("ec2")
keypair_name = "test-key-pair"
filename = f"/tmp/{keypair_name}.pem"

response = ec2_client.describe_key_pairs()
json_response = json.dumps(response, default=serialize_datetime, indent=2)
logger.info(f"Describing key pairs: \n{json_response}")

# search for keypair, and remove if exists
for keypair in response["KeyPairs"]:
    kp = keypair["KeyName"]
    logger.info(f"Processing keypair: {kp}")
    if kp == keypair_name:
        logger.info(f"Found {keypair_name},... removing.")
        ec2_client.delete_key_pair(KeyName=kp)
        break

# create new key pair
logger.info(f"Attempting to create {keypair_name}.")
key_pair = ec2_client.create_key_pair(KeyName=keypair_name)

# write private key to file with 400 permissions
private_key = key_pair["KeyMaterial"]
with os.fdopen(os.open(filename, os.O_WRONLY | os.O_CREAT, 0o400), "w") as handle:
    logger.info(f"Writing {filename}")
    handle.write(private_key)
