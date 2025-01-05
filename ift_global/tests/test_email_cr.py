import pytest
from pydantic import ValidationError
import os
from ift_global.credentials.email_cr import MailConfig, EmailVariablesEnv

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv(EmailVariablesEnv.smtp_server.value, "smtp.example.com")
    monkeypatch.setenv(EmailVariablesEnv.smtp_port.value, "587")

def test_email_variables_env():
    assert EmailVariablesEnv.smtp_server.value == "EMAIL_SMTP_SERVER"
    assert EmailVariablesEnv.smtp_port.value == "EMAIL_SMTP_PORT"

def test_mail_config_with_all_fields():
    config = MailConfig(smtp_server="smtp.test.com", smtp_port="25")
    assert config.smtp_server == "smtp.test.com"
    assert config.smtp_port == "25"

def test_mail_config_with_env_vars(mock_env_vars):
    config = MailConfig(smtp_server=None, smtp_port=None)
    assert config.smtp_server == "smtp.example.com"
    assert config.smtp_port == "587"

def test_mail_config_missing_smtp_server(monkeypatch):
    monkeypatch.delenv(EmailVariablesEnv.smtp_server.value, raising=False)
    with pytest.raises(ValidationError):
        MailConfig()

def test_mail_config_missing_smtp_port(monkeypatch):
    monkeypatch.delenv(EmailVariablesEnv.smtp_port.value, raising=False)
    with pytest.raises(ValidationError):
        MailConfig()

def test_mail_config_partial_fields(mock_env_vars):
    config = MailConfig(smtp_server="custom.smtp.com", smtp_port=None)
    assert config.smtp_server == "custom.smtp.com"
    assert config.smtp_port == "587"

def test_mail_config_override_env_vars(mock_env_vars):
    config = MailConfig(smtp_server="override.smtp.com", smtp_port="465")
    assert config.smtp_server == "override.smtp.com"
    assert config.smtp_port == "465"

def test_mail_config_invalid_port():
    with pytest.raises(ValueError):
        MailConfig(smtp_server="smtp.test.com", smtp_port="invalid")

def test_mail_config_empty_string_fields():
    with pytest.raises(KeyError):
        MailConfig(smtp_server="", smtp_port="")

def test_mail_config_none_fields():
    with pytest.raises(ValidationError):
        MailConfig()



