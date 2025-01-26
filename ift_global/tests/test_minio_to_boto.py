import pytest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError, ParamValidationError, HTTPClientError
from ift_global.connectors.minio_boto import BaseMinioConnection  # replace with actual import
from ift_global.credentials.minio_cr import MinioVariablesEnv
import os


@pytest.fixture
def mock_boto3_client():
    os.environ[MinioVariablesEnv.user.value] = "testuser"
    os.environ[MinioVariablesEnv.password.value] = "envpass"
    os.environ[MinioVariablesEnv.url.value] = "http://env.minio.com"
    with patch('boto3.client') as mock:
        yield mock

def test_init_success(mock_boto3_client):
    mock_boto3_client.return_value.list_buckets.return_value = {
        'ResponseMetadata': {'HTTPStatusCode': 200},
        'Buckets': [{'Name': 'test-bucket'}]
    }
    
    conn = BaseMinioConnection('test-bucket')
    assert conn.bucket_name == 'test-bucket'
    assert conn._client == mock_boto3_client.return_value

def test_init_client_error(mock_boto3_client):
    mock_boto3_client.side_effect = ClientError({'Error': {'Code': 'TestException', 'Message': 'Test'}}, 'operation')
    
    with pytest.raises(ClientError):
        BaseMinioConnection('test-bucket')

def test_init_param_validation_error(mock_boto3_client):
    mock_boto3_client.side_effect = ParamValidationError(report='Invalid parameters')
    
    with pytest.raises(ParamValidationError):
        BaseMinioConnection('test-bucket')

def test_check_bucket_exists_success(mock_boto3_client):
    mock_boto3_client.return_value.list_buckets.return_value = {
        'ResponseMetadata': {'HTTPStatusCode': 200},
        'Buckets': [{'Name': 'test-bucket'}]
    }
    
    conn = BaseMinioConnection('test-bucket')
    # If no exception is raised, the test passes


def test_get_client(mock_boto3_client):
    mock_boto3_client.return_value.list_buckets.return_value = {
        'ResponseMetadata': {'HTTPStatusCode': 200},
        'Buckets': [{'Name': 'test-bucket'}]
    }
    
    conn = BaseMinioConnection('test-bucket')
    assert conn.get_client == mock_boto3_client.return_value

