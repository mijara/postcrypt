import json
import os

from parser import Parser
from resquest_processor import process_request


def handle_load_statement(engine, load_statement):
    parser = Parser(os.path.join(engine.base_dir, load_statement.file_path))

    statements = parser.process()

    for i in range(len(statements) - 1, -1, -1):
        engine.statements.insert(0, statements[i])

    if engine.verbose:
        engine.logger.log('LOAD', load_statement.file_path, f'{len(statements)} statement(s)')


def handle_get_statement(engine, statement):
    url = engine.with_context(statement.url)

    _handle_request_statement(engine, 'get', url, headers=engine.headers)


def handle_post_statement(engine, statement):
    url = engine.with_context(statement.url)
    body = engine.with_context(statement.body)

    _handle_request_statement(engine, 'post', url, json=json.loads(body), headers=engine.headers)


def handle_put_statement(engine, statement):
    url = engine.with_context(statement.url)
    body = engine.with_context(statement.body)

    _handle_request_statement(engine, 'put', url, json=json.loads(body), headers=engine.headers)


def handle_delete_statement(engine, statement):
    url = engine.with_context(statement.url)

    _handle_request_statement(engine, 'delete', url, headers=engine.headers)


def handle_variable_statement(engine, statement):
    engine.context[statement.name] = engine.with_context(statement.value)

    if engine.verbose:
        engine.logger.log('variable', statement.name, engine.context[statement.name])


def handle_header_statement(engine, statement):
    engine.headers[statement.key] = engine.with_context(statement.value)

    engine.logger.log('header', statement.key, engine.headers[statement.key])


def handle_log_statement(engine, statement):
    text = engine.with_context_and_headers(statement.text)
    text = text.replace('&#x27;', '"')

    engine.logger.log('LOG', statement.tag, '>>>')
    print(text)


def handle_input_statement(engine, statement):
    if statement.variable in engine.saved_input:
        engine.logger.log('INPUT', f'{statement.variable}', f'[{engine.saved_input[statement.variable]}]: ', end='')
        value = input()

        if value == '':
            value = engine.saved_input[statement.variable]
    else:
        engine.logger.log('INPUT', f'{statement.variable}:', '', end='')
        value = input()

    engine.context[statement.variable] = value
    engine.saved_input[statement.variable] = value

    if engine.save:
        engine.input_storage.store(engine.saved_input)


def handle_mode_statement(engine, statement):
    if statement.mode == engine.mode:
        if engine.verbose:
            engine.logger.log('MODE', f'{statement.mode}:', 'executing...')
    else:
        # skip statements until next mode.
        engine.skip_mode = True


def _handle_request_statement(engine, method, url, *args, **kwargs):
    engine.logger.log('request', method, url)
    engine.context['response'] = process_request(method, url, *args, **kwargs)
