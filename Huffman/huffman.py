#!/usr/bin/env python3
# coding: utf-8

####
# Huffman algorithm
# By Mathieu LUX and Nathan RYDIN
####

from collections import Counter
from heapq import *
import unidecode


# --- Model ---

class Tree:
    def __init__(self, root=None):
        self.root = root

    def __str__(self):
        if self.root == None:
            return "Empty tree"
        else:
            return "Tree:\n" + self.root.print("", True)


class Node :
    def __init__(self, letter, left=None, right=None):
        self.left=left
        self.right=right
        self.letter=letter

    def isLeaf(self):
        return self.left == None and self.right == None

    def __str__(self):
        if self.isLeaf():
            return "\033[92mLeaf\033[0m '%s'" % self.letter
        else:
            return "\033[93mNode\033[0m"

    def __repr__(self):
        return '<'+ str(self.letter)+'.'+str(self.left)+'.'+str(self.right)+'>'

    def print(self, prefix, isTail=False):
        ret = ""
        ret += prefix + ( "└── " if isTail else "├── " ) + str(self) + "\n"
        if not self.isLeaf():
            ret += self.left.print(prefix + ("    " if isTail else "│   "), False)
            ret += self.right.print(prefix + ("    " if isTail else "│   "), True)
        return ret

    def __lt__(self, other):
        '''
            Handle the case where 2 values are equals for heapify and heappush
        '''
        return True


def get_french_frequencies() :
    caracteres = [
        ' ', 'a', 'b', 'c', 'd', 'e', 'f',
        'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't',
        'u', 'v', 'w', 'x', 'y', 'z'
    ]
    proba = [
        0.1835, 0.0640, 0.0064, 0.0259, 0.0260, 0.1486, 0.0078,
        0.0083, 0.0061, 0.0591, 0.0023, 0.0001, 0.0465, 0.0245,
        0.0623, 0.0459, 0.0256, 0.0081, 0.0555, 0.0697, 0.0572,
        0.0506, 0.0100, 0.0000, 0.0031, 0.0021, 0.0008
    ]
    table = [
            (proba[i], Node(caracteres[i]))
            for i in range(len(caracteres))
    ]
    return table


# --- Core ---

###  Ex.1  construction de l'arbre d'Huffamn utilisant la structure de "tas binaire"

def generate_tree(content):
    counts = Counter(content)
    freq = [
        (counts[c], Node(c))
        for c in counts
    ]
    freq.sort(key=lambda x:x[1].letter)
    return tree_from_frequencies(freq)


def tree_from_frequencies(frequencies):
    heapify(frequencies)
    while len(frequencies) > 1:
        node1 = heappop(frequencies)
        node2 = heappop(frequencies)

        parent = (node1[0] + node2[0], Node(None, left=node1[1], right=node2[1]))

        heappush(frequencies, parent)

    if len(frequencies) == 1:
        t = Tree(frequencies[0][1])
        return t
    else:
        raise Exception()


###  Ex.2  construction du code d'Huffamn

def parcours(node, prefixe, code):
    if node.isLeaf():
        code[node.letter] = prefixe
        return
    
    parcours(node.left, prefixe + '0', code)
    parcours(node.right, prefixe + '1', code)


def huffman_code(tree):
    # on remplit le dictionnaire du code d'Huffman en parcourant l'arbre
    code = {}
    parcours(tree.root,'',code)
    return code


###  Ex.3  encodage d'un texte contenu dans un fichier

def compress_file(in_file, out_file=None, tree=None):
    # Get content from input file
    with open(in_file) as f:
        content = f.read()
    
    # Compress file content
    bytestring, tree = compress(content, tree)

    # Write bytes to the output file
    if out_file != None:
        with open(out_file, 'wb') as o:
            o.write(bytestring)

    return bytestring, tree


def compress(content, tree=None):
    if tree is None:
        # Generate code from input file
        tree = generate_tree(content)
        code = huffman_code(tree)

    # First 6 bytes = size of the uncompressed data
    bits = bin(len(content))[2:].rjust(48, '0')
    # Convert content to bits using code
    for c in content:
        if c in code:
            bits += code[c]
        else:
            # If byte not found in code
            bits += code[0]

    # Transform bit string to bytes
    bytestring = bytes([int(bits[i:i+8].ljust(8, '0'), 2) for i in range(0, len(bits), 8)])

    return bytestring, tree


###  Ex.4  décodage d'un fichier compresse

def decompress_file(tree, compressed_file, out_file=None):
    with open(compressed_file, 'rb') as f:
        data = f.read()
    
    content = decompress(tree, data)

    # Write content to the output file
    if out_file != None:
        with open(out_file, 'w') as o:
            o.write(content)
    else:
        return content

    
def decompress(tree, data):
    content = ""
    current_node = tree.root
    # Convert data to bits
    bits = ''.join(bin(c)[2:].rjust(8, '0') for c in data)
    # First 6 bytes = size of the uncompressed data
    content_size = int(bits[:48], 2)
    # Iter until we get all uncompress characters
    i = 48
    current_size = 0
    while current_size < content_size:
        if bits[i] == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.isLeaf():
            current_size += 1
            content += current_node.letter
            current_node = tree.root
        # print('%d / %d' % (current_size, content_size))
        # print(i)
        i += 1
    
    return content
