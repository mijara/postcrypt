class RequestStatement:
    def __init__(self, request_type, url):
        self.request_type = request_type
        self.url = url


class PostStatement(RequestStatement):
    def __init__(self, url, body):
        super().__init__('post', url)

        self.body = body


class VariableStatement:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class SetStatement:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class LoadStatement:
    def __init__(self, file_path):
        self.file_path = file_path


class GetStatement(RequestStatement):
    def __init__(self, url):
        super().__init__('get', url)
