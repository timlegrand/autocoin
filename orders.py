import request
import json


if __name__ == '__main__':
    open_orders = request.request('open orders')
    for k, v in open_orders['result']['open'].items():
        print(30 * '=' + '\nOrder ' + k + ':')
        print(json.dumps(v, indent=4))  # json prettier than pprint, even though 'v' is pure Python
