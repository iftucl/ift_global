from abc import ABC, abstractmethod


class FileSystemRepository(ABC):
    """
    File System Repository.

    Abstract base class defining the interface for a S3 object repository.

    This class serves as a template for concrete repository implementations,
    providing a standardized set of methods for interacting with a S3 object repository.
    Concrete implementations of this class should provide specific behavior for
    each abstract method.

    :cvar _repositories: A dictionary to store registered repository classes
    :type _repositories: dict

    :Example:
        >>> class ConcreteRepository(FileSystemRepository):
        ...     def __init__(self, **kwargs):
        ...         # Implementation
        ...     def list_files(self, path, full_path=True):
        ...         # Implementation
        ...     # ... other method implementations ...
        >>> FileSystemRepository.register_repository('concrete', ConcreteRepository)
        >>> repo = FileSystemRepository.repository_route('concrete', 'my-bucket', 'user', 'password', 'http://endpoint')
    """

    _repositories = {}

    @classmethod
    def register_repository(cls, driver_name, repository_cls):
        """
        Register a repository class for a specific driver.

        :param driver_name: The name of the driver
        :type driver_name: str
        :param repository_cls: The repository class to register
        :type repository_cls: type
        """
        cls._repositories[driver_name.lower()] = repository_cls

    @abstractmethod
    def __init__(self, **kwargs):
        """
        Initialize the repository with the given keyword arguments.

        This method should be implemented by concrete subclasses to set up
        the repository, such as establishing database connections.

        :param kwargs: Arbitrary keyword arguments necessary for the repository initialization
        """
        pass

    @abstractmethod
    def list_files(self, path: str, full_path: bool = True):
        """
        List files in the specified path.

        :param path: The path to list files from
        :type path: str
        :param full_path: Whether to return full paths or just file names, defaults to True
        :type full_path: bool, optional
        :return: A list of file names or paths
        :rtype: list
        """
        pass

    @abstractmethod
    def list_dirs(self, path: str, full_path: bool =False):
        """
        List directories in the specified path.

        :param path: The path to list directories from
        :type path: str
        :param full_path: Whether to return full paths or just directory names, defaults to False
        :type full_path: bool, optional
        :return: A list of directory names or paths
        :rtype: list
        """
        pass

    @abstractmethod
    def dir_exists(self, path):
        """
        Check if a directory exists.

        :param path: The path to check
        :type path: str
        :return: True if the directory exists, False otherwise
        :rtype: bool
        """
        pass

    @abstractmethod
    def read_file(self, file_path):
        """
        Read the contents of a file.

        :param file_path: The path to the file to read
        :type file_path: str
        :return: The contents of the file
        :rtype: str or bytes
        """
        pass

    @abstractmethod
    def upload_file(self, remote_file_path, local_file_path):
        """
        Upload file to Minio.

        :param remote_file_path: The path to the file to upload
        :type file_path: str
        :param local_file_path: The path on the local file system for the file to upload
        :type file_path: str
        """
        pass

    @abstractmethod
    def download_file(self, remote_file_path, local_file_path):
        """
        Download file to Minio.

        :param remote_file_path: The path to the file to download
        :type file_path: str
        :param local_file_path: The path on the local file system where the file will be downloaded
        :type file_path: str
        """
        pass


    @abstractmethod
    def write_file(self, file_path, file_type):
        """
        Write contents to a file.

        :param file_path: The path to the file to write
        :type file_path: str
        :param file_type: The type of file to write
        :type file_type: str
        """
        pass

    @classmethod
    def repository_route(cls, driver, bucket_name, user, password, endpoint_url):
        """
        Repository Routing.

        Create and return an instance of the appropriate
        repository based on the driver.

        :param driver: The name of the driver to use
        :type driver: str
        :param bucket_name: The name of the S3 bucket
        :type bucket_name: str
        :param user: The username for authentication
        :type user: str
        :param password: The password for authentication
        :type password: str
        :param endpoint_url: The URL of the S3 endpoint
        :type endpoint_url: str
        :return: An instance of the appropriate repository
        :rtype: FileSystemRepository
        :raises ValueError: If no repository is available for the specified driver
        """
        repository_cls = cls._repositories.get(driver.lower())
        if repository_cls:
            return repository_cls(bucket_name, user, password, endpoint_url)
        else:
            raise ValueError(f"No repository available for driver : {driver}")
