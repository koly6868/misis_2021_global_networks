def int2bytes(val):
    return val.to_bytes(8, byteorder='big')

def bytes2int(bytes):
    return int.from_bytes(bytes, byteorder='big', signed=True)