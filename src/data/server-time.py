from connectors import request
import json
import datetime


if __name__ == '__main__':
    response = request.request('server time')
    unixtime = response['unixtime']
    time = datetime.datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
    print(time)
