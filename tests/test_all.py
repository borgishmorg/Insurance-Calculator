import requests
import requests.auth
import json
import pytest

protocol = "http"
ip = "localhost"


class Test:
    def __init__(self, label='', cmd_list=None):
        self.label = label
        self.cmd_list = cmd_list if cmd_list is not None else list()


tests = list()

files = [
    'test_login.json',
    'test_refresh.json',
    'test_calc.json'
]

for file_name in files:
    with open(file_name) as file:
        tests += [Test(**test) for test in json.load(file)['tests']]


@pytest.mark.parametrize('test', tests)
def test_all(test, port):
    print(test.label)
    access_token = None
    refresh_token = None

    for cmd in test.cmd_list:
        cmd_str = cmd['cmd']
        method = cmd['method'] if 'method' in cmd else None
        auth = None
        headers = dict()
        params = cmd['params'] if 'params' in cmd else None
        key = cmd['key'] if 'key' in cmd else None
        value = cmd['value'] if 'value' in cmd else None

        if 'auth' in cmd:
            if cmd['auth']['type'] == 'Basic':
                login = cmd['auth']['login'] if 'login' in cmd['auth'] else None
                password = cmd['auth']['password'] if 'password' in cmd['auth'] else None
                auth = requests.auth.HTTPBasicAuth(login, password)
            if cmd['auth']['type'] == 'Bearer':
                if 'token_type' in cmd['auth'] and cmd['auth']['token_type'] == 'refresh-token':
                    headers['Authorization'] = f'Bearer {refresh_token}'
                else:
                    headers['Authorization'] = f'Bearer {access_token}'

        r = requests.request(method,
                             f'{protocol}://{ip}:{port}/{cmd_str}',
                             auth=auth, json=params, headers=headers)
        assert r.status_code == 200

        res = r.json()
        if cmd_str == 'login':
            access_token = res['access-token'] if 'access-token' in res else None
            refresh_token = res['refresh-token'] if 'refresh-token' in res else None

        if key is not None:
            if value is not None:
                assert key in res
                assert res[key] == value
            else:
                assert key in res
