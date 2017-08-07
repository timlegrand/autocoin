from connectors import request
import tabulate
import datetime


if __name__ == '__main__':
    balance = request.request('account balance')
    table = balance['result']
    del table['KFEE']  # Kraken Fee Credit

    # sorted_table = sorted(table.items(), key=lambda x: float(x[-1]), reverse=True)  # By balance
    sorted_table = sorted(table.items())  # By currency
    table_headers=['Currency', 'Balance']
    print(tabulate.tabulate(sorted_table, headers=table_headers, floatfmt=".9f"))
