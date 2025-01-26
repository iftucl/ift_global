.. _miniorw-howto:

Minio Read/Write: How to?
=========================


This section shows how to read and write from Minio.

File types accepted to read/write are csv, parquet, avro or pickle.

To import the MinioFileSystemRepo:

.. ipython:: python
    :okexcept:

    from ift_global import MinioFileSystemRepo


And instantiate the class as (assuming you have all environment variables set):

.. ipython:: python
    :okexcept:
    :verbatim:

    minio_client = MinioFileSystemRepo(bucket_name='iftbigdata')


else

.. ipython:: python
    :okexcept:
    :verbatim:

    minio_client = MinioFileSystemRepo(bucket_name='iftbigdata', user='my_user', password='my_password', endpoint_url='http://localhost:9000')


Read & Write CSV
----------------

As an example, you can read csv files using MinioFileSystemRepo:

.. ipython:: python
    :okexcept:
    :verbatim:

    minio_client.read_file(file_path="/my_file/path/to/file.csv", file_type="csv")


or write:

.. ipython:: python
    :okexcept:
    :verbatim:

    import pandas as pd

    large_df = pd.DataFrame({
        'a': range(10000),
        'b': range(0, 20000, 2),
        'c': range(0, 30000, 3)
    })

    minio_client.write_file(file_path="/my_file/path/to/file.csv", output_data=large_df, file_type="csv")


