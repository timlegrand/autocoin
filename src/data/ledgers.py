from connectors import request

import datetime


def get_private_ledger(entry_type=[]):
    headers = {'asset': 'ZEUR'}
    ledgers = request.request('ledgers', headers)

    table = []
    sum = 0
    for k, v in ledgers.items():
        e_id = v['refid']
        e_time = datetime.datetime.fromtimestamp(int(v['time'])).strftime('%Y-%m-%d %H:%M:%S')
        e_type = v['type']
        e_class = v['aclass']
        e_asset = v['asset']
        e_amount = float(v['amount'])
        e_fee = float(v['fee'])
        e_balance = float(v['balance'])
        if entry_type:
            if e_type not in entry_type:
                continue
        table.append([e_id, e_time, e_type, e_asset, e_amount, e_fee, e_balance])

    table_headers=['ID', 'Time', 'Type', 'Asset', 'Amount', 'Fee', 'Balance']

    return table, table_headers


if __name__ == '__main__':
    table, table_headers = get_private_ledger(['deposit'])
    sorted_table = sorted(table, key=lambda x: x[1], reverse=True)  # By date
    import tabulate
    print(tabulate.tabulate(sorted_table, headers=table_headers, floatfmt=".5f"))
    sum = 0
    for e in table:
        sum += float(e[4])
    print('TOTAL deposit: ' + str(sum))
