import boto3
import json

def create_iam_policy():
    # Create IAM client
    iam = boto3.client('iam')

    # Create a policy



    my_managed_policy = {
    "Version": "2012-10-17",
    "Statement": [
    {
    "Sid": "AmazonFullAccess",
    "Effect": "Allow",
    "Action": [
    "rds:AmazonEC2FullAccess"
    ],
    "Resource": "*"
    }
    ]
    }

    response = iam.create_policy(
        PolicyName='ec2access',
        PolicyDocument=json.dumps(my_managed_policy)
        )
    print(response)
