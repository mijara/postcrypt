import json

import requests


def process_request(method, url, *args, **kwargs):
    res = getattr(requests, method)(url, *args, **kwargs)
    return process_response(res)


def process_response(response):
    if response.ok:
        return json.loads(response.text)
    else:
        raise requests.exceptions.ConnectionError(response=response)
