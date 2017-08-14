from connectors import request
from utils import progressbar

import datetime


def get_open_orders():
    progressbar.print(0, msg='Downloading open orders')
    open_orders = request.request('open orders')
    progressbar.erase()
    progressbar.print(100, msg='Downloading open orders')
    table=[]
    for k, v in open_orders['open'].items():
        iso_date = datetime.datetime.fromtimestamp(int(v['opentm'])).strftime('%Y-%m-%d_%H:%M:%S')
        order_line = (' '.join([k, v['descr']['order'], iso_date])).split()
        del order_line[4]
        table.append(order_line)

    table_headers=['Order #', 'Type', 'Volume', 'Pair', 'Method', 'Cost', 'Created']
    return table, table_headers


if __name__ == '__main__':
    table, table_headers = get_open_orders()
    sorted_table = sorted(table, key=lambda x: x[-1], reverse=True)
    import tabulate
    print(tabulate.tabulate(sorted_table, headers=table_headers))
