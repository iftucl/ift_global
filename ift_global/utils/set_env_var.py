import os
from pydantic import validate_call
from typing import Literal, List
from dotenv import load_dotenv
from pathlib import Path

@validate_call
def set_env_variables(env_variables: List[str],
                      env_type: Literal['local', 'dev', 'preprod', 'prod'],
                      env_file: bool = False, 
                      env_file_path: str = './') -> bool:
    """
    Set environment variables based on the provided list and environment type.

    :param env_variables: A list of environment variable names to set.
    :type env_variables: List[str]
    :param env_type: The type of environment (local, dev, preprod, prod).
    :type env_type: Literal['local', 'dev', 'preprod', 'prod']
    :param env_file: Whether to load environment variables from a.env file.
    :type env_file: bool
    :param env_file_path: The path to the directory containing the.env files.
    :type env_file_path: str
    :return: True if all environment variables are set successfully, False otherwise.
    :rtype: bool
    :raises ValueError: If env_type is not one of the allowed values.
    :raises FileNotFoundError: If the specified.env file does not exist when env_file is True.

    .. note::
        This function first loads environment variables from a.env file if specified, then sets the provided environment variables based on the given environment type.

    .. seealso::
        :func:`var_from_env_file`
        :func:`gather_export_env_variables`
    """
    if env_file:
        var_from_env_file(dotenv_path=env_file_path, env_type=env_type)
    for env_var in env_variables:
        gather_export_env_variables(var_name=env_var, env=env_type)
    return True


def var_from_env_file(dotenv_path: str, env_type: Literal['local', 'dev', 'preprod', 'prod']) -> None:
    """
    Load environment variables from a .env file based on the specified environment type.

    :param dotenv_path: The path to the directory containing the.env files.
    :param env_type: The type of environment (local, dev, preprod, prod).
    :raises FileNotFoundError: If the specified.env file does not exist.
    :raises ValueError: If the env_type is not one of the allowed values.
    """

    # Validate env_type
    allowed_env_types = ['local', 'dev', 'preprod', 'prod']
    if env_type not in allowed_env_types:
        raise ValueError(f"Invalid env_type. Must be one of {allowed_env_types}")

    # Construct the full path to the.env file
    dotenv_file = Path(dotenv_path) / f".env.{env_type}"

    # Check if the file exists
    if not dotenv_file.exists():
        raise FileNotFoundError(f".env.{env_type} file could not be located at {dotenv_file}")

    try:
        # Load the.env file
        load_dotenv(dotenv_path=str(dotenv_file))
    except Exception as e:
        raise RuntimeError(f"Failed to load {dotenv_file}: {e}")


@validate_call
def gather_export_env_variables(var_name: str, env: Literal['local', 'dev', 'preprod', 'prod']) -> bool:
    """
    Gather and export environment variables based on the provided environment.

    :param var_name: The name of the environment variable.
    :type var_name: str
    :param env: The environment to check (local, dev, preprod, prod).
    :type env: Literal['local', 'dev', 'preprod', 'prod']
    :return: True if the environment variable is set, False otherwise.
    :rtype: bool
    :raises ValueError: If env is not one of the allowed values.

    :example:
        >>> gather_export_env_variables('MY_VAR', 'dev')
        True
    """
    # Check if default env variable is set
    if var_name in os.environ:
        return True
    # If not set, check if specific env variable is set
    var_name_env = f"{var_name}_{env.upper()}"
    if var_name_env in os.environ:
        os.environ[var_name] = os.environ[var_name_env]
        return True
    # If neither is set, return False
    return False