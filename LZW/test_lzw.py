#!/usr/bin/env python3
# coding: utf-8


def test_wikipedia_example():
    data = 'TOBEORNOTTOBEORTOBEORNOT'.encode()

    compressed = compress(data)
    d = decompress(compressed)

    print("Compression from %d to %d bytes" % (len(data), len(compressed)))
    print('Compression ratio %.2f%%' % ((1 - len(compressed) / len(data)) * 100))
    print('Equal ?', d == data)
    assert d == data


def test_lorem_text():
    with open('samples/lorem.txt', 'rb') as f:
        data = f.read()

    compressed = compress(data)
    d = decompress(compressed)

    print("Compression from %d to %d bytes" % (len(data), len(compressed)))
    print('Compression ratio %.2f%%' % ((1 - len(compressed) / len(data)) * 100))
    print('Equal ?', d == data)
    assert d == data

    with open('samples/lorem.txt.lzw', 'wb') as f:
        f.write(compressed)


def test_horla_text():
    with open('samples/horla.txt', 'rb') as f:
        data = f.read()

    compressed = compress(data)
    d = decompress(compressed)

    print("Compression from %d to %d bytes" % (len(data), len(compressed)))
    print('Compression ratio %.2f%%' % ((1 - len(compressed) / len(data)) * 100))
    print('Equal ?', d == data)
    assert d == data

    with open('samples/horla.txt.lzw', 'wb') as f:
        f.write(compressed)
