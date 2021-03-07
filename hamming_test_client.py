import socket
import hamming
import int_convert
import random as r


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65433      # The port used by the server
NO_ERR_MODE = 0
SINGLE_ERR_MODE = 1
MULTIPLE_ERR_MODE = 2
r.seed(1)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        l = input('for exit inter "exit" for start - "start"\n')
        while l != 'exit':
            path = input('file path\n')
            if path == 'exit':
                break
            mode = input('Choose mode:\n 0 - errorless\n 1 - single errors\n 2 - multiple errors\n')
            if mode == 'exit':
                break
            mode = int(mode)

            with open(path, 'rb') as f:
                data = f.read() 
            words = hamming.bytes2words(data)
            words = [hamming.encode_word(word) for word in words]
            correct_wrds_gen, err_count_gen = insert_errors(words, 0.2, mode)
            n = len(words)
            s.sendall(int_convert.int2bytes(n))
            for i, word in enumerate(words):
                s.sendall(word)

            total_err = int_convert.bytes2int(s.recv(8))
            correct_words = int_convert.bytes2int(s.recv(8))
            print(f'total error count. recived :  {total_err}; generated : {err_count_gen}')
            print(f'total correct words. recived : {correct_words}; generated : {correct_wrds_gen}')


def insert_errors(words, worng_word_rate, mode):
    correct_words = len(words)
    err_count = 0  
    if mode == NO_ERR_MODE:
        return correct_words, err_count
    elif mode == SINGLE_ERR_MODE:
        for i in range(len(words)):
            if r.random() < worng_word_rate:
                index = r.randint(0, hamming.WORD_SIZE-1)
                hamming.insert_err(words[i], index)
                correct_words -= 1
                err_count += 1
    else:
        for i in range(len(words)):
            if r.random() < worng_word_rate:
                index1 = r.randint(0, hamming.WORD_SIZE-1)
                index2 = r.randint(0, hamming.WORD_SIZE-1)
                if index1 == index2:
                    if index1 > 0:
                        index1 -= 1
                    else:
                        index1 += 1
                hamming.insert_err(words[i], index1)
                hamming.insert_err(words[i], index2)
                correct_words -= 1
                err_count += 2

    return correct_words, err_count


main()
