
# DynamoDB project for User management!
This API allows CRUD operations on user data stored in DynamoDB.

## Base URL
`https://your-api-gateway-url.com/prod`


## DynamoDB Table Schema
`Table Name: users-learning-table`

`Partition Key: user_id (String)`

`Sort Key: timestamp (String)`

`Global Secondary Index: email-index with partition key email`

## API Endpoints
After deployment, you'll get an API Gateway URL. The available endpoints are:

## CRUD Operations

* `POST /users` - Create a new user
* `GET /users` - List all users (latest versions)
* `GET /users/{user_id}` - Get a specific user
* `PUT /users/{user_id}` - Update a user
* `DELETE /users/{user_id}` - Delete a user


## Batch Operations

POST /batch - Batch operations (write, read, populate sample data)

Query Operations

GET /query - Various query patterns



## Other Useful Notes

 
