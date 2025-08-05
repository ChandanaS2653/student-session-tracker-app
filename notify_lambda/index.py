import json
import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        message = body.get('message', 'Hello from NotifyLambda!')

        # Replace with your SNS topic ARN
        topic_arn = 'arn:aws:sns:us-east-1:123456789012:MyTopic'

        sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject='Student Session Notification'
        )

        return response(200, {'message': 'Notification sent successfully.'})

    except Exception as e:
        return response(500, {'message': f'Error: {str(e)}'})

def response(status, body):
    return {
        'statusCode': status,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*'
        },
        'body': json.dumps(body)
    }
