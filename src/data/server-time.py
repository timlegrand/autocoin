from connectors import request
import json


if __name__ == '__main__':
    response = request.request('server time')
    print(json.dumps(response, indent=4))  # json prettier than pprint, even though 'v' is pure Python
