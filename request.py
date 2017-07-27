import http.client
import urllib.request
import urllib.parse
import urllib.error
import time
import hashlib
import hmac
import base64
import json

KRAKEN_API_URL = 'https://api.kraken.com'
KRAKEN_API_VERSION = 0


def url_path_join(*parts):
    """Join several path parts with slashes.
    Example: url_path_join('0', 'private', 'OpenOrders')
    creates: '/0/private/OpenOrders'"""
    parts = [x.strip('/') for x in parts if x]
    path = '/' + '/'.join(parts)
    return path


resources = {
    'server time': ('Time', 'public'),
    'open orders': ('OpenOrders', 'private'),
}


def request(name):
    try:
        (resource, privacy_level) = resources[name]
        private_api = True if privacy_level == 'private' else False
    except KeyError:
        raise Exception('Unknown resource: "' + name + '"')

    urlpath = url_path_join(
        str(KRAKEN_API_VERSION),
        'private' if private_api else 'public',
        resource)

    headers = {
        'User-Agent': 'autocoin/0.0.0',
    }

    request_data = {}
    if private_api == True:
        request_data['nonce'] = int(time.time() * 1000)
        postdata = urllib.parse.urlencode(request_data)
        encoded = (str(request_data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        apikey = ''
        with open('api.key') as f:
            apikey = f.readline().replace('\n', '')

        secret = ''
        with open('secret.key') as f:
            secret = f.readline().replace('\n', '')

        signature = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
        signature_digest = base64.b64encode(signature.digest())

        headers.update({
            'API-Key': apikey,
            'API-Sign': signature_digest
        })

    url = urllib.parse.urljoin('https://api.kraken.com', urlpath)

    conn = http.client.HTTPSConnection('api.kraken.com', timeout=15)
    data = urllib.parse.urlencode(request_data)
    conn.request('POST', url, data, headers)
    response = conn.getresponse()
    if response.status not in (200, 201, 202):
        raise http.client.HTTPException(response.status)
    resp = response.read().decode()
    resp_json = json.loads(resp)

    if len(resp_json['error']) != 0:
        raise Exception(resp_json['error'])

    return resp_json