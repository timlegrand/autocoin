import http.client
import urllib.parse
import time
import hashlib
import hmac
import base64
import json
import utils.url

from datetime import datetime, timedelta

from connectors.cache import cache, is_cachable
from connectors.kraken import resources, API_SERVER_NAME, API_URL, API_VERSION
from utils import progressbar


last_request_time = None


def request(name, data_headers={}):
    """High-level, exposed request function.
    Return cached response if any.
    Otherwise, emit a first request and search in response for total_count
    information (count info in response means partial response with a single
    chunk of data). Then proceed to further requests with offset until
    retreived entries count equals total count."""
    if name in cache:
        # print('Using cached ' + name)
        return cache[name]

    complete_response = {}
    progress_count = 0
    total_count = 0
    last_progress_count = 0
    retries = 0

    p = progressbar.Progressbar(msg='Downloading ' + name)
    p.progress(0)

    while True:
        if total_count:
            if len(complete_response) >= total_count:
                break
            if last_progress_count == progress_count:
                # Iteration was unsuccessful to get data
                retries += 1
            if retries == 3:
                raise Exception('Cannot retry data for ' + name)
            last_progress_count = progress_count
            data_headers.update({'ofs': len(complete_response)})

        response_data = _request(name, data_headers)

        if 'count' in response_data:
            total_count = response_data['count']
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

        if total_count:
            progress_count = len(complete_response)
        else:
            progress_count = 100

        p.progress(progress_count, total_count)

        if not total_count:
            break

    # Cache data for future requests
    if is_cachable(name):
        cache[name] = complete_response

    return complete_response


def _request(name, data_headers=None):
    global last_request_time
    if last_request_time is not None:
        if last_request_time + timedelta(1) > datetime.now():
            # time.sleep(4)
            pass
    last_request_time = datetime.now()
    try:
        (resource, privacy_level, cachable) = resources[name]
        private_api = True if privacy_level == 'private' else False
    except KeyError:
        raise Exception('Unknown resource: "' + name + '"')

    urlpath = utils.url.join(
        str(API_VERSION),
        'private' if private_api else 'public',
        resource)

    headers = {
        'User-Agent': 'autocoin/0.0.0',
    }

    request_data = {}
    if data_headers is not None:
        request_data.update(data_headers)

    if private_api:
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

    url = urllib.parse.urljoin(API_URL, urlpath)

    conn = http.client.HTTPSConnection(API_SERVER_NAME, timeout=15)
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
