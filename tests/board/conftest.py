import pytest

from tests.conftest import read_board


@pytest.fixture
def board_expected(filename_expected, num_rows: int, num_cols: int):
    return read_board(filename_expected, num_rows, num_cols)
