from django.conf import settings
import boto3
import logging
from botocore.config import Config

class S3:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
            config=Config(signature_version='s3v4')
        )

    def generate_presigned_url(self, object_name, client_method='get_object', expiration=3600):
        """
        Generate a presigned S3 URL for S3 operations
        """
        try:
            response = self.client.generate_presigned_url(
                ClientMethod=client_method,
                Params={
                    'Bucket': settings.AWS_S3_BUCKET_NAME,
                    'Key': object_name,
                },
                ExpiresIn=expiration
            )
        except Exception as e:
            logging.error(f"Error generating presigned URL: {e}")
            return None
        return response
    
    def generate_upload_url(self, object_name, expiration=3600):
        """
        Generates a presigned URL to upload a file to S3
        
        :param self: Client instance
        :param object_name: File name
        :param expiration: Expiration time in seconds
        """

        return self.generate_presigned_url(
            object_name,
            client_method='put_object',
            expiration=3600
        )
    