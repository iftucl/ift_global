import csv
import pickle
from io import BytesIO, StringIO
from typing import Union

import pandas as pd
import pyarrow
from pyarrow import parquet


def check_data_structure(
          data_check: Union[list, dict, pd.DataFrame],
          accepted_instances : tuple = Union[list, dict, pd.DataFrame]
        ) -> bool:
    """
    Function to check data structure validity.

    :param data_check: checks data structure is list, pandas df or dictionary
    :type data_check: Union[list, dict, pd.DataFrame]
    :param accepted_instances: instances accepted, defaults to ["list", "dict", "pd.DataFrame"]
    :type accepted_instances: tuple, optional
    :raises TypeError: raises a type error is data provided is not instance of accepted instances
    :return: True
    :rtype: bool
    """
    if not isinstance(data_check, accepted_instances):
          raise TypeError("""Accepted data structures 
                          are only lists, dictionaries 
                          or pd.DataFrames""")
    return True


def serialise_csv(
          output_data: Union[list, dict, pd.DataFrame],
          sep = ','
        ) -> str:
    """
    Serialise python obj to csv like str.

    :param output_data: python object in form of
        dictionary with lists as column representation
        list of dictionaries where each dict is a row
        pd.DataFrame
        if user wants to create an empty file, pass an empty list or dict
    :type output_data: Union[list, dict, pd.DataFrame]
    :param sep: if csv is comma, tab, pipe ... separated
        defaults to ','
    :type sep: str, optional
    :return: output string representation of csv comma separated
    :rtype: str
    :Examples:
        >>> output_data =[{'a': 1, 'b': 2, 'c': 5},
        ...               {'a': 5, 'b': 6, 'c': 7},
        ...               {'a': 18, 'b': 9, 'c': 10}]
        >>> csv_repr = serialise_csv(output_data)
    """
    # check if df and convert to dict
    if isinstance(output_data, pd.DataFrame):
        output_data = output_data.to_dict('list')

    csv_buffer=StringIO()

    if isinstance(output_data, dict):
        if not output_data:
             return '' # allows user to write empty files
        # write dict assumes each key has values stored in list repr a column
        col_names = output_data.keys()
        data_rows = zip(*output_data.values())
        w = csv.writer(csv_buffer, delimiter=sep)
        # write headers
        w.writerow(col_names)
        # write rows
        w.writerows(data_rows)
        return csv_buffer.getvalue()

    if isinstance(output_data, list):
        if not output_data:
             return '' # allows user to write empty files
        col_names = output_data[0].keys()
        data_rows = output_data
        # write header
        w = csv.DictWriter(csv_buffer, list(col_names), delimiter=sep)
        w.writeheader()
        w.writerows(data_rows)

    return csv_buffer.getvalue()


def serialise_parquet(
          output_data: Union[list, dict, pd.DataFrame]
        ) -> str:
    """
    Serialise data to parquet.

    :param output_data: _description_
    :type output_data: Union[list, dict, pd.DataFrame]
    :raises TypeError: if data structure is not list, pdDataFrame or dict
    :return: serialized data
    :rtype: str
    :Examples:
        >>> output_data =[{'a': 1, 'b': 2, 'c': 5},
        ...               {'a': 5, 'b': 6, 'c': 7},
        ...               {'a': 18, 'b': 9, 'c': 10}] 
        >>> pqt_repr = serialise_parquet(output_data)

    """
    if not check_data_structure(output_data):
        raise TypeError('Cannot serialise to parquet file')


    if isinstance(output_data, pd.DataFrame):
        output_data = output_data.to_dict('list')
        output_table = pyarrow.Table.from_pydict(output_data)

    if isinstance(output_data, list):
            output_table = pyarrow.Table.from_pylist(output_data)

    if isinstance(output_data, dict):
            output_table = pyarrow.Table.from_pydict(output_data)

    writer = pyarrow.BufferOutputStream()
    parquet.write_table(output_table, writer)
    body = bytes(writer.getvalue())
    return body


