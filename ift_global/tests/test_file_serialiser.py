from __future__ import annotations
import pandas as pd
import pytest
import pickle
import pyarrow

from ift_global.connectors.file_serialiser import (
    serialise_csv,
    serialise_pickle,
    serialise_parquet
)

@pytest.fixture
def output_string():
    return 'a,b,c\r\n1,2,3\r\n5,6,7\r\n8,9,10\r\n'

def test_list_serialise_csv_writer():
    output_list =[{'a': 1, 'b': 2, 'c': 3},{'a': 5, 'b': 6, 'c': 7}, {'a': 8, 'b': 9, 'c': 10}]
    assert serialise_csv(output_data=output_list) == 'a,b,c\r\n1,2,3\r\n5,6,7\r\n8,9,10\r\n'
    
def test_dict_serialise_csv_writer():
    output_dict = {'a': [1,5,8], 'b': [2,6,9], 'c': [3,7,10]}
    assert serialise_csv(output_data=output_dict) == 'a,b,c\r\n1,2,3\r\n5,6,7\r\n8,9,10\r\n'

def test_pd_serialise_csv_writer():
    output_df = pd.DataFrame({'a': [1,5,8], 'b': [2,6,9], 'c': [3,7,10]})
    assert serialise_csv(output_data=output_df) == 'a,b,c\r\n1,2,3\r\n5,6,7\r\n8,9,10\r\n'

def test_pd_serialise_pickle():
    output_df = pd.DataFrame({'a': [1,5,8], 'b': [2,6,9], 'c': [3,7,10]})
    assert serialise_pickle(output_data=output_df) == pickle.dumps(output_df)

def test_serialise_parquet_list():
    # Test case for list input
    input_data = [
        {'a': 1, 'b': 2, 'c': 5},
        {'a': 5, 'b': 6, 'c': 7},
        {'a': 18, 'b': 9, 'c': 10}
    ]
    
    result = serialise_parquet(input_data)
    
    # Check if the result is bytes
    assert isinstance(result, bytes)
    
    # Verify the content by reading it back
    buffer = pyarrow.py_buffer(result)
    table =  pyarrow.parquet.read_table(buffer)
    
    assert table.column_names == ['a', 'b', 'c']
    assert table.num_rows == 3
    assert table.to_pydict() == {
        'a': [1, 5, 18],
        'b': [2, 6, 9],
        'c': [5, 7, 10]
    }

def test_serialise_parquet_dataframe():
    # Test case for pandas DataFrame input
    input_data = pd.DataFrame({
        'x': [1, 2, 3],
        'y': ['a', 'b', 'c'],
        'z': [True, False, True]
    })
    
    result = serialise_parquet(input_data)
    
    # Check if the result is bytes
    assert isinstance(result, bytes)
    
    # Verify the content by reading it back
    buffer = pyarrow.py_buffer(result)
    table =  pyarrow.parquet.read_table(buffer)
    
    assert table.column_names == ['x', 'y', 'z']
    assert table.num_rows == 3
    assert table.to_pydict() == {
        'x': [1, 2, 3],
        'y': ['a', 'b', 'c'],
        'z': [True, False, True]
    }
