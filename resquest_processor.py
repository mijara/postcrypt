import json

import requests


def process_request(method, url, *args, **kwargs):
    response = getattr(requests, method)(url, *args, **kwargs)

    if response.ok:
        return json.loads(response.text)
    else:
        raise requests.exceptions.ConnectionError(response=response)
