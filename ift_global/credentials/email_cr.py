import os
from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, Field, SecretStr
from pydantic.functional_validators import field_validator


class EmailVariablesEnv(Enum):
    """
    Email Enum container to map environment variables 
    to python local denomination
    """

    smtp_server = 'EMAIL_SMTP_SERVER'
    smtp_port = 'EMAIL_SMTP_PORT'


class MailConfig(BaseModel):
    """
    Mail Config mapping.
    
    Maps internal to environment variables for email functionality

    :param smtp_server: loim smtp server address
    :type smtp_server: str
    :param smtp_port: smtp server port
    :type smtp_port: str
    """
    smtp_server : Optional[str] = Field(description="E-Mail smtp server address")
    smtp_port : Optional[str] = Field(description="E-Mail smtp server port")

    @field_validator("smtp_server", mode="after")
    @classmethod
    def check_smtp_server(cls, v: Any):
        if not v:
            try:
                return os.environ[EmailVariablesEnv.smtp_server.value]
            except KeyError:
                print(f'If smtp_server is not provided, please export to env variable {EmailVariablesEnv.smtp_server.value}')
                raise
        return v
    @field_validator("smtp_port", mode="after")
    @classmethod
    def check_smtp_port(cls, v: Any):
        if not v:
            try:
                return os.environ[EmailVariablesEnv.smtp_port.value]
            except KeyError:
                print(f'If smtp_port not provided, please export to env variable {EmailVariablesEnv.smtp_port.value}')
                raise
        try:
            _ = int(v)
            return v
        except ValueError as ve:
            print(f"smtp port needs to be a char string that contains numbers only: {ve}")
            raise
