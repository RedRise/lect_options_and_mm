import os
from src.arbitrum import _parse_content_to_datetime
from datetime import datetime


def _get_block_request_content():
    filepath = os.path.join("data", "tests", "requests",
                            "arbitrum_block_request_content.txt")
    with open(filepath, "r") as file:
        return file.readlines()


def test_parse_content_to_datetime():
    content = _get_block_request_content()
    date_dt = _parse_content_to_datetime(str(content))
    assert date_dt == datetime(2021, 8, 31, 14, 15, 16)
