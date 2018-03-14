# EC2 Instance Stop Start

A simple [AWS Lambda](https://aws.amazon.com/lambda/) function that helps manage start and stop schedules to save costs on EC2 instances.

Based initially on [this AWS example](https://aws.amazon.com/premiumsupport/knowledge-center/start-stop-lambda-cloudwatch/).

## Setup

1. Create a new Python 3.6 Lambda function (eg. in the [AWS Lambda console](https://console.aws.amazon.com/lambda/home?#/create)). It will need access to `startInstances` and/or `stopInstances` for the EC2 instance(s) you wish to modify, so you will also need to [create a suitable IAM role](https://console.aws.amazon.com/iam/home?#/roles$new?step=type) if you don't have one already.
2. Either fork this repository and modify [.travis.yml](.travis.yml) to deploy to your new function (function name, role name, AWS access details, etc.) ___OR___ open [lambda_function.py](lambda_function.py) and copy the code into your new Lambda function.
3. Visit the CloudWatch console and [add a new rule](https://console.aws.amazon.com/cloudwatch/home?#rules:action=create).
4. Select the _Schedule_ option, and create the schedule for when you would like to start or stop your instance(s) - you'll probably want to use the _Cron expression_ option (note that unlike many cron implementations, AWS requires a question mark (?) for either the day-of-month or day-of-week fields - see [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#CronExpressions) for full documentation).
5. Click _Add target_ over on the right, and select your Lambda function (and version or alias, if applicable - I usually set up at least a _dev_ and _prod_ alias, with deployment handled in [.travis.yml](.travis.yml), but if you've copied and pasted the function you probably don't need to worry about maintaining separate versions!).
6. Expand _Configure input_ and select the _Constant (JSON text)_ option. Enter the following text, using either 'start' or 'stop' for the action, and of course specifying the region and the instance IDs you wish to operate on:

    { "action": "start", "region": "ap-southeast-2", instances": [ "i-0155bb8e6d7dddf46", "i-0155bb8e6d7dddf46" ] }

7. Finally, click _Configure details_, fill out the requested information, and click _Create rule_! Repeat from step 3 above to create additional schedules for other instances, regions, or start/stop actions.

## Development

Clone (or fork and clone) the repository to your machine.

If you have Docker running, you can test the function locally by running `make test`.

## License

[MIT](LICENSE).
