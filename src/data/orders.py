from connectors import request

import datetime


def get_open_orders():
    open_orders = request.request('open orders')
    table=[]
    for o_id, v in open_orders['open'].items():
        o_date = datetime.datetime.fromtimestamp(int(v['opentm'])).strftime('%Y-%m-%d_%H:%M:%S')
        order_line = (' '.join([o_id, v['descr']['order'], o_date])).split()
        del order_line[4]
        table.append(order_line)

    table_headers=['Open Order #', 'Type', 'Volume', 'Pair', 'Method', 'Price', 'Created']
    return table, table_headers


def get_closed_orders():
    closed_orders = request.request('closed orders')
    table=[]
    for o_id, v in closed_orders.items():
        if v['status'] != 'closed':
            continue
        o_date = datetime.datetime.fromtimestamp(int(v['closetm'])).strftime('%Y-%m-%d_%H:%M:%S')
        try:
            before, after = v['descr']['order'].split('@')
            before = before.split()
            after = after.split()
            o_type = before[0]
            o_vol = float(v['vol'])
            o_pair = before[-1]
            o_method = after[0]
            o_price = float(v['price'])
            o_cost = float(v['cost'])
        except:
            import json
            print(v['descr']['order'])
            print(json.dumps({o_id: v}, indent=4))
            raise
        order_line = [o_id, o_type, o_vol, o_pair, o_method, o_price, o_cost, o_date]
        table.append(order_line)

    table_headers=['Closed Order #', 'Type', 'Volume', 'Pair', 'Method', 'Price', 'Cost', 'Close Time']
    return table, table_headers


if __name__ == '__main__':
    open_orders, open_orders_headers = get_open_orders()
    sorted_open_orders = sorted(open_orders, key=lambda x: x[-1], reverse=True)
    closed_orders, closed_orders_headers = get_closed_orders()
    sorted_closed_orders = sorted(closed_orders, key=lambda x: x[-1], reverse=True)
    import tabulate
    print(tabulate.tabulate(sorted_open_orders, headers=open_orders_headers))
    print(tabulate.tabulate(sorted_closed_orders, headers=closed_orders_headers))
