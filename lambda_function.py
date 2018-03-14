"""
A simple AWS Lambda function that helps manage start and stop schedules to save costs on EC2
instances.

Initially based on this:
https://aws.amazon.com/premiumsupport/knowledge-center/start-stop-lambda-cloudwatch/
"""

import boto3

region = 'ap-southeast-2'
action = 'stop' # 'start' or 'stop'
instances = [ 'i-0155bb8e6d7dddf46', 'i-03ae34997d9442d74' ]

def lambda_handler( event, context ):

  ec2 = boto3.client( 'ec2', region_name = region )

  if 'start' == action:
    ec2.start_instances( InstanceIds = instances )
  elif 'stop' == action:
    ec2.stop_instances( InstanceIds = instances )

  print( ( 'Started' if 'start' == action else 'Stopped' ) + ' instances: ' + ', '.join( instances ) )

  return {
    "action":    action,
    "instances": instances
  }
