"""
A simple AWS Lambda function that helps manage start and stop schedules to save costs on EC2
instances.

Initially based on this:
https://aws.amazon.com/premiumsupport/knowledge-center/start-stop-lambda-cloudwatch/
"""

import boto3, json

def lambda_handler( event, context ):

  ec2 = boto3.client( 'ec2', region_name = event["region"] )

  if 'start' == event["action"]:
    ec2.start_instances( InstanceIds = event["instances"] )
  elif 'stop' == event["action"]:
    ec2.stop_instances( InstanceIds = event["instances"] )

  print( event["action"] )
  print( 'instances: ' + ', '.join( event["instances"] ) )

  return {
    "action":    event["action"],
    "instances": event["instances"]
  }
