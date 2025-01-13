from __future__ import annotations

import pytest
import os
from pydantic import ValidationError

from ift_global.utils.set_env_var import var_from_env_file, gather_export_env_variables

def test_gather_export_env_variables_default_set():
    os.environ['MY_VAR'] = 'default_value'
    assert gather_export_env_variables('MY_VAR', 'dev') is True
    del os.environ['MY_VAR']

def test_gather_export_env_variables_specific_set():
    os.environ['MY_VAR_DEV'] = 'dev_value'
    assert gather_export_env_variables('MY_VAR', 'dev') is True
    assert os.environ['MY_VAR'] == 'dev_value'
    del os.environ['MY_VAR_DEV']
    del os.environ['MY_VAR']

def test_gather_export_env_variables_neither_set():
    assert gather_export_env_variables('MY_VAR', 'dev') is False

def test_gather_export_env_variables_invalid_env():
    with pytest.raises(ValidationError):
        gather_export_env_variables('MY_VAR', 'invalid_env')

# Test case for valid env_type
def test_var_from_env_file_valid_env_type(tmp_path):
    # Create a dummy env file
    env_file_path = tmp_path / ".env.local"
    env_file_path.write_text("KEY=VALUE")
    
    var_from_env_file(str(tmp_path), "local")
    assert os.getenv("KEY") == "VALUE"

# Test case for invalid env_type
def test_var_from_env_file_invalid_env_type(tmp_path):
    with pytest.raises(ValueError):
        var_from_env_file(str(tmp_path), "invalid")

# Test case for non-existent env file
def test_var_from_env_file_non_existent_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        var_from_env_file(str(tmp_path), "local")

# Parametrized test case for different env types
@pytest.mark.parametrize("env_type", ["local", "dev", "preprod", "prod"])
def test_var_from_env_file_different_env_types(tmp_path, env_type):
    # Create a dummy env file
    env_file_path = tmp_path / f".env.{env_type}"
    env_file_path.write_text("KEY=VALUE")
    
    var_from_env_file(str(tmp_path), env_type)
    assert os.getenv("KEY") == "VALUE"