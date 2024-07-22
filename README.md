# AWS-Cognito
An sign-in, sign-up and verifying user through the AWS Cognito.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
IMPLEMENTATION


Step 1: Set Up the Serverless Framework
	Install the Serverless Framework:
	npm install -g serverless
	Create a New Serverless Service:
	Create a new project directory and initialize a Serverless service:


Step 2: Prepare Your Project Directory
	Install Boto3:
	Make sure Boto3 is available in your Lambda environment.
	pip install boto3
	Create handler.py:
	Create serverless.yml:
	

Step 3: Implement the Lambda Functions
	Sign Up Function:
		This function handles user registration with AWS Cognito.
		It collects user details (email, password, phone number) from the request.
		Uses the Cognito sign_up API to create a new user.
		Automatically confirms the user using the admin_confirm_sign_up API.
		
	Sign In Function:
		This function handles user authentication.
		It collects user credentials (email, password) from the request.
		Uses the Cognito initiate_auth API to authenticate the user and retrieve tokens.

	Verify User Function:
		This function handles user verification via OTP (email or SMS).
		It collects the confirmation code from the user.
		Uses the Cognito confirm_sign_up API to verify the user.


Step 4: Update serverless.yml
	Your serverless.yml should define the functions and environment variables:


Step 5: Deploy the Service
	Deploy the service to AWS using the Serverless Framework:


Step 6: Test with Postman
	Get Your API Gateway Endpoint:
	After deploying, note the API Gateway endpoint provided by the Serverless Framework.


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Testing the API using POSTMAN:

Sign Up User:
	Method: POST
		URL: https://{your_api_gateway_id}.execute-api.{region}.amazonaws.com/dev/signup
		Headers:
		Content-Type: application/json
		Body (raw JSON):
		json
		Copy code
		{
		  "email": "testuser@example.com",
		  "password": "Test@123",
		  "phone_number": "+1234567890"
		}
		
Sign In User:
	Method: POST
		URL: https://{your_api_gateway_id}.execute-api.{region}.amazonaws.com/dev/signin
		Headers:
		Content-Type: application/json
		Body (raw JSON):
		json
		Copy code
		{
		  "email": "testuser@example.com",
		  "password": "Test@123"
		}
		
Verify User:
	Method: POST
		URL: https://{your_api_gateway_id}.execute-api.{region}.amazonaws.com/dev/verify
		Headers:
		Content-Type: application/json
		Body (raw JSON):
		json
		Copy code
		{
		  "email": "testuser@example.com",
		  "confirmation_code": "123456"
		}
		
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Step 7: Monitor and Debug

CloudWatch Logs:
	Check AWS CloudWatch logs for your Lambda functions to ensure they are executing correctly and to troubleshoot any issues.

Verify Email/SMS:
	Ensure that verification emails or SMS messages are being sent and received. Check your SES configuration if using email.


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


**************************************************************************HAPPY CODING****************************************************************************************



