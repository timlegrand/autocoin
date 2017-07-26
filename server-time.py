import http.client
import urllib.request
import urllib.parse
import urllib.error
import time
import hashlib
import hmac
import base64
import json


def request(name):
    path = ''
    if name == 'open orders':
        path = 'OpenOrders'
    elif name == 'server time':
        path = 'Time'
    else:
        raise NotImplementedException('Unknown request: ' + name)

    request_data = {}
    request_data['nonce'] = int(time.time() * 1000)
    postdata = urllib.parse.urlencode(request_data)
    urlpath = '/0/public/' + path
    encoded = (str(request_data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    # apikey = ''
    # with open('api.key') as f:
    #     apikey = f.readline().replace('\n', '')

    # secret = ''
    # with open('secret.key') as f:
    #     secret = f.readline().replace('\n', '')

    # signature = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    # signature_digest = base64.b64encode(signature.digest())

    headers = {
        'User-Agent': 'autocoin/0.0.0',
        # 'API-Key': apikey,
        # 'API-Sign': signature_digest
    }

    url = 'https://api.kraken.com' + urlpath

    conn = http.client.HTTPSConnection('api.kraken.com', timeout=15)
    data = urllib.parse.urlencode(request_data)
    conn.request('POST', url, data, headers)
    response = conn.getresponse()
    if response.status not in (200, 201, 202):
        raise http.client.HTTPException(response.status)
    resp = response.read().decode()
    open_orders = json.loads(resp)

    if len(open_orders['error']) != 0:
        raise Exception(open_orders['error'])

    return open_orders


if __name__ == '__main__':
    open_orders = request('server time')
    for k, v in open_orders['result'].items():
        print(30 * '=' + '\nOrder ' + k + ':')
        print(json.dumps(v, indent=4))  # json prettier than pprint, even though 'v' is pure Python
