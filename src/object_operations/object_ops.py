import os
from typing import Any, Optional

from src.bucket_operations.bucket_ops import S3Bucket
from src.main import S3Resource


class S3Object(S3Resource):
    """
    Class for S3 object operations.
    """

    def __init__(self, region_name: str, bucket_name: str):
        super().__init__(region_name)
        self.bucket_name = bucket_name
        if not self.check_resource_exists('bucket', bucket_name=bucket_name):
            print(f"Warning: Bucket {bucket_name} doesn't exist")
            bucket_handler = S3Bucket(region_name)
            bucket_handler.create_bucket(bucket_name)
        self.bucket = self.resource.Bucket(bucket_name)

    def upload_file(self, local_file_path: str, object_name: Optional[str] = None, extra_args: Optional[dict[str, Any]] = None):
        """
        Upload object to s3
        """
        if not object_name:
            object_name = os.path.basename(local_file_path)

        try:
            response = self.bucket.upload_file(
                Filename=local_file_path, Key=object_name, ExtraArgs=extra_args)
            print("File created Succesfully", response)
            return response
        except Exception as e:
            print("Error when creating file", e)
            return None

    def download_file(self, object_name: str, download_path: str, extra_args: Optional[dict[str, Any]] = None):
        """
        Download object from S3
        """
        try:
            response = self.bucket.download_file(
                Key=object_name, Filename=download_path, ExtraArgs=extra_args)
            print("succesfully downloaded file", response)
            return response
        except Exception as e:
            print("Error occured when downloading file")
            return None

    def delete_object(self, object_key: str):
        """
        Delete an object from the bucket.
        """
        try:
            self.bucket.delete_object(
                Key=object_key
            )
            print(f"Successfully deleted {object_key} from {self.bucket_name}")
            return True
        except Exception as e:
            print(f"Error deleting object: {e}")
            return False

    def list_objects(self, prefix: str = None, max_keys: int = None):
        """
        List objects in the bucket with optional prefix filtering.
        """
        try:
            params = {'Bucket': self.bucket_name}
            if prefix:
                params['Prefix'] = prefix
            if max_keys:
                params['MaxKeys'] = max_keys

            response = self.client.list_objects_v2(**params)
            return response.get('Contents', [])
        except Exception as e:
            print(f"Error listing objects: {e}")
            return []
