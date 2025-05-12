# S3Learning

A simple AWS S3 operations library for Python.

## Installation

```bash
pip install s3learning
```

## AWS Credentials Setup

This library requires AWS credentials to authenticate with AWS services. You can set up your credentials in one of the following ways:

1. Environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_preferred_region
```

2. AWS credentials file (~/.aws/credentials):
```
[default]
aws_access_key_id = your_access_key
aws_secret_access_key = your_secret_key
```

3. AWS config file (~/.aws/config):
```
[default]
region = your_preferred_region
```

For more information, see [AWS credentials configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html).

## Usage

```python
from s3learning import S3Bucket, S3Object

# Create a bucket handler
bucket_handler = S3Bucket('us-east-1')
buckets = bucket_handler.list_buckets()
print(f"Available buckets: {buckets}")

# Work with objects in a bucket
object_handler = S3Object('us-east-1', 'my-bucket-name')
object_handler.upload_file('local_file.txt', 'remote_name.txt')
```

## Features

- Bucket operations: create, list, delete buckets
- Object operations: upload, download, delete, list objects
- Lifecycle policy management
- Resource existence checking
