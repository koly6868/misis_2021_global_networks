import hashlib
Hash = hashlib.sha512
MAX_HASH_PLUS_ONE = 2**(Hash().digest_size * 8)


def x_map(v):
    return s2f(f'xxx_{v}')


def y_map(v):
    return s2f(f'yyy_{v}')


def gen2dpoint(key):
    return (x_map(key), y_map(key))


def s2f(in_str):
    """Return a reproducible uniformly random float in the interval [0, 1) for the given string."""
    seed = in_str.encode()
    hash_digest = Hash(seed).digest()
    hash_int = int.from_bytes(hash_digest, 'big')
    return hash_int / MAX_HASH_PLUS_ONE
