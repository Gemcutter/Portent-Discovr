import boto3

boto3

ACCESS_KEY = -1
SECRET_KEY = -1
SESSION_TOKEN = -1

client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN
)
