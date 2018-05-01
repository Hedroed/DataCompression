#!/usr/bin/python3
# coding: utf-8

####
# Huffman algorithm
# By Mathieu LUX and Nathan RYDIN
####

from heapq import *
import unidecode

###  distribution de proba sur les letrres

caracteres = [
    ' ', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z' ]

proba = [
    0.1835, 0.0640, 0.0064, 0.0259, 0.0260, 0.1486, 0.0078,
    0.0083, 0.0061, 0.0591, 0.0023, 0.0001, 0.0465, 0.0245,
    0.0623, 0.0459, 0.0256, 0.0081, 0.0555, 0.0697, 0.0572,
    0.0506, 0.0100, 0.0000, 0.0031, 0.0021, 0.0008  ]

###  la classe Node

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


def frequencies() :
    table = [
        (proba[i], Node(caracteres[i]))
        for i in range(len(caracteres))
    ]
    return table


###  Ex.1  construction de l'arbre d'Huffamn utilisant la structure de "tas binaire"

def huffman_tree(frequencies):
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

def compress_file(code, in_file, out_file=None):

    # Get content from input file
    with open(in_file) as f:
        content = f.read()

    # Compress file content
    bytestring = compress(code, content)

    # Write bytes to the output file
    if out_file != None:
        with open(out_file, 'wb') as o:
            o.write(bytestring)
    else:
        return bytestring


def compress(code, content):

    # Remove uppercase letters and accents
    content = content.lower()
    content = unidecode.unidecode(content)

    # Convert content to bits using code
    bits = ""
    for c in content:
        if c in code:
            bits += code[c]
        else:
            bits += code[' ']

    # Transform bit string to bytes
    bytestring = bytes([int(bits[i:i+8], 2) for i in range(0, len(bits), 8)])

    return bytestring


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
    
    for b in bits:
        if b == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.isLeaf():
            content += current_node.letter
            current_node = tree.root
    
    return content


if __name__ == '__main__':  

    F = frequencies()
    tree = huffman_tree(F)
    code = huffman_code(tree)
