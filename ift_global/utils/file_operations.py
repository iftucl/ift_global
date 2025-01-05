import platform
from pydantic import validate_call

@validate_call
def check_path(path: str, bucket_name: str, path_with_file : bool = False):
    """
    File Path Check.

    :param path: Utility to check weather a file paths is consistent with expectations
    :type path: str
    :param bucket_name: s3 name of bucket
    :type bucket_name: str
    :param path_with_file: if file path contains file name and file extension, defaults to False
    :type path_with_file: bool, optional
    :return: file path
    :rtype: str
    """
    if path[0:4].lower() == 's3:/':
        path = path[4:]

    if path.startswith('/'):
        path = path[1:]

    path = path.replace(bucket_name + '/', '')

    if path_with_file:
        return path

    if path.endswith('/'):
        return path

    return path + '/'

@validate_call
def extract_file_name(file_path: str):
    """
    Extract file name & path.

    From file path containing file name, extract file path and file.

    :param file_path: full file path with file name
    :type file_path: str
    :return: returns a tuple with file path and file name
    :rtype: tuple
    """
    *dirs_name, file_name = file_path.split('/')
    file_path = '/'.join(dirs_name)
    return file_path, file_name


def _os_is_windows() -> bool:
    """
    internal.

    :return bool True if os is windows, else False

    """
    return platform.system().lower() == 'windows'


def _os_is_unix() -> bool:
    """
    internal.

    :return: returns True if os is Unix-like else False
    :rtype: bool
    """
    return platform.system().lower() == 'linux'