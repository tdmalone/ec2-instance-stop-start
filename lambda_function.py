"""
A simple AWS Lambda function that helps manage start and stop schedules to save costs on EC2
instances.

Initially based on this:
https://aws.amazon.com/premiumsupport/knowledge-center/start-stop-lambda-cloudwatch/
"""

import boto3, json, os

def lambda_handler( event, context ):

  # If IP addresses have been provided in the event, check if the source IP is a-ok.
  if 'authorised-ips' in event:
    if 'source-ip' in event and not event['source-ip'] in event['authorised-ips']:
      raise Exception( 'Unauthorised.' )

  # If IP addresses have been provided in an environment variable, check if the source IP is a-ok.
  # TODO

  ec2 = boto3.client( 'ec2', region_name = event['region'] )

  # Start or stop the requested instance(s).
  if 'start' == event['action']:
    ec2.start_instances( InstanceIds = event['instances'] )
  elif 'stop' == event['action']:
    ec2.stop_instances( InstanceIds = event['instances'] )

  print( event['action'] )
  print( 'instances: ' + ', '.join( event['instances'] ) )

  return {
    'action':    event['action'],
    'instances': event['instances']
  }
