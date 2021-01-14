"""An interface to deal with AWS"""

from helpers.logger import Logger
from os.path import join, relpath
from os import walk
import boto3
from boto3.exceptions import S3UploadFailedError

logger = Logger.initial(__name__)


class AWS:
    """Will upload and download files to s3"""
    @staticmethod
    def download_from_s3(bucket_name: str, object_name: str, file_name: str):
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, object_name, file_name)

    @staticmethod
    def copy_to_s3(local_directory: str, bucket: str, destination: str):
        client = boto3.client('s3')

        try:
            client.delete_object(Bucket=bucket, Key=destination)
        except:
            logger.error(f"Unable to delete {destination}...")

        # enumerate local files recursively
        for root, dirs, files in walk(local_directory):

            for filename in files:

                local_path = join(root, filename)
                relative_path = relpath(local_path, local_directory)
                s3_path = join(destination, relative_path)

                logger.info(f"Searching {s3_path} in {bucket}")
                try:
                    client.head_object(Bucket=bucket, Key=s3_path)
                    logger.info(f"Path found on S3! Skipping {s3_path}...")
                except:
                    logger.info(f"Uploading {s3_path}...")
                    try:
                        client.upload_file(local_path, bucket, s3_path)
                    except S3UploadFailedError as e:
                        logger.error('Failed to copy to S3 bucket: {msg}'.format(msg=e))
                    except:
                        logger.error('Failed to copy to S3 bucket:')
