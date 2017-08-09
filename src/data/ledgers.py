from connectors import request
from utils import progressbar

import datetime
import tabulate


if __name__ == '__main__':
    ledgers = {}
    ledger_chunk = None
    count = 0
    progress = None
    while True:
        headers = {'asset': 'ZEUR', 'ofs': len(ledgers)}
        ledger_chunk = request.request('ledgers', headers)
        if not count:
            count = ledger_chunk['count']
        else:
            if progress:
                progressbar.erase()
            progress = len(ledgers.keys()) * 100 // count
            progressbar.print(progress, size=10)
        ledger_chunk = ledger_chunk['ledger']
        if not ledger_chunk:
            break
        ledgers.update(ledger_chunk)

    table = []
    sum = 0
    for k, v in ledgers.items():
        e_id = v['refid']
        e_time = datetime.datetime.fromtimestamp(int(v['time'])).strftime('%Y-%m-%d %H:%M:%S')
        e_type = v['type']
        e_class = v['aclass']
        e_asset = v['asset']
        e_amount = v['amount']
        e_fee = v['fee']
        e_balance = v['balance']
        table.append([e_id, e_time, e_type, e_asset, e_amount, e_fee, e_balance])

    sorted_table = sorted(table, key=lambda x: x[1], reverse=True)  # By date
    table_headers=['ID', 'Time', 'Type', 'Asset', 'Amount', 'Fee', 'Balance']
    print(tabulate.tabulate(sorted_table, headers=table_headers, floatfmt=".5f"))
