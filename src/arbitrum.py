import re
import requests
from datetime import datetime

BLOCK_TIME_RE = re.compile("ago[\s]*\(([^\(\)]*)\s\+UTC\).*</div>")
DATE_FORMAT = "%b-%d-%Y %I:%M:%S %p"


def _parse_content_to_datetime(content: str) -> datetime:

    dates = BLOCK_TIME_RE.findall(content)

    if len(dates) != 1:
        return None

    return datetime.strptime(dates[0], DATE_FORMAT)


def get_block_time(block: int) -> datetime:

    url_template = "https://arbiscan.io/block/{block}"
    url = url_template.format(block=block)
    req = requests.get(url)

    if req.status_code != 200:
        print("Request error for url={1}, response={1}".format(
            url, str(req)))
        return None

    return _parse_content_to_datetime(str(req.content))
