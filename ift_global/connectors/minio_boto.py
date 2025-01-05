from typing import Optional

import boto3
from botocore.exceptions import ClientError, HTTPClientError, ParamValidationError

from ift_global.credentials.minio_cr import MinioCredentials


class BaseMinioConnection:
    """
    Base Minio Client Connection.

    This class provides an abstraction for Minio Client based on boto3.

    :param bucket_name: Name of a bucket in Minio
    :type bucket_name: str
    :param user: Username for Minio, defaults to os.getenv('MINIO_USER')
    :type user: str, optional
    :param password: Password for Minio, defaults to os.getenv('MINIO_PASSWORD')
    :type password: str, optional
    :param endpoint_url: URL for Minio, defaults to os.getenv('MINIO_URL')
    :type endpoint_url: str, optional

    :ivar bucket_name: Name of the Minio bucket
    :ivar _client: Boto3 S3 client instance
    :vartype _client: boto3.client

    :raises ClientError: If there's an error connecting to the Minio server
    :raises ParamValidationError: If the provided parameters are incorrect or the bucket doesn't exist

    :Example:
        >>> minio_conn = BaseMinioConnection(bucket_name='loim-dev-sirs')
        >>> client = minio_conn.get_client
        >>> buckets = client.list_buckets()
    """

    def __init__(self, bucket_name: str, user: Optional[str] = None, password: Optional[str] = None, endpoint_url: Optional[str] = None):
        self._credentials = MinioCredentials(user=user,
                                             password=password,
                                             url=endpoint_url)
        self.bucket_name = bucket_name
        self._client = self._get_client()
        self._check_bucket_exists()

    def _get_client(self):
        """
        Establish connection to Minio server.

        :return: Boto3 S3 client instance
        :rtype: boto3.client
        :raises ClientError: If there's an error connecting to the Minio server
        :raises ParamValidationError: If the provided parameters are incorrect
        """
        try:
            minio_client = boto3.client('s3',
                    aws_access_key_id=self._credentials.user,
                    aws_secret_access_key=self._credentials.password,
                    endpoint_url=self._credentials.url)
            return minio_client
        except ClientError as error:
            print(f"Client could not establish connection: {error}")
            raise
        except ParamValidationError as error:
            print('The parameters you provided are incorrect: {}'.format(error))
            raise

    def _check_bucket_exists(self):
        """
        Check if the specified bucket exists.

        :raises HTTPClientError: If the Minio client couldn't connect to the server
        :raises ParamValidationError: If the specified bucket doesn't exist
        """
        all_buckets = self._client.list_buckets()
        http_status = all_buckets.get('ResponseMetadata', {}).get('HTTPStatusCode')
        if http_status != 200:
            raise HTTPClientError(f'Minio client could not connect to server with error {http_status}')
        bucket_names = [x.get('Name') for x in all_buckets.get('Buckets', [])]
        if self.bucket_name not in bucket_names:
            raise ParamValidationError('Bucket provided does not exist')

    @property
    def get_client(self):
        """
        Get the Minio Client.

        :return: Boto3 S3 client instance
        :rtype: boto3.client

        :Example:
            >>> minio_client = BaseMinioConnection(bucket_name='loim-dev-sirs')
            >>> buckets = minio_client.get_client.list_buckets()
        """
        return self._client
