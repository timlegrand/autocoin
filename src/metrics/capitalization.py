from connectors import request
from data import assets


def get_existing_pairs(source_curr, kraken_pairs=None, dest_curr=['XXBT', 'ZEUR']):
    '''For a given source and destination currencies,
    returns the list of the matching existing Kraken pairs
    e.g. LTC => ['XLTCZEUR', 'XLTCXXBT'], BCH => ['BCHEUR', 'BCHXBT']
    '''
    if not kraken_pairs:
        kraken_pairs = assets.get_asset_pairs()
    pairs = []
    for s in source_curr:
        for d in dest_curr:
            if s + d in kraken_pairs:
                pairs.append(s + d)

    return pairs


def get_balance_capitalization():

    # Get account balance for all owned currencies
    balance = request.request('account balance')
    del balance['KFEE']  # Ignore Kraken Fee Credit
    owned_currencies = balance.keys()

    # Get ticker for owned currencies and XBT/EUR
    kraken_pairs = assets.get_asset_pairs()  # For later reuse
    cap_pairs = get_existing_pairs(owned_currencies, kraken_pairs, ['XXBT', 'XBT', 'ZEUR', 'EUR'])
    pairs_string = ', '.join(cap_pairs)
    ticker = request.request('ticker', {'pair': pairs_string})
    xbt_eur_ask = float(ticker['XXBTZEUR']['a'][0])

    # Consolidate the balance capitalization table
    cap_table = {}
    total_dir_cap = 0
    total_xbt_cap = 0
    for currency in balance:
        curr_balance = float(balance[currency])
        try:
            pair_to_XBT = get_existing_pairs([currency], kraken_pairs, ['XXBT', 'XBT'])[0]
            curr_ask_xbt = float(ticker[pair_to_XBT]['a'][0])
        except:
            curr_ask_xbt = 1
        try:
            pair_to_EUR = get_existing_pairs([currency], kraken_pairs, ['ZEUR', 'EUR'])[0]
            curr_ask_eur = float(ticker[pair_to_EUR]['a'][0])
        except:
            curr_ask_eur = 1
        curr_dir_cap = curr_ask_eur * curr_balance
        curr_xbt_cap = curr_ask_xbt * curr_balance * xbt_eur_ask if currency != 'ZEUR' else curr_dir_cap
        result_line = (currency, curr_balance, curr_ask_eur, curr_dir_cap, curr_ask_xbt, curr_xbt_cap)
        cap_table[currency] = result_line
        total_dir_cap += curr_dir_cap
        total_xbt_cap += curr_xbt_cap

    cap_table = [list(cap_table[x]) for x in cap_table]
    table_headers=['Currency', 'Balance', 'Ask (EUR)', 'Direct Cap.', 'Ask (XBT)', 'XBT-to-EUR Cap.']
    total_table = [['TOTAL EUR', '', '', total_dir_cap, '', total_xbt_cap]]

    return cap_table, table_headers, total_table


if __name__ == '__main__':
    cap_table, table_headers, total_table = get_balance_capitalization()
    sorted_table = sorted(cap_table, key=lambda x: x[-1], reverse=True)
    import tabulate
    print(tabulate.tabulate(sorted_table, headers=table_headers, floatfmt=".5f"))
    print()
    print(tabulate.tabulate(total_table, headers=table_headers, floatfmt=".5f"))
