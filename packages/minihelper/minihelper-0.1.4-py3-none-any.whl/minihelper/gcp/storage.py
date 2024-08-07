from io import BytesIO, StringIO
from loguru import logger
from google.cloud import storage
import google.auth
from typing import Union, BinaryIO

SCOPES = [
 "https://storage.googleapis.com/auth/storage"   
]

def _client() -> storage.Client:
    """Returns a storage cleint with default credentials

    Returns:
        storage.Client: a storage client with default credentials
    """

    creds, proj = google.auth.default(SCOPES)
    return storage.Client(project=proj, credentials=creds)

def upload_from_string(data: Union[StringIO, BytesIO], bucket: str, path: str, content_type: str = 'text/plain') -> None:
    """Upload file to storage bucket from string/bytes

    Args:
        data (Union[StringIO, BytesIO]): data to be uploaded
        bucket (str): destination bucket
        path (str): destination path
        content_type (str, optional): content type of data. Defaults to 'text/plain'.
    """

    logger.debug(f"Loading bucket: {bucket}")

    bucket = _client().bucket(bucket)
    bucket.blob(path).upload_from_string(data=data, content_type=content_type)
    
    logger.info(f"Upload file success: gs://{bucket}/{path}")


def upload_from_file(file: BinaryIO, bucket: str, path: str) -> None:
    """Upload file to storage bucket from file

    Args:
        file (BinaryIO): file object in binary format
        bucket (str): destination bucket
        path (str): destination_path
    """

    logger.debug(f"Loading bucket: {bucket}")

    bucket = _client().bucket(bucket)
    bucket.blob(path).upload_from_file(file)

    logger.info(f"Upload file success: gs://{bucket}/{path}")


def upload_from_filename(local_path: str, bucket: str, destination_path: str) -> None:
    """Upload file to storage bucket from file path

    Args:
        local_path (str): local file path
        bucket (str): destination bucket
        destination_path (str): destination file path
    """

    logger.debug(f"Loading bucket: {bucket}")

    bucket = _client().bucket(bucket)
    bucket.blob(destination_path).uplod_from_filename(local_path)

    logger.info(f"Upload file success: gs://{bucket}/{destination_path}")