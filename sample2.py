import urllib.request
import pprint
import json

host_ = '18080'
pass_ = '*****'

def generate_token():
    obj = {'APIPassword': pass_}
    json_data = json.dumps(obj).encode('utf8')
    url = f'http://localhost:{host_}/kabusapi/token'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as res:
            content = json.loads(res.read())    
            token_value = content.get('Token')
    except urllib.error.HTTPError as e:
        print(e)
    return token_value

token = generate_token()
