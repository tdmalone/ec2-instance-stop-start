"""
A simple AWS Lambda function that helps manage start and stop schedules to save costs on EC2
instances.

Initially based on this:
https://aws.amazon.com/premiumsupport/knowledge-center/start-stop-lambda-cloudwatch/
"""

import boto3, os

def lambda_handler( event, context ):
  """Handler function called directly by Lambda."""

  # Disable pylint check for unused args, as Lambda will always try to pass through `context`.
  #pylint: disable=unused-argument

  # If IP addresses have been provided in the event, check if the source IP is a-ok.
  if 'authorised-ips' in event:
    if 'source-ip' in event and not event['source-ip'] in event['authorised-ips']:
      raise Exception( 'Unauthorised.' )

  # If IP addresses have been provided in an environment variable, check if the source IP is a-ok.
  if 'AUTHORISED_IPS' in os.environ:
    authorised_ips = os.environ['AUTHORISED_IPS'].split( ',' )
    if 'source-ip' in event and not event['source-ip'] in authorised_ips:
      raise Exception( 'Unauthorised.' )

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
