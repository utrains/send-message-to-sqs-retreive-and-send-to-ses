from __future__ import print_function
import time

import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

#function to send email
def send_email(message):
    SENDER = "noel.tatah@utrains.org" # must be verified in AWS SES Email
    RECIPIENT = "tatahnoellimnyuy@gmail.com" # must be verified in AWS SES Email

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "ca-central-1"

    # The subject line for the email.
    SUBJECT = "this order is destined for shop1!!"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Hey Hi...\r\n"
                "here is an oder \n {message} "
                "\n thankyou"
                ).format(message=message)
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head>order from website </head>
    <body>
    <h1>Hey Hi...</h1>
    <p>There is  a clients order
        <a href=''>{message}</a> using the
        </p>
    </body>
    </html>
                """.format(message=message)            

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
        
                        'Data': BODY_HTML
                    },
                    'Text': {
        
                        'Data': BODY_TEXT
                    },
                },
                'Subject': {

                    'Data': SUBJECT
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])



def lambda_handler(event, context):
    for record in event['Records']:
        print("test")
        payload = record["body"]
        print(str(payload))
        send_email(payload)
    print("shop1")
    time.sleep(5)
