from __future__ import annotations
import avro.errors
import pandas as pd
import pytest
import pickle
import pyarrow
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import io
import json

from ift_global.connectors.file_serialiser import (
    serialise_csv,
    serialise_pickle,
    serialise_parquet,
    serialise_avro,
    deserialise_avro,
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

@pytest.fixture
def sample_schema():
    return avro.schema.parse(json.dumps({
        "type": "record",
        "name": "TestRecord",
        "fields": [
            {"name": "a", "type": "int"},
            {"name": "b", "type": "int"},
            {"name": "c", "type": "int"}
        ]
    }))


@pytest.fixture
def sample_dataframe(output_string):
    return pd.read_csv(io.StringIO(output_string))

def test_serialise_avro_with_dataframe(sample_dataframe, sample_schema):
    result = serialise_avro(sample_dataframe, sample_schema)
    assert isinstance(result, bytes)
    
    reader = DataFileReader(io.BytesIO(result), DatumReader())
    deserialized_data = list(reader)
    assert deserialized_data == sample_dataframe.to_dict('records')

def test_serialise_avro_with_list(sample_dataframe, sample_schema):
    data = sample_dataframe.to_dict('records')
    result = serialise_avro(data, sample_schema)
    assert isinstance(result, bytes)
    
    reader = DataFileReader(io.BytesIO(result), DatumReader())
    deserialized_data = list(reader)
    assert deserialized_data == data

def test_serialise_avro_with_dict(sample_dataframe, sample_schema):
    data = sample_dataframe.iloc[0].to_dict()
    result = serialise_avro(data, sample_schema)
    assert isinstance(result, bytes)
    
    reader = DataFileReader(io.BytesIO(result), DatumReader())
    deserialized_data = list(reader)
    assert deserialized_data == [data]

def test_serialise_avro_with_invalid_input(sample_schema):
    with pytest.raises(TypeError):
        serialise_avro("invalid input", sample_schema)

def test_serialise_avro_with_mismatched_schema(sample_dataframe, sample_schema):
    invalid_data = sample_dataframe.rename(columns={'c': 'd'}).to_dict('records')
    with pytest.raises(avro.errors.AvroTypeException):
        serialise_avro(invalid_data, sample_schema)

def test_serialise_avro_with_empty_dataframe(sample_schema):
    empty_df = pd.DataFrame(columns=['a', 'b', 'c'])
    result = serialise_avro(empty_df, sample_schema)
    assert isinstance(result, bytes)
    
    reader = DataFileReader(io.BytesIO(result), DatumReader())
    deserialized_data = list(reader)
    assert deserialized_data == []

def test_serialise_avro_with_large_dataset(sample_schema):
    large_data = pd.DataFrame({
        'a': range(10000),
        'b': range(0, 20000, 2),
        'c': range(0, 30000, 3)
    })
    result = serialise_avro(large_data, sample_schema)
    assert isinstance(result, bytes)
    
    reader = DataFileReader(io.BytesIO(result), DatumReader())
    deserialized_data = list(reader)
    assert deserialized_data == large_data.to_dict('records')



@pytest.fixture
def sample_avro_data(output_string, sample_schema):
    df = pd.read_csv(io.StringIO(output_string))
    records = df.to_dict('records')
    
    output_buffer = io.BytesIO()
    writer = DataFileWriter(output_buffer, DatumWriter(), sample_schema)
    for record in records:
        writer.append(record)
    writer.flush()
    
    return output_buffer.getvalue()

def test_deserialise_avro_basic(sample_avro_data, sample_schema):
    mock_response = type('MockResponse', (), {'read': lambda self: sample_avro_data})()
    result = deserialise_avro(mock_response, sample_schema)
    
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0] == {'a': 1, 'b': 2, 'c': 3}
    assert result[1] == {'a': 5, 'b': 6, 'c': 7}
    assert result[2] == {'a': 8, 'b': 9, 'c': 10}

def test_deserialise_avro_empty(sample_schema):
    empty_buffer = io.BytesIO()
    writer = DataFileWriter(empty_buffer, DatumWriter(), sample_schema)
    writer.flush()
    mock_response = type('MockResponse', (), {'read': lambda self: empty_buffer.getvalue()})()
    
    result = deserialise_avro(mock_response, sample_schema)
    assert isinstance(result, list)
    assert len(result) == 0

def test_deserialise_avro_invalid_data(sample_schema):
    invalid_data = b'This is not Avro data'
    mock_response = type('MockResponse', (), {'read': lambda self: invalid_data})()
    
    with pytest.raises(Exception):  # You might want to catch a more specific exception
        deserialise_avro(mock_response, sample_schema)


def test_deserialise_avro_large_dataset(sample_schema):
    large_df = pd.DataFrame({
        'a': range(10000),
        'b': range(0, 20000, 2),
        'c': range(0, 30000, 3)
    })
    
    output_buffer = io.BytesIO()
    writer = DataFileWriter(output_buffer, DatumWriter(), sample_schema)
    for record in large_df.to_dict('records'):
        writer.append(record)
    writer.flush()
    
    mock_response = type('MockResponse', (), {'read': lambda self: output_buffer.getvalue()})()
    result = deserialise_avro(mock_response, sample_schema)
    
    assert isinstance(result, list)
    assert len(result) == 10000
    assert result[0] == {'a': 0, 'b': 0, 'c': 0}
    assert result[-1] == {'a': 9999, 'b': 19998, 'c': 29997}
