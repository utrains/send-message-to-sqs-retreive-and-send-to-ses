import json
import logging
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define our methods
postMethod = 'POST'


#define our Paths
messagePath = '/message'


def send_sqs_message(QueueName, msg_body,orderId):
    """

    :param sqs_queue_url: String URL of existing SQS queue
    :param msg_body: String message body
    :return: Dictionary containing information about the sent message. If
        error, returns None.
    """

    # Send the SQS message
    sqs_client = boto3.client('sqs')
    sqs_queue_url = sqs_client.get_queue_url(
    QueueName=QueueName
)['QueueUrl']
    try:
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                      MessageBody=json.dumps(msg_body), MessageGroupId="GroupId",MessageDeduplicationId=str(orderId))
    except ClientError as e:
        logging.error(e)
        return None
    return msg


def lambda_handler(event, context):
    print(event)
    QueueName = 'food-ordering-queue.fifo'
    logger.info(event) #log the request event to see how the request looks like
    httpMethod = event['httpMethod'] #extract the http method from our event object
    path = event['path'] #extract the path
    if httpMethod == postMethod and path == messagePath:
       message= json.loads(event['body'])
       #print(message)
       order_message = "message:" + message['message'] + "\n email: "+ message['email'] + "\nfood:" + message['food'] + "\n number of orders:" + message['number']
       order_id= message['id']
       msg=send_sqs_message(QueueName,order_message,order_id)
       if msg is not None:
           logging.info(f'Sent SQS message ID: {msg["MessageId"]}')
           response ={
                'statusCode': 200,
                'body': json.dumps(event)
            
                    }
    else:
        response = buildResponse(404, 'Not found')
    
    return response

