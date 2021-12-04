import boto3

client = boto3.Client('sns', 'us-east-2')
client.publish(PhoneNumber="+1 (609)212-7855", message="Hello from AWS!")
