import boto3
from typing import Any, Optional
from botocore.config import Config


# parent class for S3 operations
class S3Resource:
    def __init__(self, region_name: str):
        self.s3 = boto3.resource('s3', region_name=region_name)
        self.session = boto3.session.Session(region_name=region_name)
        self.client = self.session.client('s3')

    def check_resource_exists(self, resource_type: str, bucket_name: Optional[str]=None, object_name: Optional[str]=None) -> bool:
        if resource_type == 'bucket':
            try:
                self.s3.meta.client.head_bucket(Bucket=bucket_name)
                print("Bucket Found")
                return True
            except Exception as e:
                print(f"Bucket {bucket_name} does not exist: {e}")
                return False
        if resource_type == 'object':
            try:
                self.s3.meta.client.head_object(Bucket=bucket_name, Key=object_name)
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
    

    

s3_test = S3Resource('us-east-1')
# s3_test.check_resource_exists(resource_type='object', bucket_name='a-cli-demo7977', object_name='backuptl.sql')
s3_test.format_s3_path(bucket_name='a-cli-demo7977')



            



