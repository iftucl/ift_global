import pytest
import logging
import datetime
from ift_global.utils.logger import IFTLogger


test_logger = IFTLogger(app_name='IFT_LOGGER', service_name='logger_info', log_level='info')

@pytest.fixture
def log_file(tmp_path):
    """Fixture to create a temporary log file path."""
    return tmp_path / "test_app.log"

def test_logger_initialization_without_file(log_file):
    """Test logger initialization without writing to a log file."""
    logger = IFTLogger(app_name='test_app', service_name='test_service')
    
    assert logger.app_name == 'test_app'
    assert logger.service_name == 'test_service'
    assert logger.write_file is False
    assert isinstance(logger.logger, logging.Logger)

def test_logger_initialization_with_file(log_file):
    """Test logger initialization with writing to a log file."""
    logger = IFTLogger(app_name='test_app', service_name='test_service', log_path=str(log_file.parent), write_file=True)
    
    assert logger.app_name == 'test_app'
    assert logger.service_name == 'test_service'
    assert logger.write_file is True
    assert isinstance(logger.logger, logging.Logger)


def test_logger_uid_generation():
    """Test that the logger UID is generated correctly."""
    logger = IFTLogger(app_name='test_app', service_name='test_service')
    
    expected_uid_prefix = f'test_app_test_service_{datetime.datetime.now().strftime("%y%m%d%H%M%S")[:8]}'
    
    # Check if the generated UID starts with the expected prefix
    assert logger._logger_uid.startswith(expected_uid_prefix)


def test_IFT_logger_init():
    logger = IFTLogger(app_name='test_app', service_name='test_service')
    assert logger.app_name == 'test_app'
    assert logger.service_name == 'test_service'
    assert logger.write_file == False
    assert logger.log_level == 'debug'

def test_IFT_logger_init_with_options(log_file):
    logger = IFTLogger(
        app_name='test_app',
        service_name='test_service',
        log_level='info',
        write_file=True,
        log_path=str(log_file.parent)
    )
    assert logger.app_name == 'test_app'
    assert logger.service_name == 'test_service'
    assert logger.write_file == True
    assert logger.log_level == 'info'

def test_IFT_logger_get_log_level():
    logger = IFTLogger(app_name='test_app', service_name='test_service', log_level='debug')
    assert logger._get_log_level() == logging.DEBUG

    logger = IFTLogger(app_name='test_app', service_name='test_service', log_level='info')
    assert logger._get_log_level() == logging.INFO

    logger = IFTLogger(app_name='test_app', service_name='test_service', log_level='warning')
    assert logger._get_log_level() == logging.WARNING

    logger = IFTLogger(app_name='test_app', service_name='test_service', log_level='error')
    assert logger._get_log_level() == logging.ERROR

    logger = IFTLogger(app_name='test_app', service_name='test_service', log_level='critical')
    assert logger._get_log_level() == logging.CRITICAL