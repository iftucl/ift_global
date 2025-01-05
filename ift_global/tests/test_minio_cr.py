import pytest
from pydantic import SecretStr, ValidationError
import os
from ift_global.credentials.minio_cr import MinioCredentials, MinioVariablesEnv

def test_minio_credentials_with_all_fields():
    creds = MinioCredentials(user="testuser", password="testpass", url="http://test.minio.com")
    assert creds.user == "testuser"
    assert creds.password.get_secret_value() == "testpass"
    assert creds.url == "http://test.minio.com"

def test_minio_credentials_with_env_vars(monkeypatch):
    monkeypatch.setenv(MinioVariablesEnv.user.value, "envuser")
    monkeypatch.setenv(MinioVariablesEnv.password.value, "envpass")
    monkeypatch.setenv(MinioVariablesEnv.url.value, "http://env.minio.com")

    creds = MinioCredentials(user=None, password=None, url=None)
    assert creds.user == "envuser"
    assert creds.password.get_secret_value() == "envpass"
    assert creds.url == "http://env.minio.com"

def test_minio_credentials_missing_user():
    with pytest.raises(ValidationError):
        MinioCredentials()

def test_minio_credentials_missing_password(monkeypatch):
    monkeypatch.setenv(MinioVariablesEnv.user.value, "testuser")
    monkeypatch.delenv(MinioVariablesEnv.password.value, raising=False)
    with pytest.raises(ValidationError):
        MinioCredentials()

def test_minio_credentials_missing_url():
    os.environ[MinioVariablesEnv.user.value] = "testuser"
    os.environ[MinioVariablesEnv.password.value] = "testpass"    
    os.unsetenv(MinioVariablesEnv.url.value)

    with pytest.raises(KeyError):
        MinioCredentials(user=None, password=None, url=None)

def test_minio_credentials_partial_fields(monkeypatch):
    os.environ[MinioVariablesEnv.password.value] = "envpass"
    os.environ[MinioVariablesEnv.url.value] = "http://env.minio.com"    
    creds = MinioCredentials(user="testuser", password=None, url=None)
    assert creds.user == "testuser"
    assert creds.password.get_secret_value() == "envpass"
    assert creds.url == "http://env.minio.com"

def test_minio_credentials_override_env_vars(monkeypatch):
    monkeypatch.setenv(MinioVariablesEnv.user.value, "envuser")
    monkeypatch.setenv(MinioVariablesEnv.password.value, "envpass")
    monkeypatch.setenv(MinioVariablesEnv.url.value, "http://env.minio.com")    

    creds = MinioCredentials(user="overrideuser",  password=None, url="http://override.minio.com")
    assert creds.user == "overrideuser"
    assert creds.password.get_secret_value() == "envpass"
    assert creds.url == "http://override.minio.com"

def test_minio_credentials_secret_str_password():
    creds = MinioCredentials(user="testuser", password="testpass", url="http://test.minio.com")
    assert isinstance(creds.password, SecretStr)
    assert creds.password.get_secret_value() == "testpass"
