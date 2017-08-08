from connectors import request
import tabulate
import datetime


if __name__ == '__main__':
    open_orders = request.request('open orders')
    table=[]
    for k, v in open_orders['open'].items():
        iso_date = datetime.datetime.fromtimestamp(int(v['opentm'])).strftime('%Y-%m-%d_%H:%M:%S')
        order_line = (' '.join([k, v['descr']['order'], iso_date])).split()
        del order_line[4]
        table.append(order_line)

    sorted_table = sorted(table, key=lambda x: x[-1], reverse=True)
    table_headers=['Order #', 'Type', 'Volume', 'Pair', 'Method', 'Cost', 'Created']
    print(tabulate.tabulate(sorted_table, headers=table_headers))
