# AWS Cognito Authentication Service

A serverless authentication service built with AWS Lambda, API Gateway, and AWS Cognito. This project provides RESTful API endpoints for user sign-up, sign-in, and verification using AWS Cognito User Pool.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [AWS Cognito Setup](#aws-cognito-setup)
- [Project Setup](#project-setup)
- [Building and Deploying](#building-and-deploying)
- [API Endpoints](#api-endpoints)
- [Testing with Postman](#testing-with-postman)
- [Environment Variables](#environment-variables)
- [Monitoring and Debugging](#monitoring-and-debugging)
- [Troubleshooting](#troubleshooting)

## Features

- **User Sign Up**: Register new users with email, password, and phone number
- **User Sign In**: Authenticate users and receive JWT tokens (Access Token, ID Token, Refresh Token)
- **User Verification**: Verify users via OTP (email or SMS) or handle MFA challenges
- **Automatic User Confirmation**: Users are automatically confirmed upon sign-up (configurable)
- **Serverless Architecture**: Built with AWS Lambda and API Gateway for scalability

## Prerequisites

Before you begin, ensure you have the following installed and configured:

1. **Node.js and npm** (v14 or higher)
   - Download from [nodejs.org](https://nodejs.org/)
   - Verify installation: `node --version` and `npm --version`

2. **Python** (3.10 or higher)
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

3. **AWS Account** with appropriate permissions
   - Create an account at [aws.amazon.com](https://aws.amazon.com/)
   - Configure AWS CLI credentials (see below)

4. **AWS CLI** (optional but recommended)
   - Install: `pip install awscli` or download from [AWS CLI](https://aws.amazon.com/cli/)
   - Configure: `aws configure`
   - You'll need:
     - AWS Access Key ID
     - AWS Secret Access Key
     - Default region (e.g., `us-east-1`)
     - Default output format (e.g., `json`)

5. **Serverless Framework**
   - Install globally: `npm install -g serverless`
   - Verify installation: `serverless --version`

## AWS Cognito Setup

Follow these steps to set up AWS Cognito User Pool and App Client:

### Step 1: Create AWS Cognito User Pool

1. **Log in to AWS Console**
   - Navigate to [AWS Console](https://console.aws.amazon.com/)
   - Search for "Cognito" in the services search bar

2. **Create User Pool**
   - Click "Create user pool"
   - Choose "Cognito user pool" (not "Federated identity")

3. **Configure Sign-in Experience**
   - **Sign-in options**: Select at least:
     - ☑ Email
     - ☑ Username (optional, but recommended)
   - Click "Next"

4. **Configure Security Requirements**
   - **Password policy**: Choose your requirements (minimum 8 characters recommended)
     - Example: Minimum length 8, require uppercase, lowercase, numbers, and symbols
   - **Multi-factor authentication**: 
     - For development: Choose "No MFA"
     - For production: Choose "Optional MFA" or "Required MFA"
   - **User account recovery**: 
     - Select "Email only" or "Email and phone number"
   - Click "Next"

5. **Configure Sign-up Experience**
   - **Self-service sign-up**: Enable this option
   - **Cognito-assisted verification**: 
     - Choose "Send email verification code" or "Send email with verification link"
   - **Required attributes**: Select:
     - ☑ Email
     - ☑ Phone number (optional, but used in this project)
   - **Custom attributes**: Leave as default (or add custom ones if needed)
   - Click "Next"

6. **Configure Message Delivery**
   - **Email provider**: 
     - For development: Choose "Send email with Cognito"
     - For production: Configure Amazon SES (requires SES verification)
   - **Email from**: 
     - Choose "Cognito default email" or configure custom email
   - **SMS provider**: 
     - For development: Choose "Cognito default SMS" (limited to 50 SMS/day)
     - For production: Configure Amazon SNS
   - Click "Next"

7. **Integrate Your App**
   - **User pool name**: Enter a descriptive name (e.g., `my-auth-user-pool`)
   - **App client name**: Enter a name (e.g., `my-auth-app-client`)
   - **Client secret**: 
     - For this project: Choose "Don't generate a client secret" (we use USER_PASSWORD_AUTH flow)
   - Click "Next"

8. **Review and Create**
   - Review all settings
   - Click "Create user pool"

### Step 2: Configure App Client Settings

1. **Navigate to App Integration Tab**
   - In your User Pool, go to the "App integration" tab
   - Find your App client and click on it

2. **Configure Authentication Flow**
   - Under "Authentication flows configuration", enable:
     - ☑ ALLOW_USER_PASSWORD_AUTH (required for this project)
     - ☑ ALLOW_REFRESH_TOKEN_AUTH (recommended)
   - Click "Save changes"

3. **Configure Hosted UI (Optional)**
   - If you want to use Cognito Hosted UI, configure the callback URLs
   - For API-only usage, this is not required

### Step 3: Get Your Cognito Credentials

1. **Copy User Pool ID**
   - In the User Pool overview page, you'll see the "User pool ID"
   - Copy this value (format: `us-east-1_XXXXXXXXX`)

2. **Copy App Client ID**
   - Go to "App integration" tab
   - Under "App clients and analytics", find your app client
   - Copy the "Client ID" (format: alphanumeric string)

3. **Note Your Region**
   - Note the AWS region where you created the User Pool (e.g., `us-east-1`)

### Step 4: Configure IAM Permissions (Optional)

If you're using IAM roles with restricted permissions, ensure your Lambda execution role has:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cognito-idp:SignUp",
        "cognito-idp:InitiateAuth",
        "cognito-idp:ConfirmSignUp",
        "cognito-idp:RespondToAuthChallenge",
        "cognito-idp:AdminConfirmSignUp",
        "cognito-idp:DescribeUserPool",
        "cognito-idp:AdminInitiateAuth",
        "cognito-idp:AdminGetUser"
      ],
      "Resource": "arn:aws:cognito-idp:REGION:ACCOUNT_ID:userpool/USER_POOL_ID"
    }
  ]
}
```

## Project Setup

### Step 1: Clone or Navigate to Project Directory

```bash
cd AWS-Cognito
```

### Step 2: Install Python Dependencies

Create a virtual environment (recommended):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

This installs:
- `boto3` - AWS SDK for Python

### Step 3: Install Serverless Plugins

Install the Python requirements plugin for Serverless:

```bash
npm install --save-dev serverless-python-requirements
```

This plugin automatically packages your Python dependencies for Lambda deployment.

### Step 4: Configure Environment Variables

Set up your environment variables. You have two options:

**Option A: Using Environment Variables (Recommended for Local Development)**

```bash
# Windows PowerShell
$env:USER_POOL_ID="us-east-1_XXXXXXXXX"
$env:CLIENT_ID="your-client-id-here"

# Windows CMD
set USER_POOL_ID=us-east-1_XXXXXXXXX
set CLIENT_ID=your-client-id-here

# macOS/Linux
export USER_POOL_ID="us-east-1_XXXXXXXXX"
export CLIENT_ID="your-client-id-here"
```

**Option B: Using .env File (Alternative)**

1. Create a `.env` file in the project root:
```env
USER_POOL_ID=us-east-1_XXXXXXXXX
CLIENT_ID=your-client-id-here
```

2. Install serverless-dotenv-plugin:
```bash
npm install --save-dev serverless-dotenv-plugin
```

3. Add to `serverless.yml` under `plugins`:
```yaml
plugins:
  - serverless-python-requirements
  - serverless-dotenv-plugin
```

### Step 5: Update serverless.yml (If Needed)

Review `serverless.yml` and ensure:
- The region matches your Cognito User Pool region
- The IAM role statements include the correct User Pool ARN (or use wildcard `*`)

The User Pool ARN format is:
```
arn:aws:cognito-idp:REGION:ACCOUNT_ID:userpool/USER_POOL_ID
```

You can use a wildcard for the account ID:
```yaml
Resource: arn:aws:cognito-idp:${self:provider.region}:*:userpool/${self:provider.environment.USER_POOL_ID}
```

## Building and Deploying

### Step 1: Verify Configuration

Before deploying, verify your setup:

```bash
# Check Serverless version
serverless --version

# Verify AWS credentials (if using AWS CLI)
aws sts get-caller-identity

# Check environment variables are set
# Windows PowerShell
echo $env:USER_POOL_ID
echo $env:CLIENT_ID

# macOS/Linux
echo $USER_POOL_ID
echo $CLIENT_ID
```

### Step 2: Deploy to AWS

Deploy your service:

```bash
serverless deploy
```

Or deploy to a specific stage:

```bash
serverless deploy --stage dev
serverless deploy --stage prod
```

Or deploy to a specific region:

```bash
serverless deploy --region us-west-2
```

### Step 3: Verify Deployment

After deployment, you'll see output like:

```
Service Information
service: cognito-service
stage: dev
region: us-east-1
stack: cognito-service-dev
resources: 15
api keys:
  None
endpoints:
  POST - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/signup
  POST - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/signin
  POST - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/verify
functions:
  sign_up: cognito-service-dev-sign_up
  sign_in: cognito-service-dev-sign_in
  verify_user: cognito-service-dev-verify_user
```

**Save the API Gateway endpoints** - you'll need them for testing!

### Step 4: Test Deployment

You can test the deployment using the endpoints shown above. See the [Testing with Postman](#testing-with-postman) section below.

## API Endpoints

All endpoints accept JSON payloads and return JSON responses.

### 1. Sign Up

**Endpoint**: `POST /signup`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "phone_number": "+1234567890"
}
```

**Response (Success - 200)**:
```json
{
  "message": "User signed up and confirmed successfully.",
  "userSub": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "userConfirmed": true
}
```

**Response (Error - 400)**:
```json
{
  "error": "An account with the given email already exists."
}
```

### 2. Sign In

**Endpoint**: `POST /signin`

**Request Body**:
```json
{
  "username": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (Success - 200)**:
```json
{
  "message": "User signed in successfully",
  "accessToken": "eyJraWQiOiJ...",
  "idToken": "eyJraWQiOiJ...",
  "refreshToken": "eyJjdHkiOiJ..."
}
```

**Response (Error - 400)**:
```json
{
  "error": "Incorrect username or password."
}
```

### 3. Verify User

**Endpoint**: `POST /verify`

**For Sign-up Verification**:
```json
{
  "username": "user@example.com",
  "code": "123456"
}
```

**For MFA Challenge**:
```json
{
  "username": "user@example.com",
  "session": "session-token-from-signin",
  "code": "123456"
}
```

**Response (Success - 200)**:
```json
{
  "message": "User verified successfully"
}
```

## Testing with Postman

### Step 1: Set Up Postman Collection

1. Open Postman
2. Create a new Collection (e.g., "AWS Cognito API")
3. Set collection variables:
   - `base_url`: `https://your-api-id.execute-api.us-east-1.amazonaws.com/dev`
   - `email`: `testuser@example.com`
   - `password`: `Test@123`

### Step 2: Test Sign Up

1. **Create Request**: `POST {{base_url}}/signup`
2. **Headers**:
   - `Content-Type: application/json`
3. **Body** (raw JSON):
```json
{
  "email": "testuser@example.com",
  "password": "Test@123",
  "phone_number": "+1234567890"
}
```
4. **Send Request**
5. **Expected**: 200 status with user confirmation message

### Step 3: Test Sign In

1. **Create Request**: `POST {{base_url}}/signin`
2. **Headers**:
   - `Content-Type: application/json`
3. **Body** (raw JSON):
```json
{
  "username": "testuser@example.com",
  "password": "Test@123"
}
```
4. **Send Request**
5. **Expected**: 200 status with access token, ID token, and refresh token

### Step 4: Test Verify (If Verification Required)

1. **Check Email/SMS** for verification code
2. **Create Request**: `POST {{base_url}}/verify`
3. **Headers**:
   - `Content-Type: application/json`
4. **Body** (raw JSON):
```json
{
  "username": "testuser@example.com",
  "code": "123456"
}
```
5. **Send Request**
6. **Expected**: 200 status with verification success message

## Environment Variables

The following environment variables are required:

| Variable | Description | Example |
|----------|-------------|---------|
| `USER_POOL_ID` | AWS Cognito User Pool ID | `us-east-1_XXXXXXXXX` |
| `CLIENT_ID` | AWS Cognito App Client ID | `1a2b3c4d5e6f7g8h9i0j` |

These are automatically injected into Lambda functions via `serverless.yml`.

## Monitoring and Debugging

### CloudWatch Logs

View Lambda function logs:

1. **Via AWS Console**:
   - Navigate to CloudWatch → Log groups
   - Find log groups: `/aws/lambda/cognito-service-dev-sign_up`, etc.

2. **Via Serverless CLI**:
```bash
# View logs for a specific function
serverless logs -f sign_up --tail

# View logs for all functions
serverless logs --tail
```

### API Gateway Logs

Enable API Gateway logging:
1. Go to API Gateway → Your API → Stages → dev
2. Enable CloudWatch Logs
3. Set log level to INFO or ERROR

### Common Issues

1. **"User already exists"**
   - Delete the user from Cognito User Pool or use a different email

2. **"Invalid password"**
   - Check password meets User Pool requirements
   - Ensure password includes required character types

3. **"Not authorized to perform: cognito-idp:SignUp"**
   - Check IAM role permissions in `serverless.yml`
   - Verify User Pool ARN is correct

4. **"Unable to verify email address"**
   - Check Cognito email configuration
   - For production, configure Amazon SES

## Troubleshooting

### Issue: Deployment Fails

**Solution**:
- Verify AWS credentials: `aws sts get-caller-identity`
- Check environment variables are set
- Ensure you have permissions to create Lambda, API Gateway, and IAM resources

### Issue: "Module not found" Error

**Solution**:
- Ensure `serverless-python-requirements` plugin is installed
- Run `pip install -r requirements.txt` in your virtual environment
- Check `serverless.yml` has the plugin listed

### Issue: CORS Errors

**Solution**:
- CORS is enabled in `serverless.yml` (`cors: true`)
- If issues persist, check API Gateway CORS settings
- Verify your frontend is sending proper headers

### Issue: Verification Code Not Received

**Solution**:
- Check email spam folder
- Verify email/phone in Cognito User Pool settings
- For SMS: Check Cognito SMS limits (50/day for default)
- For production: Configure Amazon SES/SNS

### Issue: Tokens Not Working

**Solution**:
- Verify tokens are being returned correctly
- Check token expiration (default: 1 hour for access token)
- Use refresh token to get new access tokens
- Verify App Client settings allow the authentication flow

## Project Structure

```
AWS-Cognito/
├── handlers.py           # Lambda function handlers (signup, signin, verify)
├── serverless.yml        # Serverless Framework configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Security Considerations

1. **Never commit credentials**: Use environment variables or AWS Secrets Manager
2. **Use HTTPS**: All API Gateway endpoints use HTTPS by default
3. **Token Security**: Store tokens securely on client side (not in localStorage for sensitive apps)
4. **Password Policy**: Enforce strong password requirements in Cognito
5. **MFA**: Enable MFA for production environments
6. **Rate Limiting**: Consider implementing rate limiting for API endpoints

## Next Steps

- [ ] Add refresh token endpoint
- [ ] Implement password reset functionality
- [ ] Add user profile management
- [ ] Set up CI/CD pipeline
- [ ] Configure custom domain for API Gateway
- [ ] Add API key authentication for additional security
- [ ] Implement request validation
- [ ] Add comprehensive error handling

## Additional Resources

- [AWS Cognito Documentation](https://docs.aws.amazon.com/cognito/)
- [Serverless Framework Documentation](https://www.serverless.com/framework/docs)
- [Boto3 Cognito Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html)
- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)

## License

This project is open source and available for use.

---

**Happy Coding! 🚀**
