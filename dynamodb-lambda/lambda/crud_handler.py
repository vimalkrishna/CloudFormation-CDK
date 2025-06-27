import json     # For handling JSON serialization/deserialization
import boto3    # AWS SDK to interact with DynamoDB
import os       # For accessing environment variables
from datetime import datetime
from decimal import Decimal 
from boto3.dynamodb.conditions import Key
import uuid    # For generating unique user IDs

# Initialize DynamoDB resource using environment variable for table name
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

class DecimalEncoder(json.JSONEncoder):
    """Custom JSONEncoder to convert Decimal types to float.
        DynamoDB stores numbers as Decimal by default."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    """
    AWS Lambda handler entry point.
    Determines the HTTP method and routes to appropriate CRUD function.
    Handles: POST (create), GET (read), PUT (update), DELETE (delete)
    """
    try:
        http_method = event['httpMethod']
        path_parameters = event.get('pathParameters', {})
        
        if http_method == 'POST':
            return create_user(event)
        elif http_method == 'GET':
            if path_parameters and 'user_id' in path_parameters:
                return get_user(path_parameters['user_id'])
            else:
                return list_users()
        elif http_method == 'PUT':
            return update_user(event, path_parameters['user_id'])
        elif http_method == 'DELETE':
            return delete_user(path_parameters['user_id'])
        else:
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method not allowed'})
            }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def create_user(event):
    """Create a new user. Generates a user_id if not provided, supports optional fields."""
    try:
        # Parse request body
        body = json.loads(event['body'])
        
        # Generate user_id if not provided
        user_id = body.get('user_id', str(uuid.uuid4()))
        
        # Create user item
        user_item = {
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat(),
            'name': body['name'],
            'email': body['email'],
            'age': body.get('age', 0),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Add optional fields
        if 'phone' in body:
            user_item['phone'] = body['phone']
        if 'address' in body:
            user_item['address'] = body['address']
        
        # Put item in DynamoDB
        table.put_item(Item=user_item)
        
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'User created successfully',
                'user': user_item
            }, cls=DecimalEncoder)
        }
        
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Missing required field: {str(e)}'})
        }

def get_user(user_id):
    """Get a specific user by user_id record by ID, returns the most recent version."""
    try:
        # Query for the user (we need to get the latest timestamp)
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id),
            ScanIndexForward=False,  # Sort in descending order (latest first)
            Limit=1
        )
        
        if response['Items']:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'user': response['Items'][0]
                }, cls=DecimalEncoder)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def list_users():
    """Retrieves the latest version of all user records. Uses naive in-memory filtering; not scalable for large datasets."""
    try:
        # Scan the table (not efficient for large tables, but good for learning)
        response = table.scan()
        
        # Group by user_id and keep only the latest timestamp
        users_dict = {}
        for item in response['Items']:
            user_id = item['user_id']
            if user_id not in users_dict or item['timestamp'] > users_dict[user_id]['timestamp']:
                users_dict[user_id] = item
        
        users_list = list(users_dict.values())
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'users': users_list,
                'count': len(users_list)
            }, cls=DecimalEncoder)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def update_user(event, user_id):
    """Update an existing user. Creates a new version (with new timestamp).
    """
    try:
        # Parse request body
        body = json.loads(event['body'])
        
        # First, get the current user to check if it exists
        current_response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id),
            ScanIndexForward=False,
            Limit=1
        )
        
        if not current_response['Items']:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }
        
        current_user = current_response['Items'][0]
        
        # Create updated user item with new timestamp
        updated_user = current_user.copy()
        updated_user['timestamp'] = datetime.utcnow().isoformat()
        updated_user['updated_at'] = datetime.utcnow().isoformat()
        
        # Update fields from request body
        allowed_fields = ['name', 'email', 'age', 'phone', 'address']
        for field in allowed_fields:
            if field in body:
                updated_user[field] = body[field]
        
        # Put the updated item
        table.put_item(Item=updated_user)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'User updated successfully',
                'user': updated_user
            }, cls=DecimalEncoder)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def delete_user(user_id):
    """Deletes all versions of a user record from DynamoDB."""
    try:
        # First, get all versions of the user
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        
        if not response['Items']:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }
        
        # Delete all versions
        deleted_count = 0
        for item in response['Items']:
            table.delete_item(
                Key={
                    'user_id': item['user_id'],
                    'timestamp': item['timestamp']
                }
            )
            deleted_count += 1
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'User deleted successfully. Removed {deleted_count} versions.'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }