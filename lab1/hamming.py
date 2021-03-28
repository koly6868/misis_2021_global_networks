import math


WORD_SIZE = 78
K = 7
MSG_SIZE = WORD_SIZE + K


def insert_empty_control_bits(word, msg_len):
    sstart = 0
    k = 2
    dst = bytearray(math.ceil(msg_len / 8))

    while k < msg_len:
        i = k
        j = min(msg_len, 2*k-1)
        count = j - i
        write_bits(dst, word, i, sstart, count)
        sstart += count
        k *= 2

    return dst


def gen_mask(zeros_start, zeros_end):
    x = 255
    count_zeros = zeros_end - zeros_start
    x = x >> 8 - count_zeros
    x = x << 8 - zeros_end
    return ~x


def clip_byte(val, start=0, end=8):
    x = 255
    d = end - start
    x = x >> 8 - d
    x = x <<  8 - end
    return val & x


#def write_bits2(dst : bytearray, src : bytearray, dstart, sstart, count):
#    dst_p = dstart
#    src_byte_num =  sstart // 8
#    src_bit_pos = sstart % 8
#    while count > 0:
#        count_left = min(count, 8)
#
#        cur_byte_count_left =  min(8 - src_bit_pos, count_left)
#        v = clip_byte(src[src_byte_num], src_bit_pos, src_bit_pos + cur_byte_count_left) << src_bit_pos
#
#        count -= cur_byte_count_left
#        src_byte_num += 1
#        src_bit_pos = 0
#        ncur_byte_count_left = count_left - cur_byte_count_left
#        if ncur_byte_count_left > 0:
#            second_part_shift = cur_byte_count_left
#            cur_byte_count_left = ncur_byte_count_left
#            v = v | (clip_byte(src[src_byte_num], src_bit_pos, src_bit_pos + cur_byte_count_left) >> 8 - second_part_shift)
#            src_bit_pos = cur_byte_count_left
#            count -= cur_byte_count_left
#        
#        write_byte_part(dst, v, dst_p, dst_p + count_left)
#        dst_p += count_left
    

def write_byte_part(barray : bytearray, val, start, end):
    count = end - start
    assert count <= 8, "count <= 8"

    byte_num = start // 8
    byte_pos = start % 8
    val_pos = 0

    fcount = min(8 - byte_pos, count)
    v = barray[byte_num]
    barray[byte_num] = (gen_mask(byte_pos, byte_pos+fcount) & v) | ((gen_mask(fcount, 8) & val) >> byte_pos )
    val_pos += fcount

    if fcount != count:
        byte_num += 1
        byte_pos = 0
        fcount = count - fcount 
        v = barray[byte_num]
        barray[byte_num] = (gen_mask(fcount, 8) & v) | ((~gen_mask(val_pos, val_pos+fcount) & val) << val_pos)


def calculate_control_bits(barr : bytearray, k, msg_len):
    control_bits = []
    total_len = k + msg_len

    for control_bit in range(k):
        n = 2**control_bit
        t = 0
        for i in range(n-1, msg_len, 2*n):
            upper_bound = min(i+n, msg_len)
            for j in range(i, upper_bound):
                byte_index = j // 8
                bit_index = j % 8
                mask = 128 >> bit_index

                if mask & barr[byte_index] > 0:
                    t = t ^ 1

        control_bits.append(t)
    
    return control_bits


def insert_control_bits(barr : bytearray, k, control_bits):
    c_bit_pos = 1
    for i in range(k):
        byte_pos = (c_bit_pos-1) // 8
        bit_pos = (c_bit_pos-1) % 8

        v = barr[byte_pos]
        mask = 128 >> bit_pos
        cbit = control_bits[i] << (7 - bit_pos)
        barr[byte_pos] = (v & ~mask) | cbit

        c_bit_pos *= 2


def calculate_parity_bit(word, msg_len):
    t = 0
    for i in range(msg_len):
        byte_index = i // 8
        bit_index = i % 8
        mask = 128 >> bit_index
        bit = 0
        if (word[byte_index] & mask) > 0:
            bit = 1
        t = t ^ bit
    
    return t


