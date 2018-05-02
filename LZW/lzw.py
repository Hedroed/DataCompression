#!/usr/bin/python3
# coding: utf-8

####
# LZW compression algorithm
# By Mathieu LUX and Nathan RYDIN
####


def compress(text: bytes):

    groups = []  # Dictionnary
    length = 8
    offset = pow(2, length)

    ret = ''

    textLen = len(text)
    w = text[0:1]

    i = 1
    while i <= textLen:
        current = text[i:i+1]
        i+=1

        while i <= textLen and (w+current) in groups:
            w += current
            current = text[i:i+1]
            i+=1
        # print(current)

        # print(w)
        if len(w) == 1:
            ret += "{:b}".format(int.from_bytes(w, 'big')).rjust(length+1, '0')
        else:
            ret += "{:b}".format(groups.index(w) + 256).rjust(length+1, '0')

        if len(groups) >= offset:
            print('Size up')
            length += 1
            offset = pow(2, length)

        if i < textLen:
            groups.append(w + current)

        w = current

    ret += '0' * (len(ret) % 8)  # padding with 0

    print("bitcode len", len(ret), len(ret) % 8)

    bitcode = [int(ret[i:i+8], 2) for i in range(0,len(ret),8)]
    return bytes(bitcode)


def decompress(text: bytes):

    bitcode = ''.join("{:08b}".format(i) for i in text)
    # print(bitcode)
    # code = [int(bitcode[i:i+9], 2) for i in range(0, len(bitcode), 9)]
    # print(code)

    groups = []  # Dictionnary
    length = 9
    offset = pow(2, length-1)

    v = int(bitcode[0:length], 2)
    ret = v.to_bytes(1, 'big')
    w = ret

    bitLen = len(bitcode)
    i = length
    while i+length < bitLen:

        v = int(bitcode[i:i+length], 2)  # current code
        i += length

        r = b''
        if v < 256:
            r = v.to_bytes(1, 'big')
        else:
            r = groups[v - 256]

        # print(v,"=>",r)
        ret += r
        groups.append(w + r[0:1])

        if len(groups) >= offset:
            print('Size up')
            offset = pow(2, length)
            length += 1

        w = r
    
    return ret



if __name__ == '__main__':
    # data = 'TOBEORNOTTOBEORTOBEORNOT'.encode()

    with open('samples/lorem.txt', 'rb') as f:
        data = f.read()

    compressed = compress(data)

    print(len(data))
    print(data)

    print(len(compressed))
    # print(compressed)
    with open('samples/lorem.txt.lzw', 'wb') as f:
        f.write(compressed)

    d = decompress(compressed)

    print(len(d))
    print(d)

    print('Compression ratio %.2f%%' % ((1 - len(compressed) / len(data)) * 100))
    print('Equal ?', d == data)