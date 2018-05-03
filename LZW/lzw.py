#!/usr/bin/env python3
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
        i += 1

        while i <= textLen and (w+current) in groups:
            w += current
            current = text[i:i+1]
            i += 1
        # print(current)

        # print(w)
        if len(w) == 1:
            r = "{:b}".format(int.from_bytes(w, 'big')).rjust(length+1, '0')
        else:
            r = "{:b}".format(groups.index(w) + 256).rjust(length+1, '0')

        ret += r

        if len(groups) >= offset:
            print('Size up')
            length += 1
            offset = pow(2, length)

        if i < textLen:
            groups.append(w + current)

        w = current

    # print("padding len", 8 - len(ret) % 8)
    ret += '0' * (8 - len(ret) % 8)  # padding with 0

    bitcode = [int(ret[i:i+8], 2) for i in range(0, len(ret), 8)]
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
    while i+length <= bitLen:

        # print(bitcode[i:i+length])

        v = int(bitcode[i:i+length], 2)  # current code
        i += length

        print(v, len(groups))

        r = b''
        if v < 256:
            r = v.to_bytes(1, 'big')
        else:
            r = groups[v - 256]

        ret += r
        groups.append(w + r[0:1])

        if len(groups) >= offset:
            print('Size up')
            offset = pow(2, length)
            length += 1

        w = r
    return ret
