import random

import numpy as np


class Hamming:
    def __init__(self, H, G):
        self.H = H
        self.G = G

    def encode(self, M):
        encoded = []
        for i in range(0, int(len(M) / 4)):
            word = [int(e) for e in list(M[i * 4: i * 4 + 4])]
            encoded.append(np.dot(word, self.G) % 2)
        return encoded

    def corrupt(self, M):
        corrupted = []
        for i in range(0, int(len(M) / 7)):
            word = [int(e) for e in list(M[i * 7: i * 7 + 7])]
            corrupt = random.randrange(start=0, step=1, stop=6)
            if (corrupt < len(word)):
                word[corrupt] = (word[corrupt] + 1) % 2
            corrupted.append(word)
        return corrupted

    def decode(self, M):
        decoded = []
        for i in range(0, int(len(M) / 7)):
            word = [int(e) for e in list(M[i * 7: i * 7 + 7])]
            control = np.dot(self.H, word) % 2
            if (1 in control):
                i = int('{}{}{}'.format(*control), 2)
                word[i - 1] = (word[i - 1] + 1) % 2
            decoded.append(word[0:4])
        return decoded


if __name__ == '__main__':
    hamming = Hamming(H=[[0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1], [1, 0, 1, 0, 1, 0, 1]],
                      G=[[1, 0, 0, 0, 0, 1, 1], [0, 1, 0, 0, 1, 0, 1], [0, 0, 1, 0, 1, 1, 0], [0, 0, 0, 1, 1, 1, 1]])

    # Encode
    coded_message = []
    with open('source.txt', 'r') as source:
        content = source.read().replace('\n', '')
        coded_message = hamming.encode(content)
    with open('emis.txt', 'w') as dest:
        for coded_word in coded_message:
            dest.write(''.join(str(word) for word in coded_word))

    # Corrupt
    corrupted_message = []
    with open('emis.txt', 'r') as source:
        content = source.read().replace('\n', '')
        corrupted_message = hamming.corrupt(content)
    with open('recu.txt', 'w') as dest:
        for corrupted_word in corrupted_message:
            dest.write(''.join(str(word) for word in corrupted_word))

    # Decode
    with open('recu.txt', 'r') as source:
        content = source.read().replace('\n', '')
        decoded_message = hamming.decode(content)
    with open('message.txt', 'w') as dest:
        for decoded_word in decoded_message:
            dest.write(''.join(str(word) for word in decoded_word))
