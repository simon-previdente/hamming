import random
import numpy as np

class Hamming:
    def __init__(self, H, G):
        self.H = H
        self.G = G

    def encode(self, M):
        encoded = []
        for i in range(0, int(len(M) / 4)):
            word = [int(M[i * 4]), int(M[i * 4 + 1]), int(M[i * 4 + 2]), int(M[i * 4 + 3])]
            encoded.append(np.dot(word, self.G) % 2)
        return encoded

    def corrupt(self, M):
        corrupted = []
        for i in range(0, int(len(M) / 7)):
            word = [int(M[i * 7]), int(M[i * 7 + 1]), int(M[i * 7 + 2]), int(M[i * 7 + 3]), int(M[i * 7 + 4]),
                    int(M[i * 7 + 5]), int(M[i * 7 + 6])]
            corrupt = random.randrange(start=0, step=1, stop=6)
            if (corrupt < len(word)):
                word[corrupt] = (word[corrupt] + 1) % 2
            corrupted.append(word)
        return corrupted

    def decode(self, M):
        decoded = []
        for i in range(0, int(len(M) / 7)):
            word = [int(M[i * 7]), int(M[i * 7 + 1]), int(M[i * 7 + 2]), int(M[i * 7 + 3]), int(M[i * 7 + 4]),
                    int(M[i * 7 + 5]), int(M[i * 7 + 6])]
            control = np.dot(self.H, word) % 2
            if(1 in control):
                i = int('{}{}{}'.format(*control), 2)
                word[i-1] = (word[i-1] + 1) % 2
            decoded.append(word[0:4])
        return decoded



if __name__ == '__main__':
    hamming = Hamming( H=[[0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1], [1, 0, 1, 0, 1, 0, 1]],
                       G=[[1, 0, 0, 0, 0, 1, 1], [0, 1, 0, 0, 1, 0, 1], [0, 0, 1, 0, 1, 1, 0], [0, 0, 0, 1, 1, 1, 1]])

    # Encode
    source = open('source.txt', 'r')
    content = source.read().replace('\n', '')
    encoded = hamming.encode(content)
    source.close()
    dest = open('emis.txt', 'w')
    for part in encoded:
        s = '{}{}{}{}{}{}{}'.format(*part)
        dest.write(s)
    dest.close()

    # Bruit
    source = open('emis.txt', 'r')
    content = source.read().replace('\n', '')
    bruite = hamming.corrupt(content)
    source.close()
    dest = open('recu.txt', 'w')
    for part in bruite:
        s = '{}{}{}{}{}{}{}'.format(*part)
        dest.write(s)
    dest.close()

    # Decode
    source = open('recu.txt', 'r')
    content = source.read().replace('\n', '')
    decoded = hamming.decode(content)
    source.close()
    dest = open('message.txt', 'w')
    for part in decoded:
        s = '{}{}{}{}'.format(*part)
        dest.write(s)
    dest.close()