def insert_parity_bit(word, msg_len, bit):
    if msg_len == len(word) * 8:
        word = word + bytearray.fromhex('00')
    
    byte_pos = msg_len // 8
    bit_pos = msg_len % 8

    v = word[byte_pos]
    mask = 128 >> bit_pos
    word[byte_pos] = (~mask & v) | (bit << (7 - bit_pos))
    
    return word


def get_parity_bit(word, msg_len):
    byte_pos = msg_len // 8
    bit_pos = msg_len % 8
    
    bit = 0
    mask = 128 >> bit_pos
    if word[byte_pos] & mask > 0:
        bit = 1

    return bit


def bits2byte(bits):
    if len(bits) >= 8:
        raise 
    res = 0
    c = 1
    for b in bits:
        if b:
            res += c
        c << 1

    return res


def extract_data(msg):
    byte_count = math.ceil(WORD_SIZE / 8)
    res = bytearray(byte_count)
    res_bits_count = 0

    # parity bit exclusive
    total_msg_len = WORD_SIZE + K
    block_start = 2
    while block_start < total_msg_len:
        block_end = min(total_msg_len, block_start*2 - 1)
        count = block_end - block_start
        write_bits(res, msg, res_bits_count, block_start, count)
        res_bits_count += count
        block_start *= 2

    return res


def encode_word(word):
    word = insert_empty_control_bits(word, WORD_SIZE + K)
    control_bits = calculate_control_bits(word, K, WORD_SIZE)
    insert_control_bits(word, K, control_bits)

    msg_len = WORD_SIZE + K
    bit = calculate_parity_bit(word, msg_len)
    word = insert_parity_bit(word, msg_len, bit)

    return word


def decode_word(word):
    msg_len = WORD_SIZE + K
    bits = calculate_control_bits(word, K, WORD_SIZE)
    p_extr = get_parity_bit(word, msg_len)
    p_calc = calculate_parity_bit(word, WORD_SIZE + K)
    p = p_calc^p_extr
    c = bits2byte(bits)

    if c == 0:
        return extract_data(word), 0
    elif c != 0 and p == 1:
        c -= 1
        byte_pos = c // 8
        bit_pos = c % 8

        v = word[byte_pos]
        mask = 128 >> bit_pos
        # extract and invert
        bit = 1
        if v & mask > 0:
            bit = 0

        word[byte_pos] = (~mask & v) | (bit << (7-bit_pos))
        return extract_data(word), 1

    return word, 2


def write_bits(dst : bytearray, src : bytearray, dstart, sstart, count):
    dst_pos = dstart
    src_pos = sstart

    for i in range(count):
        dst_byte_pos = dst_pos // 8
        dst_bit_pos = dst_pos % 8
        src_byte_pos = src_pos // 8
        src_bit_pos = src_pos % 8
        
        dst_mask = 128 >> dst_bit_pos
        src_mask = 128 >> src_bit_pos
        
        v = src_mask & src[src_byte_pos]
        v = v << src_bit_pos
        v = v >> dst_bit_pos
        dst[dst_byte_pos] = (~dst_mask & dst[dst_byte_pos]) | v
        
        dst_pos += 1
        src_pos += 1
    

def insert_err(word, index):
    byte_pos = index // 8
    bit_pos = index % 8

    mask = 128 >> bit_pos

    # exract and invert
    bit = 1
    if word[byte_pos] & mask > 0:
        bit = 0
    
    word[byte_pos] = (~mask & word[byte_pos]) | (bit << (7 - bit_pos) )



def bytes2words(data : bytearray):
    words = []
    n = math.ceil(len(data) * 8 / WORD_SIZE)
    word_size_in_bytes = math.ceil(WORD_SIZE / 8)

    data_pos = 0
    for i in range(n):
        word = bytearray(word_size_in_bytes)
        count = min(WORD_SIZE, len(data) - i*WORD_SIZE)
        write_bits(word, data, 0, data_pos, count)
        data_pos += WORD_SIZE
        words.append(word)
    
    return words