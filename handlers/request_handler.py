import json
from abc import ABC

import requests

from handler import Handler


class RequestHandler(Handler, ABC):
    def make_request(self, method, url, *args, **kwargs):
        self.logger.log('request', method, url)

        response = getattr(requests, method)(url, *args, headers=self.context.headers, **kwargs)

        if response.ok:
            data = json.loads(response.text)
            self.context.set_var('response', data)
            return data
        else:
            raise requests.exceptions.ConnectionError(response=response)


class GetRequestHandler(RequestHandler):
    def handle(self, statement):
        url = self.context.render(statement.url)

        return self.make_request('get', url)


class DeleteRequestHandler(RequestHandler):
    def handle(self, statement):
        url = self.context.render(statement.url)

        return self.make_request('delete', url)


class PostRequestHandler(RequestHandler):
    def handle(self, statement):
        url = self.context.render(statement.url)
        body = self.context.render(statement.body)

        return self.make_request('post', url, json=json.loads(body))


class PutRequestHandler(RequestHandler):
    def handle(self, statement):
        url = self.context.render(statement.url)
        body = self.context.render(statement.body)

        return self.make_request('put', url, json=json.loads(body))
