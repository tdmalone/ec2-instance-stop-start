from distutils.core import setup

setup(
  name = 'ec2-instance-stop-start',
  packages = ['ec2-instance-stop-start'],
  version = '0.0.0',
  description = 'An AWS Lambda function that helps manage start and stop schedules to save costs on EC2 instances.',
  author = 'Tim Malone',
  author_email = 'tdmalone@gmail.com',
  url = 'https://github.com/tdmalone/ec2-instance-stop-start',
  download_url = 'https://github.com/tdmalone/ec2-instance-stop-start/archive/v0.0.0.tar.gz',
  keywords = ['aws', 'lambda', 'ec2' ],
  classifiers = [],
)
