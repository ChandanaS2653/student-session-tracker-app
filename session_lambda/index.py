import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentSessions')

def lambda_handler(event, context):  
    try:
        body = json.loads(event['body'])
        student_id = body.get('student_id')

        if not student_id:
            return response(400, {'message': 'Student ID is required'})

        # Fetch session info
        db_res = table.get_item(Key={'student_id': student_id})
        item = db_res.get('Item')

        if not item:
            return response(404, {'message': 'Session not found'})

        return response(200, {
            'login_time': item.get('login_time', 'N/A'),
            'logout_time': item.get('logout_time', 'N/A'),
            'session_duration': item.get('session_duration', 'N/A')
        })

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
