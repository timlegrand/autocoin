from connectors import request


def get_matching_pairs(source_curr, kraken_pairs=None, dest_curr=['XXBT', 'ZEUR']):
    """For a given source and destination currencies,
    return the list of the matching existing Kraken pairs
    e.g. LTC => ['XLTCZEUR', 'XLTCXXBT'], BCH => ['BCHEUR', 'BCHXBT']."""
    if not kraken_pairs:
        kraken_pairs = get_asset_pairs()
    pairs = []
    for s in source_curr:
        for d in dest_curr:
            if s + d in kraken_pairs:
                pairs.append(s + d)

    return pairs


def get_standard_names_for_pair(approx_pair, kraken_pairs=None, kraken_assets=None):
    """For a given, non-standard currency pair,
    return the existing Kraken currency names
    e.g. LTCEUR => ('XLTC', 'ZEUR'), BCHXBT => ('BCH', 'XBT')"""
    if not kraken_pairs:
        kraken_pairs = get_asset_pairs()
    if not kraken_assets:
        kraken_assets = get_assets()
    length = len(approx_pair)
    src = approx_pair[:length//2]
    dest = approx_pair[-length//2:]
    std_src = get_asset_standard_name(src, kraken_assets)
    std_dest = get_asset_standard_name(dest, kraken_assets)
    possible_pairs = [(x,y) for x in [src, std_src] for y in [dest, std_dest]]
    for s, d in possible_pairs:
        if s + d in kraken_pairs:
            return get_asset_standard_name(s), get_asset_standard_name(d)
    raise Exception('Standard name for asset pair "' + approx_pair + '" not found.')


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
    print('BCH standard name is ' + get_asset_standard_name('BCH', assets_dict))
    print('XBT standard name is ' + get_asset_standard_name('XBT', assets_dict))
    print('Standard currency names for pair BCHXBT is ' + str(get_standard_names_for_pair('BCHXBT')))
