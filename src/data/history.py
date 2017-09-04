from data import assets
from connectors import request


def get_trade_history(currency):
    """Return the trading orders (open, completed or cancelled) for the given
    currency."""
    currency = assets.get_asset_standard_name(currency)
    trade_history = request.request('trade history')
    import json
    print(json.dumps(trade_history, indent=4))
    history = []
    for a, b in trade_history.items():
        history.append((a, b))

    headers=['ID', 'Time', 'Type', 'Asset', 'Amount', 'Fee', 'Balance']
    return history, headers


if __name__ == '__main__':
    history, headers = get_trade_history('XETH')
    import tabulate
    print(tabulate.tabulate(history, headers=headers))
