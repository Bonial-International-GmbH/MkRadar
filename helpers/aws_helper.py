"""An interface to deal with AWS"""

import mimetypes
from helpers.logger import Logger
from os.path import join, relpath
from os import walk
from pathlib import Path
import boto3
from botocore.errorfactory import ClientError
from boto3.exceptions import S3UploadFailedError

logger = Logger.initial(__name__)


class AWS:
    """Will upload and download files to s3"""

    @staticmethod
    def download_mkradar(s3_bucket_name: str, s3_bucket_destination: str, website_path: str):
        bucket_name = s3_bucket_name
        bucket_destination = join(s3_bucket_destination, "Mkradar.db")
        local_file = join(website_path, "Mkradar.db")
        logger.info(f"Downloading {bucket_destination} from {bucket_name} to {local_file}")
        Path(website_path).mkdir(parents=True, exist_ok=True)
        try:
            AWS.download_from_s3(bucket_name, bucket_destination, local_file)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def download_from_s3(bucket_name: str, object_name: str, local_file_path: str):
        s3 = boto3.client('s3')
        try:
            s3.head_object(Bucket=bucket_name, Key=object_name)
        except ClientError:
            logger.warning(f"Unable to download Mkradar.db")
        else:
            s3.download_file(bucket_name, object_name, local_file_path)

    @staticmethod
    def clean_s3_bucket(bucket_name: str):
        s3 = boto3.resource('s3')
        try:
            bucket = s3.Bucket(bucket_name)
            bucket.objects.all().delete()
        except Exception as e:
            logger.error(e)
            logger.error(f"Unable to delete {bucket_name}...")

    @staticmethod
    def copy_to_s3(local_directory: str, bucket: str, destination: str):
        client = boto3.client('s3')

        # enumerate local files recursively
        for root, dirs, files in walk(local_directory):

            for filename in files:

                local_path = join(root, filename)
                relative_path = relpath(local_path, local_directory)
                s3_path = join(destination, relative_path)
                mimetype, _ = mimetypes.guess_type(local_path)
                if mimetype is None:
                    mimetype = "binary/octet-stream"

                logger.info(f"Searching {s3_path} in {bucket}")
                try:
                    client.head_object(Bucket=bucket, Key=s3_path)
                    logger.info(f"Path found on S3! Skipping {s3_path}...")
                except:
                    logger.info(f"Uploading {s3_path}...")
                    try:
                        client.upload_file(
                            Filename=local_path,
                            Bucket=bucket,
                            Key=s3_path,
                            ExtraArgs={
                               "ContentType": mimetype
                            })
                    except S3UploadFailedError as e:
                        logger.error('Failed to copy to S3 bucket: {msg}'.format(msg=e))
                    except Exception as e:
                        logger.error(e)
                        logger.error('Failed to copy to S3 bucket:')
