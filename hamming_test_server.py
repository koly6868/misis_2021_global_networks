import socket
import hamming
import int_convert
import math


HOST = '127.0.0.1'
PORT = 65433 


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                n = conn.recv(8)
                n = int_convert.bytes2int(n)
                corrected_err_count = 0
                total_correct_words = 0
                total_wrong_words = 0
                msg_size = math.ceil(hamming.MSG_SIZE / 8)

                for i in range(n):
                    word = conn.recv(msg_size)
                    word = bytearray(word)
                    _, err_c = hamming.decode_word(word)
                    if err_c == 1:
                        corrected_err_count += 1
                    if err_c  < 2:
                        total_correct_words += 1
                    if err_c == 2:
                        total_wrong_words += 1

                conn.sendall(int_convert.int2bytes(corrected_err_count))
                conn.sendall(int_convert.int2bytes(total_correct_words))
                conn.sendall(int_convert.int2bytes(total_wrong_words))

                

main()