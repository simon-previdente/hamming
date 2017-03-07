import random

import numpy as np


class Hamming:
    def __init__(self, H, G):
        self.H = H
        self.G = G

    def cut_and_fill_lines(self, M, n):
        lines = M.split('\n')
        for index, line in enumerate(lines):
            if len(line) % n == 0:
                continue
            for i in range(0, n - len(line) % n):
                lines[index] += '1'
        return lines

    def encode(self, M):
        encoded = []
        lines = self.cut_and_fill_lines(M=M, n=4)
        for line in lines:
            for i in range(0, int(len(line) / 4)):
                word = [int(e) for e in list(line[i * 4: i * 4 + 4])]
                encoded.append(np.dot(word, self.G) % 2)
            encoded.append('\n')
        return encoded

    def corrupt(self, M):
        corrupted = []
        lines = self.cut_and_fill_lines(M=M, n=7)
        for line in lines:
            for i in range(0, int(len(line) / 7)):
                word = [int(e) for e in list(line[i * 7: i * 7 + 7])]
                corrupt = random.randrange(start=0, step=1, stop=6)
                if (corrupt < len(word)):
                    word[corrupt] = (word[corrupt] + 1) % 2
                corrupted.append(word)
            corrupted.append('\n')
        return corrupted

    def decode(self, M):
        decoded = []
        lines = self.cut_and_fill_lines(M=M, n=7)
        for line in lines:
            for i in range(0, int(len(line) / 7)):
                word = [int(e) for e in list(line[i * 7: i * 7 + 7])]
                control = np.dot(self.H, word) % 2
                if (1 in control):
                    i = int(''.join(str(e) for e in control), 2)
                    word[i - 1] = (word[i - 1] + 1) % 2
                decoded.append(word[0:4])
            decoded.append('\n')
        return decoded


if __name__ == '__main__':
    hamming = Hamming(H=[[0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1], [1, 0, 1, 0, 1, 0, 1]],
                      G=[[1, 0, 0, 0, 0, 1, 1], [0, 1, 0, 0, 1, 0, 1], [0, 0, 1, 0, 1, 1, 0], [0, 0, 0, 1, 1, 1, 1]])

    # Encode
    coded_message = []
    with open('source.txt', 'r') as source:
        content = source.read()
        coded_message = hamming.encode(content)
    with open('build/emis.txt', 'w') as dest:
        for coded_word in coded_message:
            dest.write(''.join(str(word) for word in coded_word))

    # Corrupt
    corrupted_message = []
    with open('build/emis.txt', 'r') as source:
        content = source.read()
        corrupted_message = hamming.corrupt(content)
    with open('build/recu.txt', 'w') as dest:
        for corrupted_word in corrupted_message:
            dest.write(''.join(str(word) for word in corrupted_word))

    # Decode
    with open('build/recu.txt', 'r') as source:
        content = source.read()
        decoded_message = hamming.decode(content)
    with open('build/message.txt', 'w') as dest:
        for decoded_word in decoded_message:
            dest.write(''.join(str(word) for word in decoded_word))
