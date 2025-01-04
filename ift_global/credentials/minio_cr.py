from pydantic import BaseModel, Field, SecretStr
from pydantic.functional_validators import field_validator
from enum import Enum
from typing import Optional, Any
import os

class MinioVariablesEnv(Enum):
    """
    Enumerate env variable for Minio
    """
    user = "MINIO_USER"
    password = "MINIO_PASSWORD"
    url = "MINIO_URL"


class MinioCredentials(BaseModel):
    """
    Credential Minio Config Mapping

    Map internal to environment variables for Minio

    """
    user : Optional[str] = Field(..., default=None, description="Username for Minio auth")
    password : Optional[SecretStr] = Field(..., default=None, description="Password for Minio auth")
    url : Optional[str] = Field(..., default=None, description="Minio url address")
    
    @field_validator("user", mode="after")
    @classmethod
    def check_user(cls, v: Any):
        if not v:
            try:
                return os.environ[MinioVariablesEnv.user.value]
            except KeyError:
                print(f'If user is not provided, please export to environment variable {MinioVariablesEnv.user.value}')
                raise
    @field_validator("password", mode="after")
    @classmethod
    def check_pwd(cls, v: Any):
        if not v:
            try:
                return os.environ[MinioVariablesEnv.password.value]
            except KeyError:
                print(f'If user is not provided, please export to environment variable {MinioVariablesEnv.password.value}')
                raise
    @field_validator("url", mode="after")
    @classmethod
    def check_url(cls, v: Any):
        if not v:
            try:
                return os.environ[MinioVariablesEnv.url.value]
            except KeyError:
                print(f'If user is not provided, please export to environment variable {MinioVariablesEnv.url.value}')
                raise

MinioCredentials()