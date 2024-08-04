import json
import urllib.request
import urllib.parse
import urllib.error
from functools import partial


class RequestException(Exception):
    pass


def _request(url: str, data: dict | None, method: str) -> dict:
    try:
        return __request(url, data, method)
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        raise RequestException("Failed to request url: {}.", exc)


def __request(url: str, data: dict | None, method: str) -> dict:
    encoded_data = urllib.parse.urlencode(data).encode('utf-8') if data else None
    request = urllib.request.Request(url, data=encoded_data, method=method)

    with urllib.request.urlopen(request) as response:
        status_code = response.getcode()
        if status_code == 200:
            response_data = response.read()
        else:
            raise RequestException("Status code is not ok: {status_code}.")

    json_data = response_data.decode('utf-8')
    return json.loads(json_data)


get = partial(_request, method="GET")
post = partial(_request, method="POST")
