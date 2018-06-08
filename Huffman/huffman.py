#!/usr/bin/env python3
# coding: utf-8

####
# Huffman algorithm
# By Mathieu LUX and Nathan RYDIN
####

from collections import Counter
from heapq import *


# --- Model ---

class Tree:
    """Tree structure.

    A tree is composed of a root (a node).
    The root is a node, it can have a left children and a right children.

    Args:
        root (Node): the root ("top") of the tree
    """

    def __init__(self, root=None):
        self.root = root

    def __str__(self):
        if self.root is not None:
            return "Empty tree"
        else:
            return "Tree:\n" + self.root.print("", True)


class Node:
    """Node structure for Huffman tree.

    A node can contains a letter, a left children and a right children.
    """
    def __init__(self, letter, left=None, right=None):
        self.left = left
        self.right = right
        self.letter = letter

    def isLeaf(self):
        """Is the node a leaf ?
        A node is a leaf if it has not childrens.
        """
        return self.left is None and self.right is None

    def __str__(self):
        if self.isLeaf():
            return "\033[92mLeaf\033[0m '%s'" % self.letter
        else:
            return "\033[93mNode\033[0m"

    def __repr__(self):
        return '<' + str(self.letter) + '.' + str(self.left) + '.' + str(self.right) + '>'

    def print(self, prefix, isTail=False):
        """Recursively print the nodes, starting from this node."""
        ret = ""
        ret += prefix + ("└── " if isTail else "├── ") + str(self) + "\n"
        if not self.isLeaf():
            ret += self.left.print(prefix + ("    " if isTail else "│   "), False)
            ret += self.right.print(prefix + ("    " if isTail else "│   "), True)
        return ret

    def __lt__(self, other):
        """Handle the case where 2 values are equals for heapify and heappush."""
        return True


def get_french_frequencies():
    """Get french fequencies on [a-z ]."""
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

# I - Huffman tree genration using "binary heap" structure

def generate_tree(content):
    """Generate an Huffman tree from datas.
    
    Args:
        content (str): the datas

    Returns:
        The Huffman tree.
    """
    counts = Counter(content)
    freq = [
        (counts[c], Node(c))
        for c in counts
    ]
    freq.sort(key=lambda x: x[1].letter)
    return tree_from_frequencies(freq)


def tree_from_frequencies(frequencies):
    """Generate a tree from frequencies.

    Args:
        frequencies (list): A list of tuples (proba, Node(letter))

    Returns:
        The Huffman tree.
    """
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


# II - Huffman code construction

def browse_tree(node, prefix, code):
    """Browse the tree to make Huffman code.

    Args:
        node (Node): The parent node
        prefix (str): Prefix from parent node
        code (list): list containing the Huffman code
    """
    if node.isLeaf():
        code[node.letter] = prefix
        return

    browse_tree(node.left, prefix + '0', code)
    browse_tree(node.right, prefix + '1', code)


def huffman_code(tree):
    """Fill the dictionary with the Huffman code by browsing the tree.
    
    Args:
        tree (Tree): the tree used to generate Huffman code

    Returns:
        The Huffman code.
    """
    code = {}
    browse_tree(tree.root, '', code)
    return code


# III - Data compression

def compress_file(in_file, out_file=None, tree=None):
    """Compress a file.

    If out_file is not None, the compressed data will be stored in a file.
    If tree is None, a tree will be automatically generated according to
    the content of in_file.

    Args:
        in_file (str): path to the file to compress
        out_file (str): path to the output file
        tree (Tree): The Huffman tree

    Returns:
        The compressed datas.
    """
    # Get content from input file
    with open(in_file) as f:
        content = f.read()

    # Compress file content
    bytestring, tree = compress(content, tree)

    # Write bytes to the output file
    if out_file is not None:
        with open(out_file, 'wb') as o:
            o.write(bytestring)

    return bytestring, tree


def compress(content, tree=None):
    """Compress datas.

    If tree is None, a tree will be automatically generated according to
    the content of in_file.

    Args:
        content (str): The datas to compress
        tree (Tree): The Huffman tree

    Returns:
        The compressed datas.
    """
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


# IV - b. Data decompression

def decompress_file(tree, compressed_file, out_file=None):
    """Decompress datas from a file.

    Args:
        tree (Tree): the tree used to compress the file
        compressed_file (str): path to the compressed file
        out_file (str): path to the output file

    Returns:
        The decompressed datas.
    """
    with open(compressed_file, 'rb') as f:
        data = f.read()

    content = decompress(tree, data)

    # Write content to the output file
    if out_file is not None:
        with open(out_file, 'w') as o:
            o.write(content)
    else:
        return content


def decompress(tree, data):
    """Decompress datas

    Args:
        tree (Tree): the tree used to compress
        data (str): the compressed datas

    Returns:
        The decompressed datas.
    """
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
        i += 1

    return content
