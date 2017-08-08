from connectors import request
import tabulate


if __name__ == '__main__':
    # Get balance for all owned currencies
    balance = request.request('account balance')
    del balance['KFEE']  # Kraken Fee Credit
    del balance['ZEUR']

    # sorted_balance = sorted(table.items(), key=lambda x: float(x[-1]), reverse=True)  # By balance
    # sorted_balance = sorted(balance.items())  # By currency
    table_headers=['Currency', 'Balance']

    owned_currencies = balance.keys()

    pairs_list = [x + 'ZEUR' for x in owned_currencies if x not in ['BCH']]
    pairs_list.extend([x + 'XXBT' for x in owned_currencies if x not in ['XXBT', 'BCH']])
    pairs_string = ', '.join(pairs_list)

    ticker = request.request('ticker', {'pair': pairs_string})

    table = {}
    xbt_eur_ask = float(ticker['XXBTZEUR']['a'][0])
    for pair in ticker:
        source_curr = pair[:4]
        if table:
            if source_curr in table:
                # currency already processed in a previous iteration
                print('skipping pair: ' + pair)
                continue
        dest_curr = pair[4:]
        curr_balance = float(balance[source_curr])
        curr_ask_eur = float(ticker[source_curr+'ZEUR']['a'][0])
        curr_dir_cap = curr_ask_eur * curr_balance
        if source_curr != 'XXBT':
            curr_ask_xbt = float(ticker[source_curr+'XXBT']['a'][0])
        else:
            curr_ask_xbt = 1
        curr_xbt_cap = curr_ask_xbt * curr_balance * xbt_eur_ask
        result_line = (source_curr, curr_balance, curr_ask_eur, curr_dir_cap, curr_ask_xbt, curr_xbt_cap)            
        table[source_curr] = result_line

    table = [list(table[x]) for x in table]
    sorted_table = sorted(table, key=lambda x: x[-1], reverse=True)
    table_headers=['Currency', 'Balance', 'Ask (EUR)', 'Direct Cap.', 'Ask (XBT)', 'XBT-to-EUR Cap.']
    print(tabulate.tabulate(sorted_table, headers=table_headers, floatfmt=".5f"))
