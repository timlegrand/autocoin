from connectors import request


def get_ticker(pairs=['XXBTZEUR']):
    ticker = request.request('ticker', {'pair': ', '.join(pairs)})
    
    table=[]
    for k, v in ticker.items():
        ticker_line = [k, v['b'][0], v['a'][0]]
        table.append(ticker_line)

    table_headers=['Pair', 'Bid', 'Ask']

    return table, table_headers


if __name__ == '__main__':
    pairs = ['XZECXXBT, XZECZEUR, XXBTZEUR, XETHXXBT, XETHZEUR']
    table, table_headers = get_ticker(pairs)
    sorted_table = sorted(table, key=lambda x: x[-1], reverse=True)
    import tabulate
    print(tabulate.tabulate(sorted_table, headers=table_headers))