def serialise_pickle(output_data: Union[list, dict, pd.DataFrame]) -> str:
    """
    Serialise python obj to pickle.

    :param output_data: list, dict or pd dataframe
    :type output_data: Union[list, dict, pd.DataFrame]
    :return: pickle obj
    :rtype: pickle
    """
    return pickle.dumps(output_data)


def deserialise_pickle(
          response_body : str,
          read_type : str = 'read' # TODO as for now defaults to read, maybe future can be improved
          ) -> Union[list, dict]:
    """Deserialise pickle file.

    :param response_body: body response from boto3
    :type response_body: str
    :param read_type: type of read operation (readlines or other, if not readline will default to read)
    :type read_type: str
    :return: a deserialized pickle
    :rtype: Union[list, dict]
    :Examples:
        >>> input_data = boto_client.get_object(Bucket='my_bucket',
        ...                                     Key='root/my_file.pickle')
        >>> pkl_obj = serialise_csv(input_data.get('Body'))
    """
    if read_type == 'readlines':
          str_input = response_body.readlines()
    else:
         str_input = response_body.read()

    deserial_object = pickle.loads(str_input)
    return deserial_object


def deserialise_csv(response_body : str) -> list:
    """
    Deserialise body to python obj.

    :param response_body: body response from boto3
    :type response_body: str
    :return: list of dict
    :rtype: list
    :Examples:
        >>> input_data = boto_client.get_object(
        ...                     Bucket='my_bucket',
        ...                     Key='root/my_file.csv'
        ...                     )
        >>> csv_obj = serialise_csv(
        ...                 input_data.get('Body')
        ...                 )
    """
    lines = response_body.read().decode('utf-8').splitlines(True)
    reader = csv.DictReader(lines)
    input_data = []
    for row in reader:
        input_data.append(row)
    return input_data


def deserialise_parquet(response_body : str) -> pyarrow.lib.Table:
    """
    Deserialise boto3 body response to python obj.

    :param response_body: body response from boto3 client get_object
    :type response_body: str
    :return: pyarrow table object can be conveerted to df as `.to_pandas`
    :rtype: pyarrow.lib.Table
    :Examples:
        >>> input_data = boto_client.get_object(
        ...                     Bucket='my_bucket',
        ...                     Key='root/my_file.parquet'
        ...                     )
        >>> pqt_obj = serialise_parquet(
        ...                     input_data.get('Body')
        ...                     )
        >>> pqt_obj.to_pandas()
        >>> pqt_obj.to_pydict()
        >>> pqt_obj.to_pylist()
    """
    body = BytesIO(response_body.read())
    pq_df = pd.read_parquet(body)
    return pq_df


def abstraction_serialiser(file_type : str) -> callable:
    """
    Abstraction function to select the serialiser.

    :param file_type: accepted csv, parquet or pickle
    :type file_type: str
    :return: a callable function as defined in:
        serialise_csv
        serialise_parquet
        serialise_pickle
    :rtype: callable
    """
    abstr_function = {
          "csv" : serialise_csv,
          "parquet" : serialise_parquet,
          "pickle" : serialise_pickle,
     }
    if file_type not in abstr_function.keys():
        raise ValueError(f"File type incorrect, {', '.join(abstr_function.keys())} are accepted")

    return abstr_function.get(file_type)


def abstraction_deserialiser(file_type : str) -> callable:
    """
    Abstraction function to select the deserialiser.

    :param file_type: accepted csv, parquet or pickle
    :type file_type: str
    :return: a callable function as defined in: 
        deserialise_csv
        deserialise_parquet
        deserialise_pickle
    :rtype: callable
    """
    abstr_function = {
          "csv" : deserialise_csv,
          "parquet" : deserialise_parquet,
          "pickle" : deserialise_pickle,
     }
    if file_type not in abstr_function.keys():
        raise ValueError(f"File type incorrect, {', '.join(abstr_function.keys())} are accepted")

    return abstr_function.get(file_type)
