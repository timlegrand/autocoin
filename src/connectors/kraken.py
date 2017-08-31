
API_SERVER_NAME = 'api.kraken.com'
API_URL = 'https://' + API_SERVER_NAME
API_VERSION = 0


# Resources tuple: (<APIResourceName>, <private/public>, <cachable>)
resources = {
    'server time': ('Time', 'public', False),
    'asset pairs': ('AssetPairs', 'public', True),
    'assets': ('Assets', 'public', True),
    'ticker': ('Ticker', 'public', False),
    'open orders': ('OpenOrders', 'private', False),
    'closed orders': ('ClosedOrders', 'private', False),
    'account balance': ('Balance', 'private', False),
    'ledgers': ('Ledgers', 'private', False),
    'trade history': ('TradesHistory', 'private', False),
}
