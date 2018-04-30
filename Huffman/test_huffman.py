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


if __name__ == '__main__':
    print("Code length average : %s" % average())