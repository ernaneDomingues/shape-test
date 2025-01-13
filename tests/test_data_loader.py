import os
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from unittest.mock import patch, MagicMock
from src.data_loader import load_data

@pytest.fixture
def sample_df():
    return pd.DataFrame({"col1": [1, 2, 3], "col2": ["A", "B", "C"]})

@pytest.mark.parametrize(
    "file_path, mock_exists, read_error, expected_log, expected_df",
    [
        ("non_existent_file.parquet", False, None, "File not found: non_existent_file.parquet", pd.DataFrame()),
        ("empty_file.parquet", True, pd.errors.EmptyDataError, "File is empty: empty_file.parquet", pd.DataFrame()),
        ("corrupt_file.parquet", True, Exception("Unexpected error"), "Unexpected error: Unexpected error", pd.DataFrame()),
    ],
)
@patch("src.data_loader.log_failure")
@patch("src.data_loader.pd.read_parquet")
def test_load_data_errors(mock_read_parquet, mock_log_failure, file_path, mock_exists, read_error, expected_log, expected_df):
    with patch("os.path.exists", return_value=mock_exists):
        if read_error:
            mock_read_parquet.side_effect = read_error
        else:
            mock_read_parquet.return_value = expected_df

        result = load_data(file_path)

        mock_log_failure.assert_called_once_with(expected_log)
        assert_frame_equal(result, expected_df)

@patch("os.path.exists", return_value=True)
@patch("src.data_loader.pd.read_parquet")
def test_successful_load(mock_read_parquet, mock_path_exists, sample_df):
    mock_read_parquet.return_value = sample_df

    result = load_data("valid_file.parquet")

    assert_frame_equal(result, sample_df)
