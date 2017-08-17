
# Resources tuple: (<KrakenAPIName>, <private/public>, <cachable>)
resources = {
    'server time': ('Time', 'public', False),
    'asset pairs': ('AssetPairs', 'public', True),
    'assets': ('Assets', 'public', True),
    'ticker': ('Ticker', 'public', False),
    'open orders': ('OpenOrders', 'private', False),
    'account balance': ('Balance', 'private', False),
    'ledgers': ('Ledgers', 'private', False),
}
