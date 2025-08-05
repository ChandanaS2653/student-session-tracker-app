import json
import boto3
import hashlib
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentSessions')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        username = body.get("username")
        password = body.get("password")

        if not username or not password:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Username and password are required"})
            }

        # Generate a unique student_id
        student_id = str(uuid.uuid4())

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Save to DynamoDB
        table.put_item(
            Item={
                "student_id": student_id,
                "username": username,
                "password": hashed_password
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User registered successfully", "student_id": student_id})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }
