from connectors import request


def get_asset_pairs():
    asset_pairs = request.request('asset pairs')
    for pair in list(asset_pairs):
        if pair[-2:] == '.d':
            del asset_pairs[pair]
    return list(asset_pairs.keys())


def get_assets():
    assets = request.request('assets')
    return assets


if __name__ == '__main__':
    asset_pairs = get_asset_pairs()
    print(asset_pairs)
    assets_dict = get_assets()
