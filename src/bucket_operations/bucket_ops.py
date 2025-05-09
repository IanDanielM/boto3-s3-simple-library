from src.main import S3Resource
from uuid import uuid4
from datetime import datetime
from typing import Optional

class S3Bucket(S3Resource):
    """
    Class for S3 bucket operations.
    """
    @staticmethod
    def create_bucket_name(bucket_name: str) -> str:
        """
        Create a unique bucket name by appending a UUID to the provided name.
        """
        return f"{bucket_name}-{uuid4()}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    

    def create_bucket(self, bucket_name: str, ACL='private'):
        """
        Create a new S3 bucket with the specified name and ACL.
        """
        bucket_name = self.s3.create_bucket_name(bucket_name)
        try:
            create_bc = self.s3.create_bucket(bucket_name, ACL)
            if 'Location' in create_bc:
                print(f"Bucket {bucket_name} created successfully.")
            else:
                print(f"Failed to create bucket {bucket_name}.")
            return create_bc
        except Exception as e:
            print(f"Error creating bucket {bucket_name}: {e}")
            return None
        
    
    def list_buckets(self, max_buckets: Optional[int] = None, Prefix: Optional[str] = None) -> list:
        """
        List all buckets in the S3 account.
        """
        try:
            params = {}
            if max_buckets:
                params['MaxBuckets'] = max_buckets
            if Prefix:
                params['Prefix'] = Prefix

            response = self.s3.list_buckets(**params)
            if 'Buckets' in response:
                return [bucket['Name'] for bucket in response.get('Buckets', [])]
            else:
                print("No buckets found.")
                return []
        except Exception as e:
            print(f"Error listing buckets: {e}")
            return []
                
            
            

        