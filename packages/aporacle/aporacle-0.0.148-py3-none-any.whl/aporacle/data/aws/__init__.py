import boto3
from botocore.exceptions import NoCredentialsError


class AWSClient:
    def __init__(self):
        pass

    def upload_to_aws(self, local_file, bucket, s3_file):
        s3 = boto3.client('s3')

        try:
            s3.upload_file(local_file, bucket, s3_file)
            return True
        except FileNotFoundError as fnfe:
            raise fnfe
        except NoCredentialsError as nce:
            raise nce

    def download_from_aws(self, bucket, s3_file, local_file):
        s3 = boto3.client('s3')

        try:
            s3.download_file(bucket, s3_file, local_file)
            return True
        except FileNotFoundError as fnfe:
            raise fnfe
        except NoCredentialsError as nce:
            raise nce
        except Exception as e:
            raise e
