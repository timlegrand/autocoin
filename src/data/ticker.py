from connectors import request
import tabulate


if __name__ == '__main__':
    ticker = request.request('ticker', {'pair': 'XZECXXBT'})
    import json
    
    table=[]
    for k, v in ticker.items():
        ticker_line = [k, v['b'][0], v['a'][0]]
        table.append(ticker_line)

    sorted_table = sorted(table, key=lambda x: x[-1], reverse=True)
    table_headers=['Pair', 'Bid', 'Ask']
    print(tabulate.tabulate(sorted_table, headers=table_headers))
