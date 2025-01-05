import os
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, SecretStr
from pydantic.functional_validators import field_validator


class MinioVariablesEnv(Enum):
    """
    Enumerates environment variables for MinIO.

    This enum class defines the names of environment variables used for MinIO configuration.

    :cvar str user: Environment variable name for MinIO username ('MINIO_USER').
    :cvar str password: Environment variable name for MinIO password ('MINIO_PASSWORD').
    :cvar str url: Environment variable name for MinIO URL ('MINIO_URL').

    Usage:
        >>> MinioVariablesEnv.user.value
        'MINIO_USER'
        >>> MinioVariablesEnv.password.value
        'MINIO_PASSWORD'
        >>> MinioVariablesEnv.url.value
        'MINIO_URL'
    """
    user = "MINIO_USER"
    password = "MINIO_PASSWORD"
    url = "MINIO_URL"


class MinioCredentials(BaseModel):
    """
    Credential Minio Config Mapping.

    This class maps internal fields to environment variables for MinIO configuration.
    It inherits from BaseModel and uses Pydantic for field validation.

    :param str user: Username for MinIO authentication. Defaults to None.
    :param SecretStr password: Password for MinIO authentication. Defaults to None.
    :param str url: MinIO server URL. Defaults to None.

    If any of the fields are not provided, the class attempts to fetch them from
    environment variables defined in the MinioVariablesEnv enum.

    :raises ValueError: If a required field is not provided and not found in environment variables.

    Usage:
        >>> creds = MinioCredentials(user="myuser", password="mypassword", url="http://minio.example.com")
        >>> creds = MinioCredentials()  # Will attempt to use environment variables

    .. note::
        The password is stored as a SecretStr for enhanced security.

    .. warning::
        Ensure that the required environment variables are set if not providing values directly.
    """
    user: str | None = Field(description="Username for Minio auth")
    password: SecretStr | None = Field(description="Password for Minio auth")
    url: str | None = Field(description="Minio url address")

    @field_validator("user", mode="after")
    @classmethod
    def check_user(cls, v: Any):
        print("check user")
        if not v:
            try:
                return os.environ[MinioVariablesEnv.user.value]
            except KeyError:
                print(f'If user is not provided, please export to env variable {MinioVariablesEnv.user.value}')
                raise
        return v
    @field_validator("password", mode="after")
    @classmethod
    def check_pwd(cls, v: Any):
        if not v:
            try:
                return SecretStr(os.environ[MinioVariablesEnv.password.value])
            except KeyError:
                print(f'If user not provided, please export to env variable {MinioVariablesEnv.password.value}')
                raise
        return v
    @field_validator("url", mode="before")
    @classmethod
    def check_url(cls, v: Any):
        if not v:
            try:
                return os.environ[MinioVariablesEnv.url.value]
            except KeyError:
                print(f'If user is not provided, please export to environment variable {MinioVariablesEnv.url.value}')
                raise
        return v 
