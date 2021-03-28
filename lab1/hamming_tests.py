from hamming import * 


def bytearray2str(bytarr):
    return [f'0x{e:x}' for e in bytarr]



def test():
    barr = bytearray(2)
    write_byte_part(barr, 128, 2, 3)
    print(*barr)
   
   
def test2():
    barr = bytearray(2)
    write_bits(barr, bytearray([192]), 1, 0, 2)
    print(*barr)

def test3():
    barr = bytearray.fromhex('ffffffffffffffffffff')
    res = insert_control_bits(barr)
    print(*bytearray2str(barr))
    print(*bytearray2str(res))

def test4():
    barr = bytearray.fromhex('ffffffffffffffffffff')
    barr[0] = 0
    print(*barr)


def test_insert_control_bits():
    barr = bytearray.fromhex('0000')
    control_bits = [1,1,1]
    k = 3
    insert_control_bits(barr, k, control_bits)
    print(*bytearray2str(barr))


def test_calculate_control_bits():
    barr = bytearray.fromhex('0842e8')
    k = 5
    msg_len =  21
    bits = calculate_control_bits(barr, k, msg_len)
    print(bits)


def test_extract_data():
    barr = bytearray.fromhex('bbbb')
    extract_data(barr)

def test_encode_decode():
    arr = bytearray.fromhex('81d0b5d182d0b82e20d0')
    word = encode_word(arr)
    print(*bytearray2str(word))

    res, err = decode_word(word)
    print(err)
    print(*bytearray2str(res))


def test_encode_decode_with_err():
    arr = bytearray.fromhex('2fb46274633463883460')
    word = encode_word(arr)
    print(*bytearray2str(word))
    
    insert_err(word, 57)
    insert_err(word, 60)
    print(*bytearray2str(word))
    res, err = decode_word(word)
    print(err)
    print(*bytearray2str(res))

#test_encode_decode()
test_encode_decode_with_err()
#test_extract_data()
#test_insert_control_bits()
#test_calculate_control_bits()

