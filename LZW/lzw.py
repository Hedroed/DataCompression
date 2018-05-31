"""
LZW compression algorithm
By Mathieu LUX and Nathan RYDIN
"""
#!/usr/bin/env python3
# coding: utf-8

from typing import Dict


# MAX_GROUP_LEN = 256 * 256
MAX_GROUP_LEN = (2 ** 13)
# MAX_GROUP_LEN = (2 ** 11)


def create_dictionnary():
    groups = []  # Dictionnary
    for i in range(256):
        groups.append(i.to_bytes(1, 'big'))

    groups.append(None)

    return groups


def compress(text: bytes) -> bytes:
    statsDebug: Dict[str, int] = {}

    groups = create_dictionnary()
    length = 9
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

        r = "{:b}".format(groups.index(w)).rjust(length, '0')

        ret += r

        # k = "%d:%d" % (len(w*8), len(r))
        # if k in statsDebug:
        #     statsDebug[k] += 1
        # else:
        #     statsDebug[k] = 1

        if len(groups) >= offset:
            # print('Size up')
            length += 1
            offset = pow(2, length)

        if i < textLen:
            groups.append(w + current)

        if len(groups) > MAX_GROUP_LEN:
            ret += "{:b}".format(256).rjust(length, '0')
            # Clean up dictionnary
            groups = create_dictionnary()
            length = 9
            offset = pow(2, length)

        w = current

    ret += '0' * (8 - len(ret) % 8)  # padding with 0
    # print(statsDebug)

    bitcode = [int(ret[i:i+8], 2) for i in range(0, len(ret), 8)]
    return bytes(bitcode)


def decompress(text: bytes) -> bytes:

    bitcode = ''.join("{:08b}".format(i) for i in text)

    groups = create_dictionnary()
    length = 9
    offset = pow(2, length)

    v = int(bitcode[0:length], 2)
    ret = v.to_bytes(1, 'big')
    w = ret

    bitLen = len(bitcode)
    i = length
    r = b''
    while i+length <= bitLen:

        bc = bitcode[i:i+length]
        v = int(bc, 2)  # current code
        i += length

        if v == 256:

            groups = create_dictionnary()
            length = 9
            offset = pow(2, length)

            bc = bitcode[i:i+length]
            v = int(bc, 2)  # current code
            i += length

            r = v.to_bytes(1, 'big')
            ret += r
            w = r

            continue

        if v >= len(groups):
            r = w + r[0:1]
        else:
            r = groups[v]

        ret += r
        groups.append(w + r[0:1])

        if len(groups) >= offset:
            length += 1
            offset = pow(2, length)

        w = r

    return ret


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-d',
                        '--decode',
                        action='store_true',
                        help='Decode')

    parser.add_argument('input',
                        type=str,
                        help='In file')

    parser.add_argument('output',
                        type=str,
                        help='Out file')

    args = parser.parse_args()

    with open(args.input, 'rb') as f:
        data = f.read()

    if args.decode:
        ret = decompress(data)
    else:
        ret = compress(data)

    with open(args.output, 'wb') as f:
        f.write(ret)
