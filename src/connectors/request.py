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
    'asset pairs': ('AssetPairs', 'public'),
    'assets': ('Assets', 'public'),
    'ticker': ('Ticker', 'public'),
    'open orders': ('OpenOrders', 'private'),
    'account balance': ('Balance', 'private'),
    'ledgers': ('Ledgers', 'private'),
}


def request(name, data_headers=None):
    '''High-level, exposed request function.
    Emits a first request and search in response for count information.
    (count info in response means partial response with a single chunk of data).
    Proceeds to further requests with offset until retreived entries count equals
    total count.'''
    complete_response = {}
    count = 0
    i = 0
    while True:
        if count:
            if count == len(complete_response):
                break
            data_headers.update({'ofs': len(complete_response)})
            print('ofs/count: {}/{}'.format(str(len(complete_response)), str(count)))

        response_data = _request(name, data_headers)

        if 'count' in response_data:
            count = response_data['count']
            del response_data['count']
            try:
                response_data_keys = list(response_data.keys())
                response_data_key = response_data_keys[0]
                response_data_chunk = response_data[response_data_key]
                complete_response.update(response_data_chunk)
            except:
                raise
        else:
            complete_response.update(response_data)
            break

    return complete_response


def _request(name, data_headers=None):

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
    if data_headers is not None:
        request_data.update(data_headers)

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

    return resp_json['result']
