from typing import Union

import pandas as pd

from ift_global.connectors.file_serialiser import abstraction_deserialiser, abstraction_serialiser
from ift_global.connectors.filesystem_registry import FileSystemRepository
from ift_global.connectors.minio_boto import BaseMinioConnection
from ift_global.utils.file_operations import check_path, extract_file_name


class MinioFileSystemRepo(BaseMinioConnection, FileSystemRepository):
    """
    Minio File Client.

    A repository class for interacting with Minio Object storage.

    This class extends the BaseMinioConnection to utilize its minio connection
    and session management based on boto3. It provides methods to execute specific tasks, including
    selecting, reading and writing files from minio.
    """

    def __init__(self, bucket_name, **kwargs):
        """
        Constructor method.

        :param str bucket_name: Name of a bucket in MinIO.
        :param str user: Username for MinIO. If empty, defaults to os.getenv('MINIO_USER').
        :param str password: Password for MinIO. If empty, defaults to os.getenv('MINIO_PASSWORD').
        :param str endpoint_url: URL for MinIO. If empty, defaults to os.getenv('MINIO_URL').
        """
        super().__init__(bucket_name,
                         user=kwargs.get('user'),
                         password=kwargs.get('password'),
                         endpoint_url=kwargs.get('endpoint_url'))


    def list_files(self, path : str, full_path : bool = True) -> list:
        """
        List all files in a given object folder.

        :param str path: a regular path including bucket location as
            /ift-bigdata-dev/bigdata/input/'.
        :param bool full_path: if set to will return full file path as
            /ift-bigdata-dev/bigdata/inputs/raw_20240710/Pathways.csv if false Pathways.csv only.

        :return: a list containing all files in a given path directory.
            An empty string is generated if directory is empty or does not exists.
        """
        norm_path = check_path(path, self.bucket_name)
        obj = self._client.list_objects(Bucket=self.bucket_name, Prefix=norm_path, Delimiter='/')
        if not obj.get('Contents'):
            return []
        all_files = [f"/{self.bucket_name}/{x.get('Key')}" for x in obj.get('Contents')]
        if not all_files:
            return []

        if full_path:
            all_files = [f"/{self.bucket_name}/{x.get('Key')}" for x in obj.get('Contents')]
            return all_files
        else:
            return [x.get('Key').replace(path, '') for x in obj.get('Contents')]

    def list_dirs(self, path : str, full_path : bool =False) -> list:
        """
        List all directories in a given object folder.

        :param str path: a regular path including bucket location as 
            /ift-bigdata-dev/bigdata/input/'.
        :param bool full_path: if set to will return full file path as
            /ift-bigdata-dev/bigdata/inputs/raw_20240710/
            if false raw_20240710 only.
        
        :return: a list containing all directories in a given path directory. 
                An empty string is generated if directory is empty or does not exists.
        """
        path = check_path(path, self.bucket_name)
        obj = self._client.list_objects(Bucket=self.bucket_name, Prefix=path, Delimiter='/')

        if not obj.get('CommonPrefixes') and not obj.get('Contents'):
            print(obj.get('CommonPrefixes')  is True)
            print(obj.get('Contents'))
            print('first check not passed')
            return list()

        if not obj.get('CommonPrefixes'):
            return path

        if obj.get('CommonPrefixes'):
            all_dirs = [f"/{self.bucket_name}/{x.get('Prefix')}" for x in obj.get('CommonPrefixes')]

        if not full_path:
            return all_dirs

        all_dirs = [x.split('/') for x in all_dirs]
        relative_dirs = []
        for i, z in enumerate(all_dirs, 0):
            *_, last_dir, empty_space = z
            relative_dirs.append(last_dir)
        return relative_dirs

    def dir_exists(self, path: str) -> bool:
        """
        Directory Exists.
        
        Check if a folder exists in a bucket.

        :param str path: path to check if exists, /ift-bigdata-dev/globals/test.csv.
        :return: bool `True` is dir exists else `False`.
        
        """
        all_dirs = self.list_dirs(path)
        if not all_dirs:
            return False
        return any([path in x for x in all_dirs])

    def file_exists(self, path : str) -> bool:
        """
        File Exists.

        check if file exists in locations.
        
        :param str path: path to check if exists, /ift-bigdata-dev/globals/test.csv.
        
        :return: bool `True` is dir exists else `False`

        """
        file_path, file_name = extract_file_name(file_path=path)
        norm_path = check_path(file_path, self.bucket_name)
        obj = self._client.list_objects(Bucket=self.bucket_name, Prefix=norm_path, Delimiter='/')

        if not obj.get('Contents'):
            return False
        all_files = [f"/{self.bucket_name}/{x.get('Key')}" for x in obj.get('Contents')]
        return f'/{self.bucket_name}/{norm_path}{file_name}' in all_files

    def read_file(
            self,
            path : str,
            file_type : str
        ) -> list:
        """
        Read Files.
        
        read csv, parquet or pickle from minio.

        :param path (str): a regular path including bucket location as /ift-bigdata-dev/input/'.
        
        :return: list of dictionaries.
        """
        file_path, file_name = extract_file_name(file_path=path)
        norm_path = check_path(file_path, self.bucket_name)

        if not self.file_exists(path=path):
            raise FileExistsError

        if file_type not in ('parquet', 'csv', 'pickle'):
            raise TypeError('file type not accepted, only parquet, csv and pickle file are allowed.')
        funct_des = abstraction_deserialiser(file_type)
        response = self._client.get_object(
            Bucket=self.bucket_name,
            Key=''.join((norm_path, file_name))
            )
        body_obj = response.get('Body')  #.read().decode('utf-8').splitlines(True)
        input_data = funct_des(body_obj)
        return input_data

    def write_file(self,
                   path : str,
                   output_data: Union[dict, list, pd.DataFrame],
                   file_type: str,
                   sep : str | None = ','):
        """
        Write files.

        write files parquet, csv or pickle to minio.

        :param str path: a regular path including bucket location as /ift-bigdata-dev/test/test.csv'.
        :param output_data: output data to be written in MinIO bucket.
        :type: Union[dict, list, pd.DataFrame]
        
        :return: minio response metadata JSON representation
        """
        norm_path = path.replace('/'+self.bucket_name+'/', '')
        serial_file = abstraction_serialiser(file_type)
        text_body = serial_file(output_data)
        response = self._client.put_object(
            Bucket=self.bucket_name,
            Key=norm_path,
            Body=text_body
            )
        return response



FileSystemRepository.register_repository('minio', MinioFileSystemRepo)
