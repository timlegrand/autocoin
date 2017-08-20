from connectors import request
from data import assets, ticker, balance, orders


def get_balance_capitalization(my_balance=None):
    """Return balance capitalization at current asked price for all currencies.
    If no balance is provided, return the capitalization of the Kraken balance."""
    if not my_balance:
        # Get account balance for all owned currencies
        my_balance, h = balance.get_account_balance()
    owned_currencies = my_balance.keys()

    # Get ticker for owned currencies and XBT/EUR
    kraken_pairs = assets.get_asset_pairs()  # For later reuse
    cap_pairs = assets.get_matching_pairs(owned_currencies, kraken_pairs, ['XXBT', 'XBT', 'ZEUR', 'EUR'])
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
            pair_to_XBT = assets.get_matching_pairs([currency], kraken_pairs, ['XXBT', 'XBT'])[0]
            curr_ask_xbt = float(tickers[pair_to_XBT][1])
        except:
            curr_ask_xbt = 1
        try:
            pair_to_EUR = assets.get_matching_pairs([currency], kraken_pairs, ['ZEUR', 'EUR'])[0]
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
    """Simulate orders execution and return final balance given a starting balance."""
    new_balance = start_balance
    for order in orders:
        source_curr, dest_curr = assets.get_standard_names_for_pair(order[3])
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
    cap_pairs = assets.get_matching_pairs(owned_currencies, kraken_pairs, ['XXBT', 'XBT', 'ZEUR', 'EUR'])
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
