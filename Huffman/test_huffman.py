#!/usr/bin/env python3
# coding: utf-8

from huffman import *
import time


def average(tree):
    code = huffman_code(tree)

    avg = 0
    for i, e in enumerate(code):
        avg += len(code[e][1]) * proba[i]

    return avg/len(code) * 100


def compression_ratio(uncompressed, compressed):
    return 1 - len(compressed) / len(uncompressed) * 100


def test_compress_decompress_horla():

    # Unit test
    with open("samples/horla.txt") as f:
        original_data = f.read()

    t1 = time.time()
    compressed_data, tree = compress_file("samples/horla.txt", "samples/horla.txt.huf")
    t2 = time.time()
    decompress_data = decompress_file(tree, "samples/horla.txt.huf")
    t3 = time.time()

    assert original_data == decompress_data

    # Additional infos (pytest -s)
    print('\n[i] Compression of samples/horla.txt')
    print("->  File size: %d Bytes" % len(original_data.encode()))
    print("->  Compress time: %.4fs" % (t2 - t1))
    print("->  Decompress time: %.4fs" % (t3 - t2))
    print("->  Compression ratio: %.2f%%" % compression_ratio(original_data, compressed_data))


def test_compress_decompress_french_text():

    # Unit test
    with open("samples/french_text.txt") as f:
        original_data = f.read()

    t1 = time.time()
    compressed_data, tree = compress_file("samples/french_text.txt", "samples/french_text.txt.huf")
    t2 = time.time()
    decompress_data = decompress_file(tree, "samples/french_text.txt.huf")
    t3 = time.time()

    assert original_data == decompress_data

    # Additional infos (pytest -s)
    print('\n[i] Compression of samples/french_text.txt')
    print("->  File size: %d KB" % (len(original_data.encode()) / 1024))
    print("->  Compress time: %.4fs" % (t2 - t1))
    print("->  Decompress time: %.4fs" % (t3 - t2))
    print("->  Compression ratio: %.2f%%" % compression_ratio(original_data, compressed_data))


def test_compress_decompress_message():

    # Unit test
    with open("samples/message.txt") as f:
        original_data = f.read()

    t1 = time.time()
    compressed_data, tree = compress_file("samples/message.txt", "samples/message.txt.huf")
    t2 = time.time()
    decompress_data = decompress_file(tree, "samples/message.txt.huf")
    t3 = time.time()

    assert original_data == decompress_data

    # Additional infos (pytest -s)
    print('\n[i] Compression of samples/message.txt')
    print("->  File size: %d Bytes" % len(original_data.encode()))
    print("->  Compress time: %.4fs" % (t2 - t1))
    print("->  Decompress time: %.4fs" % (t3 - t2))
    print("->  Compression ratio: %.2f%%" % compression_ratio(original_data, compressed_data))


if __name__ == '__main__':
    test_compress_decompress_horla()
    test_compress_decompress_french_text()
    test_compress_decompress_message()
