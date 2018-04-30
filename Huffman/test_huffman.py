#!/usr/bin/python3
# coding: utf-8

from huffman import *


def average():

    F = frequencies()
    tree = huffman_tree(F)
    code = huffman_code(tree)

    avg = 0
    for i,e in enumerate(code):
        avg += len(code[e][1]) * proba[i]

    return avg/len(code) * 100


def test_encode():

    F = frequencies()
    tree = huffman_tree(F)
    code = huffman_code(tree)

    encode(code, "examples/horla.txt")


if __name__ == '__main__':
    # print("Code length average : %s" % average())
    # test_encode()

    F = frequencies()
    tree = huffman_tree(F)
    # code = huffman_code(tree)

    decode(tree, "examples/horla.txt.huf")