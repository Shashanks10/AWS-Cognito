import os
import json
import boto3
from botocore.exceptions import ClientError

def signup(event, context):
    client = boto3.client('cognito-idp')
    body = json.loads(event['body'])
    
    try:
        # Sign up the user
        response = client.sign_up(
            ClientId=os.environ['CLIENT_ID'],
            Username=body['email'],
            Password=body['password'],
            UserAttributes=[
                {'Name': 'email', 'Value': body['email']},
                {'Name': 'phone_number', 'Value': body['phone_number']}
            ]
        )
        
        # Automatically confirm the user
        client.admin_confirm_sign_up(
            UserPoolId=os.environ['USER_POOL_ID'],
            Username=body['email']
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'User signed up and confirmed successfully.',
                'userSub': response['UserSub'],
                'userConfirmed': True
            })
        }
    except ClientError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }



def signin(event, context):
    client = boto3.client('cognito-idp')
    body = json.loads(event['body'])
    try:
        response = client.initiate_auth(
            ClientId=os.environ['CLIENT_ID'],
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': body['username'],
                'PASSWORD': body['password']
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'User signed in successfully',
                'accessToken': response['AuthenticationResult']['AccessToken'],
                'idToken': response['AuthenticationResult']['IdToken'],
                'refreshToken': response['AuthenticationResult']['RefreshToken']
            })
        }
    except ClientError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }


def verify(event, context):
    client = boto3.client('cognito-idp')
    body = json.loads(event['body'])
    
    try:
        if 'session' in body:
            response = client.respond_to_auth_challenge(
                ClientId=os.environ['CLIENT_ID'],
                ChallengeName='SMS_MFA',
                Session=body['session'],
                ChallengeResponses={
                    'SMS_MFA_CODE': body['code'],
                    'USERNAME': body['username']
                }
            )
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'MFA verification successful',
                    'accessToken': response['AuthenticationResult']['AccessToken'],
                    'idToken': response['AuthenticationResult']['IdToken'],
                    'refreshToken': response['AuthenticationResult']['RefreshToken']
                })
            }
        else:
            # This is a sign-up confirmation
            response = client.confirm_sign_up(
                ClientId=os.environ['CLIENT_ID'],
                Username=body['username'],
                ConfirmationCode=body['code']
            )
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'User verified successfully'
                })
            }
    except client.exceptions.NotAuthorizedException as e:
        if "User cannot be confirmed. Current status is CONFIRMED" in str(e):
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'User is confirmed',
                    'action': 'Proceed to sign in'
                })
            }
        else:
            raise
    except client.exceptions.CodeMismatchException:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Invalid verification code',
                'message': 'Please check your code and try again.'
            })
        }
    except client.exceptions.ExpiredCodeException:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Expired verification code',
                'message': 'Your verification code has expired. Please request a new one.'
            })
        }
    except ClientError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }