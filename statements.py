class RequestStatement:
    def __init__(self, request_type, url):
        self.request_type = request_type
        self.url = url


class GetStatement(RequestStatement):
    def __init__(self, url):
        super().__init__('get', url)


class PostStatement(RequestStatement):
    def __init__(self, url, body):
        super().__init__('post', url)

        self.body = body


class PutStatement(RequestStatement):
    def __init__(self, url, body):
        super().__init__('put', url)

        self.body = body


class DeleteStatement(RequestStatement):
    def __init__(self, url):
        super().__init__('delete', url)


class VariableStatement:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class HeaderStatement:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class LoadStatement:
    def __init__(self, file_path):
        self.file_path = file_path


class LogStatement:
    def __init__(self, tag, text):
        self.tag = tag
        self.text = text


class InputStatement:
    def __init__(self, variable):
        self.variable = variable


class ModeStatement:
    def __init__(self, mode):
        self.mode = mode
