from connectors import request


def get_balance_capitalization():

    # Get account balance for all owned currencies
    balance = request.request('account balance')
    del balance['KFEE']  # Kraken Fee Credit
    del balance['ZEUR']
    owned_currencies = balance.keys()

    # Get ticker for owned currencies
    pairs_list = [x + 'ZEUR' for x in owned_currencies if x not in ['BCH']]
    pairs_list.extend([x + 'XXBT' for x in owned_currencies if x not in ['XXBT', 'BCH']])
    pairs_string = ', '.join(pairs_list)
    ticker = request.request('ticker', {'pair': pairs_string})

    # Consolidate the balance capitalization table
    cap_table = {}
    total_dir_cap = 0
    total_xbt_cap = 0
    xbt_eur_ask = float(ticker['XXBTZEUR']['a'][0])
    for pair in ticker:
        source_curr = pair[:4]
        if cap_table:
            if source_curr in cap_table:
                # currency already processed in a previous iteration
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
        cap_table[source_curr] = result_line
        total_dir_cap += curr_dir_cap
        total_xbt_cap += curr_xbt_cap

    cap_table = [list(cap_table[x]) for x in cap_table]
    table_headers=['Currency', 'Balance', 'Ask (EUR)', 'Direct Cap.', 'Ask (XBT)', 'XBT-to-EUR Cap.']
    total_table = [['TOTAL', '', '', total_dir_cap, '', total_xbt_cap]]

    return cap_table, table_headers, total_table


if __name__ == '__main__':
    cap_table, table_headers, total_table = get_balance_capitalization()
    sorted_table = sorted(cap_table, key=lambda x: x[-1], reverse=True)
    import tabulate
    print(tabulate.tabulate(sorted_table, headers=table_headers, floatfmt=".5f"))
    print()
    print(tabulate.tabulate(total_table, headers=table_headers, floatfmt=".5f"))
