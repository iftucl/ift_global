import pytest
from ift_global.connectors.filesystem_registry import FileSystemRepository  # Replace with your actual module name


class DummyFileSystemRepository(FileSystemRepository):
    """
    Dummy implementation of FileSystemRepository for testing purposes.
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def list_files(self, path: str, full_path: bool = True):
        return ["file1.txt", "file2.txt"] if full_path else ["file1", "file2"]

    def list_dirs(self, path: str, full_path: bool = False):
        return ["dir1", "dir2"] if not full_path else [f"{path}/dir1", f"{path}/dir2"]

    def dir_exists(self, path):
        return path == "/existing_directory"

    def read_file(self, file_path):
        return "file content"

    def upload_file(self, remote_file_path, local_file_path):
        return f"Uploaded {local_file_path} to {remote_file_path}"

    def download_file(self, remote_file_path, local_file_path):
        return f"Downloaded {remote_file_path} to {local_file_path}"

    def write_file(self, file_path, file_type):
        return f"Written file at {file_path} with type {file_type}"


def test_abstract_class_instantiation():
    """
    Test that instantiating FileSystemRepository directly raises a TypeError.
    """
    with pytest.raises(TypeError):
        FileSystemRepository()


def test_dummy_repository_instantiation():
    """
    Test that a concrete implementation of FileSystemRepository can be instantiated.
    """
    repo = DummyFileSystemRepository(param="test")
    assert isinstance(repo, FileSystemRepository)
    assert repo.kwargs["param"] == "test"


def test_list_files():
    """
    Test the list_files method in the dummy repository.
    """
    repo = DummyFileSystemRepository()
    files = repo.list_files("/path", full_path=True)
    assert files == ["file1.txt", "file2.txt"]

    files = repo.list_files("/path", full_path=False)
    assert files == ["file1", "file2"]


def test_list_dirs():
    """
    Test the list_dirs method in the dummy repository.
    """
    repo = DummyFileSystemRepository()
    dirs = repo.list_dirs("/path", full_path=True)
    assert dirs == ["/path/dir1", "/path/dir2"]

    dirs = repo.list_dirs("/path", full_path=False)
    assert dirs == ["dir1", "dir2"]


def test_dir_exists():
    """
    Test the dir_exists method in the dummy repository.
    """
    repo = DummyFileSystemRepository()
    assert repo.dir_exists("/existing_directory") is True
    assert repo.dir_exists("/non_existing_directory") is False


def test_read_file():
    """
    Test the read_file method in the dummy repository.
    """
    repo = DummyFileSystemRepository()
    content = repo.read_file("/path/to/file.txt")
    assert content == "file content"


def test_upload_file():
    """
    Test the upload_file method in the dummy repository.
    """
    repo = DummyFileSystemRepository()
    result = repo.upload_file("remote/path/file.txt", "/local/path/file.txt")
    assert result == "Uploaded /local/path/file.txt to remote/path/file.txt"


def test_download_file():
    """
    Test the download_file method in the dummy repository.
    """
    repo = DummyFileSystemRepository()
    result = repo.download_file("remote/path/file.txt", "/local/path/file.txt")
    assert result == "Downloaded remote/path/file.txt to /local/path/file.txt"


def test_write_file():
    """
    Test the write_file method in the dummy repository.
    """
    repo = DummyFileSystemRepository()
    result = repo.write_file("/path/to/file.txt", "text")
    assert result == "Written file at /path/to/file.txt with type text"
