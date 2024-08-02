import boto3
import pandas as pd
from io import StringIO
from botocore.exceptions import NoCredentialsError


class AWSClient:
    def __init__(self):
        pass

    def upload_data_to_aws(self, data, bucket, s3_file):
        # Convert the list to a DataFrame
        df = pd.DataFrame(data)

        # Use StringIO to save DataFrame to a CSV in memory
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False, header=False)

        # Get the CSV string from the buffer
        csv_content = csv_buffer.getvalue()

        # Initialize S3 client
        s3 = boto3.client('s3')

        try:
            # Upload CSV to S3
            s3.put_object(Bucket=bucket, Key=s3_file, Body=csv_content)
            return True
        except NoCredentialsError as nce:
            raise nce
        except Exception as e:
            raise e

    def upload_file_to_aws(self, local_file, bucket, s3_file):
        s3 = boto3.client('s3')

        try:
            s3.upload_file(local_file, bucket, s3_file)
            return True
        except FileNotFoundError as fnfe:
            raise fnfe
        except NoCredentialsError as nce:
            raise nce

    def download_file_from_aws(self, bucket, s3_file, local_file):
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
