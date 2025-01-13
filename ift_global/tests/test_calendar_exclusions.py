import pytest
from ift_global.business_date.calendar_exclusions import Country,CalendarExtract
import datetime

def test_country_enum_values():
    """Test that the enum values are correct."""
    assert Country.ALL.value == "global"
    assert Country.US.value == "usa"
    assert Country.GB.value == "england"
    assert Country.FR.value == "france"
    assert Country.DE.value == "germany"
    assert Country.JP.value == "japan"

def test_country_enum_members():
    """Test that all expected members are present in the enum."""
    expected_countries = {
        Country.ALL,
        Country.US,
        Country.GB,
        Country.FR,
        Country.DE,
        Country.JP
    }
    
    assert set(Country) == expected_countries

def test_country_enum_access():
    """Test access to enum members."""
    assert Country['US'] is Country.US
    assert Country['GB'] is Country.GB
    assert Country['FR'] is Country.FR
    assert Country['DE'] is Country.DE
    assert Country['JP'] is Country.JP

def test_country_enum_invalid_access():
    """Test that accessing an invalid member raises a KeyError."""
    with pytest.raises(KeyError):
        _ = Country['INVALID']


def test_calendar_extract_valid_initialization():
    """Test valid initialization of CalendarExtract."""
    cal_extract = CalendarExtract(country="US", exclude_date='2023-09-23')
    
    assert cal_extract.country == 'US'    
    assert cal_extract.exclude_date == datetime.datetime(2023, 9, 23)

def test_calendar_extract_invalid_date_format():
    """Test initialization with an invalid date format."""
    with pytest.raises(ValueError) as excinfo:
        # Attempt to create a CalendarExtract with an invalid date format
        cal_extract = CalendarExtract(country=Country.US, exclude_date='09/23/2023')  # Wrong format
    
    assert "time data '09/23/2023' does not match format '%Y-%m-%d'" in str(excinfo.value)


