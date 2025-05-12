import boto3
from typing import Any, Optional
from botocore.config import Config


# parent class for S3 operations
class S3Resource:
    def __init__(self, region_name: str):
        self.resource = boto3.resource('s3', region_name=region_name)
        self.session = boto3.session.Session(region_name=region_name)
        self.client = self.session.client('s3')

    def check_resource_exists(self, resource_type: str, bucket_name: Optional[str]=None, object_name: Optional[str]=None) -> bool:
        if resource_type == 'bucket':
            try:
                self.resource.meta.client.head_bucket(Bucket=bucket_name)
                print("Bucket Found")
                return True
            except Exception as e:
                print(f"Bucket {bucket_name} does not exist: {e}")
                return False
        if resource_type == 'object':
            try:
                self.resource.meta.client.head_object(Bucket=bucket_name, Key=object_name)
                return True
            except Exception as e:
                print(f"Object {object_name} does not exist: {e}")
                return False

        print("Can onlcy check for buckets or objects")
        return False
    
    def format_s3_path(self, bucket_name: str, prefix: str = None) -> str:
        if not prefix:
            return f"s3://{bucket_name}/"
        return f"s3://{bucket_name}/{prefix}"
