#!/usr/bin/env python3
# coding: utf-8

from lzw import *
import time


def compression_ratio(originalSize, compressSize):
    return (1 - compressSize / originalSize) * 100


def printResults(data, originalSize, compressedSize, compressTime, uncompressTime):
    print('\n[i] Compression of %s' % data)
    print("->  File size: %d Bytes" % originalSize)
    print("->  Compressed size: %d Bytes" % compressedSize)
    print("->  Compress time: %.4fs" % compressTime)
    print("->  Decompress time: %.4fs" % uncompressTime)
    print("->  Compression ratio: %.2f%%" %
          compression_ratio(originalSize, compressedSize))


def test_wikipedia_example():
    t0 = time.time()
    data = 'TOBEORNOTTOBEORTOBEORNOT'.encode()

    compressed = compress(data)
    t1 = time.time()
    d = decompress(compressed)
    t2 = time.time()
    assert d == data

    printResults(data, len(data), len(compressed), t1 - t0, t2 - t1)


# def test_lorem_text():
#     t0 = time.time()
#     with open('samples/lorem.txt', 'rb') as f:
#         data = f.read()

#     compressed = compress(data)
#     t1 = time.time()
#     d = decompress(compressed)
#     t2 = time.time()

#     assert d == data
#     printResults('samples/lorem.txt', len(data),
#                  len(compressed), t1 - t0, t2 - t1)

#     with open('samples/lorem.txt.lzw', 'wb') as f:
#         f.write(compressed)


def test_horla_text():
    t0 = time.time()
    with open('samples/horla.txt', 'rb') as f:
        data = f.read()

    compressed = compress(data)
    t1 = time.time()
    d = decompress(compressed)
    t2 = time.time()

    assert d == data
    printResults('samples/horla.txt', len(data),
                 len(compressed), t1 - t0, t2 - t1)

    with open('samples/horla.txt.lzw', 'wb') as f:
        f.write(compressed)


# def test_multiple_char():
#     t0 = time.time()
#     data = 'T      ML'.encode()

#     compressed = compress(data)
#     t1 = time.time()
#     d = decompress(compressed)
#     t2 = time.time()

#     assert d == data
#     printResults(data, len(data), len(compressed), t1 - t0, t2 - t1)


def test_french_text():
    t0 = time.time()
    with open('samples/french_text.txt', 'rb') as f:
        data = f.read()

    compressed = compress(data)
    t1 = time.time()
    d = decompress(compressed)
    t2 = time.time()

    assert d == data
    printResults('samples/french_text.txt', len(data),
                 len(compressed), t1 - t0, t2 - t1)

    with open('samples/french_text.txt.lzw', 'wb') as f:
        f.write(compressed)


def test_lenna_image():
    t0 = time.time()
    with open('samples/lenna.png', 'rb') as f:
        data = f.read()

    compressed = compress(data)
    t1 = time.time()
    d = decompress(compressed)
    t2 = time.time()

    assert d == data
    printResults('samples/lenna.png', len(data),
                 len(compressed), t1 - t0, t2 - t1)

    with open('samples/lenna.png.lzw', 'wb') as f:
        f.write(compressed)
