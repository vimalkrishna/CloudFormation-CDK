import json
import boto3
import os
from datetime import datetime
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr

# Initialize DynamoDB resource
# Pull table name from Lambda environment variable which is injected by CDK
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

class DecimalEncoder(json.JSONEncoder):
    """Helper class to handle Decimal serialization"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

# This is the Entry point for Lambda function
def lambda_handler(event, context):
    """
    This Lambda handler for query operations uses query patterns in DynamoDB.
    Dispatches incoming query requests based on 'operation' query param.
    This is DynamoDB access patterns without exposing internal implementation details.
    """
    try:
        query_params = event.get('queryStringParameters', {}) or {}
        operation = query_params.get('operation')
        
        if operation == 'query_by_user':
            return query_by_user(query_params.get('user_id'))
        elif operation == 'query_by_email':
            return query_by_email(query_params.get('email'))
        elif operation == 'scan_by_age':
            return scan_by_age(query_params.get('min_age'), query_params.get('max_age'))
        elif operation == 'query_user_history':
            return query_user_history(query_params.get('user_id'))
        elif operation == 'query_recent_users':
            return query_recent_users(query_params.get('hours', '24'))
        else:
            return get_available_operations()
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_available_operations():
    """Return available query operations for client introspection, making the endpoint self-documenting."""
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Available query operations',
            'operations': {
                'query_by_user': {
                    'description': 'Query specific user (latest version)',
                    'parameters': 'user_id',
                    'example': '/query?operation=query_by_user&user_id=12345'
                },
                'query_by_email': {
                    'description': 'Query user by email using GSI',
                    'parameters': 'email',
                    'example': '/query?operation=query_by_email&email=john@example.com'
                },
                'scan_by_age': {
                    'description': 'Scan users by age range',
                    'parameters': 'min_age, max_age (optional)',
                    'example': '/query?operation=scan_by_age&min_age=25&max_age=35'
                },
                'query_user_history': {
                    'description': 'Get all versions of a user',
                    'parameters': 'user_id',
                    'example': '/query?operation=query_user_history&user_id=12345'
                },
                'query_recent_users': {
                    'description': 'Get users created in recent hours',
                    'parameters': 'hours (default: 24)',
                    'example': '/query?operation=query_recent_users&hours=12'
                }
            }
        })
    }
# to get the most recent version of a user
def query_by_user(user_id):
    """Query for a specific user (latest version)"""
    try:
        if not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'user_id parameter is required'})
            }
        
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id),
            ScanIndexForward=False,  # Latest first
            Limit=1
        )
        
        if response['Items']:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'user': response['Items'][0],
                    'query_type': 'Primary Key Query'
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

# This Query handler lookup user(s) by email via GSI 
def query_by_email(email):
    """Query user by email using Global Secondary Index"""
    try:
        if not email:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'email parameter is required'})
            }
        
        response = table.query(
            IndexName='email-index',
            KeyConditionExpression=Key('email').eq(email)
        )
        
        if response['Items']:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'users': response['Items'],
                    'count': len(response['Items']),
                    'query_type': 'Global Secondary Index Query'
                }, cls=DecimalEncoder)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No users found with that email'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
# This scan handler retrieve users within an age range
def scan_by_age(min_age, max_age):
    """Scan table filtering by age range"""
    try:
        # Convert to integers
        min_age = int(min_age) if min_age else 0
        max_age = int(max_age) if max_age else 200
        
        # Build filter expression
        filter_expression = Attr('age').between(min_age, max_age)
        
        response = table.scan(
            FilterExpression=filter_expression
        )
        
        # Group by user_id to get latest version of each user
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
                'count': len(users_list),
                'age_range': f'{min_age}-{max_age}',
                'query_type': 'Scan with Filter Expression'
            }, cls=DecimalEncoder)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
# This handler gets full history (versions) for a user
def query_user_history(user_id):
    """Get all versions/history of a specific user"""
    try:
        if not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'user_id parameter is required'})
            }
        
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id),
            ScanIndexForward=False  # Latest first
        )
        
        if response['Items']:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'user_id': user_id,
                    'versions': response['Items'],
                    'version_count': len(response['Items']),
                    'query_type': 'User History Query'
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

# This handler gets users created in the last N hours
def query_recent_users(hours):
  
    try:
        hours = int(hours) if hours else 24
        
        # Calculate cutoff time
        from datetime import timedelta
        cutoff_time = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
        
        # Scan with filter for recent users
        response = table.scan(
            FilterExpression=Attr('created_at').gt(cutoff_time)
        )
        
        # Group by user_id to get unique users
        users_dict = {}
        for item in response['Items']:
            user_id = item['user_id']
            if user_id not in users_dict or item['timestamp'] > users_dict[user_id]['timestamp']:
                users_dict[user_id] = item
        
        users_list = list(users_dict.values())
        
        # Sort by creation time
        users_list.sort(key=lambda x: x['created_at'], reverse=True)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'users': users_list,
                'count': len(users_list),
                'timeframe': f'Last {hours} hours',
                'cutoff_time': cutoff_time,
            }, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }