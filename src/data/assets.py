from connectors import request


cache_asset_pairs = None
cache_assets = None


def get_asset_pairs():
    global cache_asset_pairs
    if not cache_asset_pairs:
        cache_asset_pairs = request.request('asset pairs')
    asset_pairs = cache_asset_pairs
    for pair in list(asset_pairs):
        if pair[-2:] == '.d':
            del asset_pairs[pair]
    return list(asset_pairs.keys())


def get_assets():
    global cache_assets
    if not cache_assets:
        cache_assets = request.request('assets')
    assets = cache_assets
    return assets


def get_asset_standard_name(name_or_altname, assets_dict=None):
    """Return the standard name of a given asset.
    Given asset may be provided in both standard or common forms."""
    if not assets_dict:
        assets_dict = get_assets()

    if name_or_altname in assets_dict:
        return name_or_altname

    for asset_name, info in assets_dict.items():
        if info['altname'] == name_or_altname:
            return asset_name


if __name__ == '__main__':
    assets_dict = get_assets()
    print('Kraken available assets: ' + ', '.join(sorted(assets_dict)))
    asset_pairs = get_asset_pairs()
    print('Kraken available asset pairs: ' + ', '.join(sorted(asset_pairs)))
    print('LTC standard name is ' + get_asset_standard_name('LTC', assets_dict))
    print('XETH standard name is ' + get_asset_standard_name('XETH', assets_dict))
