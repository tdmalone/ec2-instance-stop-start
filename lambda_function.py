"""
A simple AWS Lambda function that helps manage start and stop schedules to save costs on EC2
instances.

Initially based on this:
https://aws.amazon.com/premiumsupport/knowledge-center/start-stop-lambda-cloudwatch/
"""

import boto3

region = 'ap-southeast-2'
instances = ['i-0155bb8e6d7dddf46']

def lambda_handler(event, context):

  ec2 = boto3.client('ec2', region_name=region)
  ec2.stop_instances(InstanceIds=instances)

  print('Stopped instances: ' + ''.join(instances))

  return {
    "event": "stop",
    "instances": instances
  }
