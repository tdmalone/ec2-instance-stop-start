
lint:
	pylint lambda_function.py

test:
	pytest
	docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --rm -v "${PWD}":/var/task lambci/lambda:python3.6 lambda_function.lambda_handler '{ "action": "stop", "region": "ap-southeast-2", "instances": [ "i-0155bb8e6d7dddf46" ] }'
