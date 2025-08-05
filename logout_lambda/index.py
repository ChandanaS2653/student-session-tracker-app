import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentSessions')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        student_id = body.get('student_id')

        if not student_id:
            return response(400, {'message': 'Student ID is required for logout.'})

        # Fetch user
        db_res = table.get_item(Key={'student_id': student_id})
        user = db_res.get('Item')

        if not user or not user.get('login_time'):
            return response(404, {'message': 'No active login session found.'})

        # Calculate session duration
        logout_time = datetime.utcnow().isoformat()
        login_time = user.get('login_time')

        session_duration = "N/A"
        if login_time:
            login_dt = datetime.fromisoformat(login_time)
            logout_dt = datetime.fromisoformat(logout_time)
            session_duration = str(logout_dt - login_dt)

        # Update logout details
        table.update_item(
            Key={'student_id': student_id},
            UpdateExpression="SET logout_time = :lo, session_duration = :sd",
            ExpressionAttributeValues={
                ':lo': logout_time,
                ':sd': session_duration
            }
        )

        return response(200, {
            'message': 'Logged out successfully.',
            'logout_time': logout_time,
            'session_duration': session_duration
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
