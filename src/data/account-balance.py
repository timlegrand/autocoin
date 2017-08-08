from connectors import request
import tabulate


if __name__ == '__main__':
    balance = request.request('account balance')
    del balance['KFEE']  # Kraken Fee Credit

    # sorted_table = sorted(balance.items(), key=lambda x: float(x[-1]), reverse=True)  # By balance
    sorted_table = sorted(balance.items())  # By currency
    table_headers=['Currency', 'Balance']
    print(tabulate.tabulate(sorted_table, headers=table_headers, floatfmt=".9f"))
