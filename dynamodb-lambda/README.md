# DynamoDB project for User management, CD/CD and DevOps!
A real world example for learning DynamoDB and Serverless architecture. Writing and using Indexs, Query & Scan operations are very important in DynamoDB. The project will be extended for CD/CD, Disaster recovers nd multi-region deployment..
This application allows CRUD operations on user data stored in DynamoDB. 
We will expand the database to Customer Profile Management with search function.
We can use it for Device Registry.

 
See the companion [Git Repository](https://github.com/vimalkrishna/CloudFormation-CDK/tree/main/dynamodb-lambda "Discussion on implementing DynamoDB API"), 

and Blog to discuss [implementation](https://aws-cloud-deployment.blogspot.com/2025/06/dynamodb-lambda-cdk-1.html)
 and improvement plans.

**Basic architecture diagram** (created using draw.io)

![Arch diagram](img/DynamoDB-APIGateway.drawio.svg)

## Project components:
1. CDK Stack - Creates DynamoDB table with GSI and Lambda functions
2. Three Lambda Functions:
    * __CRUD Handler__  - Basic create, read, update, delete operations
    * __Batch Handler__ - Batch operations and sample data population
    * __Query Handler__ - Advanced query patterns and demonstrations


### Key DynamoDB concepts 
| Concept | Example in Project |
| --- | --- |
| `Primary Key` | Design Composite key (user_id + timestamp) | 
| `Global Secondary Index` | Query users by email | 
| `Query Operation` | Efficient retrieval by partition Key | 
| `Scan Operation` | Filter by age range across table | 
| `Batch Operations` | Create/read multiple users efficiently | 
| `Data Versioning` |  Track user changes over time | 
| `Filter Expressions` | Server-side filtering during scans | 

### Learning objectives:
- Master DynamoDB table design and key concepts
- Understand Query vs Scan operations and their performance implications
- Implement Global Secondary Indexes (GSI) for flexible access patterns
- Practice batch operations for efficient bulk processing
- Learn data versioning and audit trail patterns
- Explore serverless architecture with Lambda and API Gateway

### More features to add:
- Add authentication with AWS Cognito
- Implement DynamoDB Streams for real-time processing
- Add TTL for automatic data expiration
- Create additional GSIs for other access patterns
- Implement DynamoDB Transactions
- Add input validation and error handling improvements

### Further enhancements
- Add API Gateway request validation
- Implement proper logging and monitoring
- Add CI/CD pipeline
- Create comprehensive test suite
- Add API documentation with OpenAPI

### Technology stack:

- Infrastructure: AWS CDK (Python)
- API Layer: Amazon API Gateway
- Compute: AWS Lambda (Python upto 3.9)
- Database: Amazon DynamoDB
- Deployment: AWS CloudFormation (by CDK)

## Base URL
`https://api-gateway-url.com/prod`


## API endpoints
After deployment, you'll get an API Gateway URL. The available endpoints are:

## CRUD operations

* `POST /users` - Create a new user
* `GET /users` - List all users 
* `GET /users/{user_id}` - Get a specific user
* `PUT /users/{user_id}` - Update a user
* `DELETE /users/{user_id}` - Delete a user

## Table schema
```
Table: users-learning-table
- Partition Key: user_id (String)
- Sort Key: timestamp (String)
- Global Secondary Index: email-index
   - Partition Key: email (String)
- Attributes:
    - name (String)
    - email (String)
    - age (Number)
    - phone (String) [Optional]
    - address (String) [Optional]
    - created_at (String)
    - updated_at (String)
```

## Batch operations

POST /batch - Batch operations (write, read, populate sample data)

Query Operations

GET /query - Various query patterns






