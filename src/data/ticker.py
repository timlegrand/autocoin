from connectors import request
import tabulate
import datetime


if __name__ == '__main__':
    ticker = request.request('ticker', {'pair': 'XZECXXBT'})
    import json
    print(json.dumps(ticker, indent=4))
    
    table=[]
    for k, v in ticker['result'].items():
        ticker_line = [k, v['b'][0], v['a'][0]]
        table.append(ticker_line)

    sorted_table = sorted(table, key=lambda x: x[-1], reverse=True)
    table_headers=['Pair', 'Bid', 'Ask']
    print(tabulate.tabulate(sorted_table, headers=table_headers))
