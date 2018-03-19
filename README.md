# EC2 Instance Stop Start

A simple [AWS Lambda](https://aws.amazon.com/lambda/) function that starts and stops EC2 instances to help save on costs. You can schedule starts and stops via [CloudWatch Events](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html), set up an [API Gateway](https://aws.amazon.com/api-gateway/) endpoint to call at will... or invoke the function using any other [supported method](https://docs.aws.amazon.com/lambda/latest/dg/invoking-lambda-function.html) (or directly via the [Lambda API](https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html)) providing it's possible to configure a custom payload.

The function itself is written in Python 3 and was based initially on [this AWS example](https://aws.amazon.com/premiumsupport/knowledge-center/start-stop-lambda-cloudwatch/).

## Setup

1. Create a new Python 3.6 Lambda function (eg. in the [AWS Lambda console](https://console.aws.amazon.com/lambda/home?#/create)). It will need access to `startInstances` and/or `stopInstances` for the EC2 instance(s) you wish to modify, so you will also need to [create a suitable IAM role](https://console.aws.amazon.com/iam/home?#/roles$new?step=type) if you don't have one already.
1. Either fork this repository and modify [.travis.yml](.travis.yml) to deploy to your new function (function name, role name, AWS access details, etc.) ___OR___ open [lambda_function.py](lambda_function.py) and copy the code directly into your new Lambda function.

### Invoking on a Schedule

1. Visit the CloudWatch console and [add a new rule](https://console.aws.amazon.com/cloudwatch/home?#rules:action=create).
1. Select the _Schedule_ option, and create the schedule for when you would like to start or stop your instance(s) - you'll probably want to use the _Cron expression_ option (note that unlike many cron implementations, AWS requires a question mark (?) for either the day-of-month or day-of-week fields - see [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#CronExpressions) for full documentation).
1. Click _Add target_, and select your Lambda function (and version or alias, if applicable).
1. Expand _Configure input_ and select the _Constant (JSON text)_ option. Enter the following text, using either 'start' or 'stop' for the action, and of course specifying the region and the instance IDs you wish to operate on:

       { "action": "start", "region": "ap-southeast-2", "instances": [ "i-0155bb8e6d7dddf46", "i-0155bb8e6d7dddf46" ] }

1. Finally, click _Configure details_, fill out the requested information, and click _Create rule_! Your instance(s) should now be started or stopped along with the schedule you created.

Repeat these instructions to create additional schedules for other instances, regions, or start/stop actions.

### Invoking via API Gateway

1. Visit the [API Gateway console](https://console.aws.amazon.com/apigateway/home) and either create a new API, or select an existing one you want to use.
1. Think about how you want to structure your resources. For example, if you only have one EC2 instance to manage, you might set up a structure such as `/server/start` and `/server/stop`.
1. Under _Resources_, click _Actions -> Create Resource_, and enter a name and path. Following the above example, you'll enter 'server' at this point. Click _Create Resource_. If you need another path level, create a new resource to add that - for example, 'start'.
1. With your new resource selected, click _Actions -> Create Method_. Select the method you wish to use (although it's not technically correct, use `GET` if you want to easily call it via your browser's address bar), and click the tick.
1. Find your Lambda function (leave 'Use Lambda Proxy integration' **deselected**), and click _Save_.
1. Now under your method settings, click _Integration Request_, then scrolling down to and expand _Body Mapping Templates_.
1. Click _Add mapping template_, enter 'application/json', and click the check mark.
1. Scroll down, and for _Generate template_, select _Empty_. Replace the empty curly braces with the following, using either 'start' or 'stop' for the action, and of course changing the region and instance IDs you wish to operate on, and the IP addresses authorised to access the endpoint (leave the `authorised-ips` key out entirely if you don't want to restrict access):

       {
          "action": "start",
          "region": "ap-southeast-2",
          "instances": [
            "i-0155bb8e6d7dddf46",
            "i-0155bb8e6d7dddf46"
          ],
          "source-ip": "$context.identity.sourceIp"
        }

1. Save it, click _Stages_ over on the left, and _Create_ a stage (such as 'v1') if you don't already have one.
1. Deploy your API to your stage, then visit your endpoint! It should look something like https://12abc3defg.execute-api.ap-southeast-2.amazonaws.com/v1/server/start, depending on your API's invoke URL and the values you entered for your stage and resource(s). If everything is hooked up correctly, your server should start (or stop)!

Repeat these steps to create additional endpoints to service different actions, regions or instances. You could also set your API up to take and map dynamic input directly from the request (via the path, query string or request headers).

#### Securing your endpoint

Unless you want anyone who finds your API to be able to start and stop your servers, you'll want to think about securing it - such as with [API keys](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-usage-plans-with-console.html) or [IAM policies](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html).

There's also a built-in way to this function to restrict access by IP address. You shouldn't rely on this as your only defence, but it's worthwhile doing if you can.

The mapping template we set up earlier already configures API Gateway to send through the source IP address, so now you just need to add your authorised IP(s). You can do this by adding the `AUTHORISED_IPS` environment variable to your Lambda function, setting it to a comma delimited list of IPs such as eg. `123.45.67.89,98.76.54.32`.

Alternatively, add an `authorised-ips` key directly to the mapping template we added above:

    "authorised-ips": [
      "123.45.67.89",
      "98.76.54.32"
    ]

Which of these methods you choose depends on whether you want to configure the IPs once for each invocation of your function... or once for every endpoint that you set up.

## Development

Clone (or fork and clone) the repository to your machine.

If you have Docker running, you can test the function locally by running `make test`, although you may want to replace the instance ID in the [Makefile](Makefile) with an instance you control 🙂. You'll also need to have `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` exported as environment variables to pass into the Docker container.

Note that unit tests are not yet written.

## License

[MIT](LICENSE).
