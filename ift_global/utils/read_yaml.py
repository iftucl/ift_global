import os
import sys
from collections import UserDict

from ruamel import yaml
from ruamel.yaml.scanner import ScannerError


class ReadConfig(UserDict):
    """
    Read Config from YAML.

    This class loads configuration from a YAML file.

    :param env_type: The environment type to load from the config file
    :type env_type: str
    :param config_path: Path to the configuration file, defaults to './properties/conf.yaml'
    :type config_path: str, optional

    :ivar config_path: Path to the configuration file
    :ivar data: Program configuration (inherited from UserDict)

    :Example:
        >>> from ift_global import ReadConfig
        >>> config = ReadConfig('dev', './properties/conf.yaml')
    """

    def __init__(self, env_type: str, config_path: str = './properties/conf.yaml'):
        """
        Initialize the ReadConfig instance.

        :param env_type: The environment type to load from the config file
        :type env_type: str
        :param config_path: Path to the configuration file, defaults to './properties/conf.yaml'
        :type config_path: str, optional
        """
        self.config_path = os.path.expanduser(config_path)
        self.load(env_type)

    def load(self, env_type: str):
        """
        Load configuration from YAML file.

        This method reads the YAML file, extracts the configuration for the specified
        environment type, and stores it in the `data` attribute.

        :param env_type: The environment type to load from the config file
        :type env_type: str
        :raises ScannerError: If there's an error parsing the YAML file or if the file is not found
        """
        try:
            with open(os.path.expanduser(self.config_path), 'r') as f:
                try:
                    yaml_conn = yaml.YAML(typ='safe', pure=True)
                    cfg_data = yaml_conn.load(f)
                    self.data = cfg_data[env_type]
                except ScannerError as e:
                    raise ScannerError('Error parsing YAML config file {}: {}'.format(
                            e.problem_mark,
                            e.problem,
                        )
                    )
        except FileNotFoundError:
            raise ScannerError('YAML file not found in {}'.format(self.config_path))