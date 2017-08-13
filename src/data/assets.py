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


def get_asset_standard_name(name_or_altname, assets_dict=None):
    '''Returns the standard name of a given asset.
    Given asset may be provided in both standard or common forms.'''
    if not assets_dict:
        assets_dict = get_assets()

    if name_or_altname in assets_dict:
        return name_or_altname

    for asset_name, info in assets_dict.items():
        if info['altname'] == name_or_altname:
            return asset_name


if __name__ == '__main__':
    asset_pairs = get_asset_pairs()
    print(asset_pairs)
    assets_dict = get_assets()
    print('LTC is ' + get_asset_standard_name('LTC', assets_dict))
    print('XETH is ' + get_asset_standard_name('XETH', assets_dict))
