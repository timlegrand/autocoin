
def join(*parts):
    """Join several path parts with slashes.
    Example: join('0', 'private', 'OpenOrders')
    creates: '/0/private/OpenOrders'"""
    parts = [x.strip('/') for x in parts if x]
    path = '/' + '/'.join(parts)
    return path
