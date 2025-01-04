import pytest

from ift_global.utils.string_utils import trim_string


def test_trim_string_space_start():
    assert trim_string('   /ift/test/this/', what='leading', action_regex='\\s+') == '/ift/test/this/'


def test_trim_string_space_end():
    """test removes space at the end of the string"""
    assert trim_string('/ift/test/this/ ', what='trailing', action_regex='\\s+') == '/ift/test/this/'


def test_trim_string_space_both():
    """test removes space at the beginning & end of the string"""
    assert trim_string(' /ift/test/this/ ', what='both', action_regex='\\s+') == '/ift/test/this/'

def test_trim_string_slash_both():
    """test removes slash at the beginning & end of the string"""
    assert trim_string('/ift/test/this/', what='both', action_regex='/') == 'ift/test/this'

def test_trim_string_numbers_start():
    """test removes all numbers at the beginning of the string"""
    assert trim_string('00000/test/this/', what='leading', action_regex='0-9') == '/test/this/'

def test_trim_string_numbers_end():
    """test removes all numbers at the end of the string"""
    assert trim_string('/test/this/0000000', what='trailing', action_regex='0-9') == '/test/this/'

def test_exceptions_raised_what_argument():
    """Test exception raised when what argument is not leading, trailing or both"""
    with pytest.raises(ValueError):
        trim_string('/test/this/0000000', 
                    what='foo', 
                    action_regex='bar') == '/test/this/'

def test_trim_string_both():
    # Test trimming both leading and trailing whitespace
    input_string = "   Hello World   "
    expected_output = "Hello World"
    result = trim_string(input_string, 'both')
    assert result == expected_output

def test_trim_string_leading():
    # Test trimming leading whitespace
    input_string = "   Hello World"
    expected_output = "Hello World"
    result = trim_string(input_string, 'leading')
    assert result == expected_output

def test_trim_string_trailing():
    # Test trimming trailing whitespace
    input_string = "Hello World   "
    expected_output = "Hello World"
    result = trim_string(input_string, 'trailing')
    assert result == expected_output

def test_trim_string_none():
    # Test when 'none' is specified (should raise an error)
    input_string = "Hello World"
    with pytest.raises(ValueError):
        trim_string(input_string, 'nonea')

def test_trim_string_invalid_what():
    # Test with an invalid value for 'what' (should raise an error)
    input_string = "Hello World"
    with pytest.raises(ValueError):
        trim_string(input_string, 'invalid')

def test_trim_string_custom_regex():
    # Test with a custom regex expression
    input_string = "!!!Hello World!!!"
    expected_output = "Hello World"
    result = trim_string(input_string, 'both', action_regex='!')
    assert result == expected_output

def test_trim_string_empty_string():
    # Test with an empty string
    input_string = ""
    expected_output = ""
    result = trim_string(input_string, 'both')
    assert result == expected_output

def test_trim_string_no_match():
    # Test when the regex does not match any characters
    input_string = "Hello World"
    expected_output = "Hello World"
    result = trim_string(input_string, 'both', action_regex='[^a-zA-Z0-9 ]+')
    assert result == expected_output