import pytest
import os
import yaml
from ruamel.yaml.scanner import ScannerError
from ift_global.utils.read_yaml import ReadConfig

@pytest.fixture
def valid_yaml_file(tmp_path):
    """Fixture to create a valid YAML configuration file."""
    config_data = {
        'dev': {
            'setting1': 'value1',
            'setting2': 'value2'
        },
        'prod': {
            'setting1': 'prod_value1',
            'setting2': 'prod_value2'
        }
    }
    config_file = tmp_path / "conf.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(config_data, f)
    return str(config_file)

@pytest.fixture
def invalid_yaml_file(tmp_path):
    """Fixture to create an invalid YAML configuration file."""
    invalid_content = """
    dev:
      setting1: value1
      setting2: value2
    prod:
      setting1: prod_value1
      setting2: prod_value2
      setting3: value3:  # Invalid syntax
    """
    config_file = tmp_path / "invalid_conf.yaml"
    with open(config_file, 'w') as f:
        f.write(invalid_content)
    return str(config_file)

def test_load_valid_config(valid_yaml_file):
    """Test loading a valid YAML configuration."""
    config = ReadConfig('dev', valid_yaml_file)
    assert config.data['setting1'] == 'value1'
    assert config.data['setting2'] == 'value2'

def test_load_invalid_yaml(invalid_yaml_file):
    """Test loading an invalid YAML configuration raises a ScannerError."""
    with pytest.raises(ScannerError) as excinfo:
        ReadConfig('dev', invalid_yaml_file)
    
    assert "Error parsing YAML config file" in str(excinfo.value)

def test_file_not_found():
    """Test that a FileNotFoundError raises a ScannerError."""
    with pytest.raises(ScannerError) as excinfo:
        ReadConfig('dev', './non_existent_path/conf.yaml')
    
    assert "YAML file not found in" in str(excinfo.value)

def test_load_non_existent_env_type(valid_yaml_file):
    """Test loading a non-existent environment type raises KeyError."""    
    # Check if the data attribute is empty or raises KeyError
    with pytest.raises(KeyError):
        config = ReadConfig('non_existent_env', valid_yaml_file)
        _ = config.data['setting1']  # This should raise KeyError