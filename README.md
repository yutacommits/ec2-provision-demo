# Overview

A dockerized setup that provisions an ec2 instance with `boto3` and configures it
using `ansible` to run a TLS enabled `NGINX` server

## Requirements

* `aws` access key and secret key
* `aws` ec2 security group with the tag `boto3` (no value)
* `docker`
* `make`

The `Dockerfile` assumes a x64 system is used, but if using an ARM system
such as the Raspberry Pi, the `curl` command will have to be altered

from `https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip`

to `https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip`

## Setup

Copy `.env.example` to `.env` and fill in the aws configuration variables

    cp .env.example .env

Build the image and start the container

    make build

## Usage

Instructions are assumed to be ran inside the `boto3-py-demo` container

Enter the container

    docker exec -it boto3-py-demo bash

Create a keypair named `test-key-pair`

The private key will be output at `/tmp/test-key-pair.pem`

    python aws/create_keypair.py

Create an ec2 instance, the public ip will be logged to the console
and at `/tmp/debug.log`

    python aws/create_ec2.py

The public ip address can also be found with:

```sh
aws ec2 describe-instances \
    --query 'Reservations[*].Instances[*].PublicIpAddress' \
    --output text
```

Optional: SSH with the private key

    ssh -i /tmp/test-key-pair.pem ubuntu@<public ip>

Copy `ec2.ini.example` to `ec2.ini` and fill in the `ansible_host`

    cp ansible/inventory/ec2.ini.example ansible/inventory/ec2.ini

Create a private key and cert for `NGINX`

```sh
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -subj /CN=localhost \
    -keyout ansible/playbooks/files/nginx.key \
    -out ansible/playbooks/files/nginx.crt
```

Change directories to `ansible` and run the ansible playbook

    cd ansible
    ansible-playbook playbooks/webservers-tls.yml

Finally, terminate ALL ec2 instances created

    python aws/remove_ec2.py

