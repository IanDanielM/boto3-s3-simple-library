from datetime import datetime
from typing import Optional
from uuid import uuid4

from src.main import S3Resource


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

    def create_bucket(self, bucket_name: str, acl: str = 'private'):
        """
        Create a new S3 bucket with the specified name and ACL.
        """
        bucket_name = self.create_bucket_name(bucket_name)
        try:
            bucket = self.resource.create_bucket(ACL=acl, Bucket=bucket_name)
            return bucket
        except Exception as e:
            print(f"Error creating bucket {bucket_name}: {e}")
            return None

    def list_buckets(self, max_buckets: Optional[int] = None, prefix: Optional[str] = None) -> list:
        """
        List all buckets in the S3 account.
        """
        try:
            params = {}
            if max_buckets:
                params['MaxBuckets'] = max_buckets
            if prefix:
                params['Prefix'] = prefix

            response = self.client.list_buckets(**params)
            print(response)
            return [bucket['Name'] for bucket in response.get('Buckets', [])]
        except Exception as e:
            print(f"Error listing buckets: {e}")
            return []

    def set_lifecycle_policy(self, bucket_name: str, **kwargs):
        """
        Set a lifecycle policy for an S3 bucket using flexible keyword arguments.
        """
        # Default rule settings
        if not self.check_resource_exists('bucket', bucket_name=bucket_name):
            print(f"Bucket {bucket_name} does not exist")
            return None
        rule = {
            'ID': kwargs.get('rule_id', 'DefaultRule'),
            'Status': kwargs.get('status', 'Enabled'),
            'Filter': {}
        }
        
        # Handle filter options
        filter_elements = {}
        
        if 'prefix' in kwargs and kwargs['prefix']:
            filter_elements['Prefix'] = kwargs['prefix']
        
        if 'tags' in kwargs and kwargs['tags']:
            filter_elements['Tag'] = kwargs['tags'] if len(kwargs['tags']) == 1 else {'And': {'Tags': kwargs['tags']}}
        
        if len(filter_elements) > 1:
            rule['Filter'] = {'And': filter_elements}
        elif len(filter_elements) == 1:
            rule['Filter'] = filter_elements
        
        # Expiration settings
        expiration = {}
        if 'expiration_days' in kwargs:
            expiration['Days'] = kwargs['expiration_days']
        if 'expired_object_delete_marker' in kwargs:
            expiration['ExpiredObjectDeleteMarker'] = kwargs['expired_object_delete_marker']
        
        if expiration:
            rule['Expiration'] = expiration
        
        # Transitions
        if 'transitions' in kwargs and kwargs['transitions']:
            rule['Transitions'] = kwargs['transitions']
        
        # Noncurrent version expiration
        if 'noncurrent_version_expiration_days' in kwargs:
            rule['NoncurrentVersionExpiration'] = {
                'NoncurrentDays': kwargs['noncurrent_version_expiration_days']
            }
        
        # Noncurrent version transitions
        if 'noncurrent_version_transitions' in kwargs and kwargs['noncurrent_version_transitions']:
            rule['NoncurrentVersionTransitions'] = kwargs['noncurrent_version_transitions']
        
        lifecycle_config = {
            'Rules': [rule]
        }
        
        try:
            response = self.resource.put_bucket_lifecycle_configuration(
                Bucket=bucket_name,
                LifecycleConfiguration=lifecycle_config
            )
            print(response)
            if 'ResponseMetadata' in response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print(f"Lifecycle policy set for bucket {bucket_name}.")
            else:
                print(f"Failed to set lifecycle policy for bucket {bucket_name}.")
                return None
        except Exception as e:
            print(f"Error setting lifecycle policy for bucket {bucket_name}: {e}")
            return None
        
    def delete_bucket(self, bucket_name: str, force_empty: bool = False):
        """
        Delete an S3 bucket.
        """
        try:
            if not self.check_resource_exists('bucket', bucket_name=bucket_name):
                print(f"Bucket {bucket_name} does not exist")
                return None
            if force_empty:
                bucket = self.resource.Bucket(bucket_name)
                bucket.objects.all().delete()
                # If versioning is enabled
                # if bucket.object_versions:
                #     for version in bucket.object_versions.all():
                #         version.delete()
                print(f"All objects in bucket {bucket_name} deleted.")
            self.client.delete_bucket(Bucket=bucket_name)
            print(f"Bucket {bucket_name} deleted successfully.")
        except Exception as e:
            print(f"Error deleting bucket {bucket_name}: {e}")
