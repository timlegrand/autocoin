from connectors import request
from data import assets, ticker, balance, orders


def get_matching_pairs(source_curr, kraken_pairs=None, dest_curr=['XXBT', 'ZEUR']):
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


def get_standard_pair_name(approx_pair, kraken_pairs=None, kraken_assets=None):
    '''For a given, non-standard currency pair,
    returns the existing Kraken pair
    e.g. LTCEUR => 'XLTCZEUR', BCHXBT => 'BCHXBT'
    '''
    if not kraken_pairs:
        kraken_pairs = assets.get_asset_pairs()
    if not kraken_assets:
        kraken_assets = assets.get_assets()

    length = len(approx_pair)
    source_curr = approx_pair[:length//2]
    dest_curr = approx_pair[-length//2:]
    s = assets.get_asset_standard_name(source_curr, kraken_assets)
    d = assets.get_asset_standard_name(dest_curr, kraken_assets)
    if s + d in kraken_pairs:
        return s, d


def get_balance_capitalization(my_balance=None):

    if not my_balance:
        # Get account balance for all owned currencies
        my_balance, h = balance.get_account_balance()
    owned_currencies = my_balance.keys()

    # Get ticker for owned currencies and XBT/EUR
    kraken_pairs = assets.get_asset_pairs()  # For later reuse
    cap_pairs = get_matching_pairs(owned_currencies, kraken_pairs, ['XXBT', 'XBT', 'ZEUR', 'EUR'])
    cap_pairs.append('XXBTZEUR')
    tickers, h = ticker.get_ticker(cap_pairs)
    xbt_eur_ask = float(tickers['XXBTZEUR'][1])

    # Consolidate the balance capitalization table
    cap_table = {}
    total_dir_cap = 0
    total_xbt_cap = 0
    for currency in my_balance:
        curr_balance = float(my_balance[currency])
        try:
            pair_to_XBT = get_matching_pairs([currency], kraken_pairs, ['XXBT', 'XBT'])[0]
            curr_ask_xbt = float(tickers[pair_to_XBT][1])
        except:
            curr_ask_xbt = 1
        try:
            pair_to_EUR = get_matching_pairs([currency], kraken_pairs, ['ZEUR', 'EUR'])[0]
            curr_ask_eur = float(tickers[pair_to_EUR][1])
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


def simulate_orders_success(orders, start_balance):
    '''Simulates orders execution and computes final balance given a starting balance'''
    new_balance = start_balance
    for order in orders:
        # print('simulate_orders_success: ' + str(order))
        source_curr, dest_curr = get_standard_pair_name(order[3])
        action = order[1]
        volume = order[2]
        pair = order[3]
        price = order[5]
        if action == 'sell':
            new_balance[dest_curr] = float(start_balance[dest_curr]) + float(volume) * float(price)
            new_balance[source_curr] = float(start_balance[source_curr]) - float(volume)
        if action == 'buy':
            new_balance[dest_curr] = float(start_balance[dest_curr]) - float(volume) * float(price)
            new_balance[source_curr] = float(start_balance[source_curr]) + float(volume)

    return new_balance


def get_orders_capitalization():

    # Get account balance for all owned currencies
    my_balance, h = balance.get_account_balance()
    owned_currencies = my_balance.keys()

    # Get ticker for owned currencies and XBT/EUR
    kraken_pairs = assets.get_asset_pairs()  # For later reuse
    cap_pairs = get_matching_pairs(owned_currencies, kraken_pairs, ['XXBT', 'XBT', 'ZEUR', 'EUR'])
    cap_pairs.append('XXBTZEUR')
    tickers, h = ticker.get_ticker(cap_pairs)
    xbt_eur_ask = float(tickers['XXBTZEUR'][1])

    # Get current open orders
    open_orders, h = orders.get_open_orders()
    expected_balance = simulate_orders_success(open_orders, my_balance)

    return get_balance_capitalization(expected_balance)


if __name__ == '__main__':
    balcap, balcap_headers, balcap_total = get_balance_capitalization()
    balcap = sorted(balcap, key=lambda x: x[-1], reverse=True)  # Sort by decreasing value
    ordcap, ordcap_headers, ordcap_total = get_orders_capitalization()
    ordcap = sorted(ordcap, key=lambda x: x[-1], reverse=True)  # Sort by decreasing value
    import tabulate
    print('Balance capitalization (sell everything at current asked price):')
    print()
    print(tabulate.tabulate(balcap, headers=balcap_headers, floatfmt=".5f"))
    print()
    print(tabulate.tabulate(balcap_total, headers=balcap_headers, floatfmt=".5f"))
    print()
    print('Orders capitalization (all orders completed, then balance sold at current asked price):')
    print()
    print(tabulate.tabulate(ordcap, headers=ordcap_headers, floatfmt=".5f"))
    print()
    print(tabulate.tabulate(ordcap_total, headers=ordcap_headers, floatfmt=".5f"))
