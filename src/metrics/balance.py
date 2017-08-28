from data import balance, orders, assets


def get_engaged_volume(currency, orders_cache=None):
    """Return the volume engaged in all open orders for the given
    currency.
    The engaged volume for a given currency is the amount of this currency
    placed in open orders and that cannot be placed in new orders before
    cancelling the previous ones."""
    if not orders_cache:
        open_orders, h = orders.get_open_orders()
    else:
        open_orders, h = orders_cache

    std_curr = assets.get_asset_standard_name(currency)
    volume = 0
    for o in open_orders:
        o_id, o_type, o_vol, o_pair, o_method, o_price, o_created = o
        src_curr = assets.get_asset_standard_name(o_pair[:3])
        dst_curr = assets.get_asset_standard_name(o_pair[3:])
        msg = ''
        if src_curr == std_curr and o[1] == 'sell':
            o_spend = float(o_vol)
            volume += o_spend
            msg += 'selling {} {} (for {})'.format(
                o_spend, std_curr, dst_curr)
        elif dst_curr == std_curr and o[1] == 'buy':
            o_spend = float(o_vol) * float(o_price)
            volume += o_spend
            msg += 'spending {} {} (to buy {} {} @{} {})'.format(
                o_spend, std_curr, o_vol, src_curr, o_price, std_curr)
        if msg:
            print('Already placed: ' + msg)
    return volume


def get_positionable_balance(currencies=None):
    """Return the volume available for order creation, i.e. not engaged
    in any open order, for all given currencies.
    If no currency list given, return positionable volume for all owned
    currencies."""
    balances, balance_headers = balance.get_account_balance()
    free_balance = {}
    order_cache = orders.get_open_orders()
    if currencies:
        currencies = [assets.get_asset_standard_name(x) for x in currencies]

    for curr, bal in balances.items():
        if currencies is None or curr in currencies:
            engaged_vol = get_engaged_volume(curr, order_cache)
            bal = float(bal) - engaged_vol
            free_balance[curr] = bal

    return free_balance, balance_headers


if __name__ == '__main__':
    free_bal, headers = get_positionable_balance()
    sorted_table = sorted(free_bal.items(), key=lambda x: x[-1], reverse=True)
    import tabulate
    print(tabulate.tabulate(
        sorted_table,
        headers=headers,
        floatfmt=".9f"))
