from connectors import request


def get_server_time():
    response = request.request('server time')
    unixtime = response['unixtime']
    return unixtime


if __name__ == '__main__':
    unixtime = get_server_time()
    import datetime
    time = datetime.datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
    print(time)
