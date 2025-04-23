import pytest
from error_handling import DataLoadingError, configure_logging

def test_data_loading_error():
    with pytest.raises(DataLoadingError) as excinfo:
        raise DataLoadingError("Test error")
    assert "Test error" in str(excinfo.value)

def test_configure_logging(tmp_path):
    log_file = tmp_path / "test.log"
    configure_logging(log_file=str(log_file))
    assert log_file.exists()