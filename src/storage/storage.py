import logging
import boto3
from botocore.exceptions import ClientError


class Storage:
    BUCKET_NAME = 'vardiety-recommendation-storage'

    @staticmethod
    def upload_file(
            file_path,
            object_name,
            self
    ):
        s3_client = boto3.client('s3')

        try:
            s3_client.upload_file(file_path, self.BUCKET_NAME, object_name)
        except ClientError as e:
            logging.error(e)
            return False

        return True

    @staticmethod
    def download_file(
            file_path,
            object_name,
            self
    ):
        s3_client = boto3.client('s3')

        try:
            s3_client.download_file(self.BUCKET_NAME, object_name, file_path)
        except ClientError as e:
            logging.error(e)
            return False

        return True
