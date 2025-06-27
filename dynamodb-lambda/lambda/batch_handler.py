import json
import boto3
import os
from datetime import datetime
from decimal import Decimal
import uuid

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

class DecimalEncoder(json.JSONEncoder):
    """Helper class to handle Decimal serialization"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    """
    Main Lambda handler for batch operations
    Supports batch write and batch read operations
    """
    try:
        body = json.loads(event['body'])
        operation = body.get('operation')
        
        if operation == 'batch_write':
            return batch_write_users(body.get('users', []))
        elif operation == 'batch_read':
            return batch_read_users(body.get('user_ids', []))
        elif operation == 'populate_sample_data':
            return populate_sample_data()
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Invalid operation. Supported: batch_write, batch_read, populate_sample_data'
                })
            }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def batch_write_users(users_data):
    """Batch write multiple users"""
    try:
        if not users_data:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No users data provided'})
            }
        
        # DynamoDB batch_writer handles batching automatically (max 25 items per batch)
        with table.batch_writer() as batch:
            created_users = []
            
            for user_data in users_data:
                # Generate user_id if not provided
                user_id = user_data.get('user_id', str(uuid.uuid4()))
                
                user_item = {
                    'user_id': user_id,
                    'timestamp': datetime.utcnow().isoformat(),
                    'name': user_data['name'],
                    'email': user_data['email'],
                    'age': user_data.get('age', 0),
                    'created_at': datetime.utcnow().isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }
                
                # Add optional fields
                if 'phone' in user_data:
                    user_item['phone'] = user_data['phone']
                if 'address' in user_data:
                    user_item['address'] = user_data['address']
                
                batch.put_item(Item=user_item)
                created_users.append(user_item)
        
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': f'Successfully created {len(created_users)} users',
                'users': created_users
            }, cls=DecimalEncoder)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def batch_read_users(user_ids):
    """Batch read multiple users"""
    try:
        if not user_ids:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No user IDs provided'})
            }
        
        # For batch reads, we need to specify exact keys (partition + sort key)
        # Since we want the latest version, we'll query each user individually
        found_users = []
        not_found_users = []
        
        for user_id in user_ids:
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id),
                ScanIndexForward=False,  # Latest first
                Limit=1
            )
            
            if response['Items']:
                found_users.append(response['Items'][0])
            else:
                not_found_users.append(user_id)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'found_users': found_users,
                'not_found_users': not_found_users,
                'total_requested': len(user_ids),
                'total_found': len(found_users)
            }, cls=DecimalEncoder)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def populate_sample_data():
    """Populate the table with sample data for testing"""
    try:
        sample_users = [
            {
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'age': 30,
                'phone': '+1234567890',
                'address': '123 Main St, New York, NY'
            },
            {
                'name': 'Jane Smith',
                'email': 'jane.smith@example.com',
                'age': 28,
                'phone': '+1234567891',
                'address': '456 Oak Ave, Los Angeles, CA'
            },
            {
                'name': 'Bob Johnson',
                'email': 'bob.johnson@example.com',
                'age': 35,
                'phone': '+1234567892',
                'address': '789 Pine St, Chicago, IL'
            },
            {
                'name': 'Alice Brown',
                'email': 'alice.brown@example.com',
                'age': 26,
                'phone': '+1234567893',
                'address': '321 Elm St, Houston, TX'
            },
            {
                'name': 'Charlie Wilson',
                'email': 'charlie.wilson@example.com',
                'age': 42,
                'phone': '+1234567894',
                'address': '654 Maple Dr, Phoenix, AZ'
            },
            {
                'name': 'Diana Davis',
                'email': 'diana.davis@example.com',
                'age': 31,
                'phone': '+1234567895',
                'address': '987 Cedar Ln, Philadelphia, PA'
            },
            {
                'name': 'Frank Miller',
                'email': 'frank.miller@example.com',
                'age': 29,
                'phone': '+1234567896',
                'address': '147 Birch Rd, San Antonio, TX'
            },
            {
                'name': 'Grace Taylor',
                'email': 'grace.taylor@example.com',
                'age': 33,
                'phone': '+1234567897',
                'address': '258 Spruce St, San Diego, CA'
            }
        ]
        
        # Use batch write to insert sample data
        with table.batch_writer() as batch:
            created_users = []
            
            for user_data in sample_users:
                user_item = {
                    'user_id': str(uuid.uuid4()),
                    'timestamp': datetime.utcnow().isoformat(),
                    'name': user_data['name'],
                    'email': user_data['email'],
                    'age': user_data['age'],
                    'phone': user_data['phone'],
                    'address': user_data['address'],
                    'created_at': datetime.utcnow().isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }
                
                batch.put_item(Item=user_item)
                created_users.append(user_item)
        
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': f'Successfully populated table with {len(created_users)} sample users',
                'users': created_users
            }, cls=DecimalEncoder)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }