from connectors import request
from utils import progressbar


def get_account_balance():
    progressbar.print(0, msg='Downloading balance')
    balance = request.request('account balance')
    progressbar.erase()
    progressbar.print(100, msg='Downloading balance')
    del balance['KFEE']  # Kraken Fee Credit

    table_headers=['Currency', 'Balance']

    return balance, table_headers


if __name__ == '__main__':
    balance, table_headers = get_account_balance()
    # sorted_table = sorted(balance.items(), key=lambda x: float(x[-1]), reverse=True)  # By balance
    sorted_table = sorted(balance.items())  # By currency
    import tabulate
    print(tabulate.tabulate(sorted_table, headers=table_headers, floatfmt=".9f"))
