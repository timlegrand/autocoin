from connectors.kraken import resources


cache = {}


def is_cachable(resource_name):
    return resources[resource_name][2]
