import json
import boto3
import hashlib
import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentSessions')

def lambda_handler(event, context):
    try:
        print("Received event:", event)

        body = json.loads(event['body'])
        student_id = body.get('student_id')
        username = body.get('username')
        password = body.get('password')

        if not (student_id and username and password):
            return response(400, {'message': 'All fields are required.'})

        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        # Fetch user
        db_res = table.get_item(Key={'student_id': student_id})
        user = db_res.get('Item')

        if not user or user.get('username') != username or user.get('password') != hashed_pw:
            return response(401, {'message': 'Invalid credentials'})

        # Update login time
        login_time = datetime.datetime.utcnow().isoformat()
        table.update_item(
            Key={'student_id': student_id},
            UpdateExpression="SET login_time = :lt, logout_time = :lo, session_duration = :sd",
            ExpressionAttributeValues={
                ':lt': login_time,
                ':lo': None,
                ':sd': None
            }
        )

        return response(200, {
            'message': f'Welcome, {username}!',
            'student_id': student_id,
            'username': username,
            'login_time': login_time
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
