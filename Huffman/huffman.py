#!/usr/bin/python3
# coding: utf-8

####
# Huffman algorithm
# By Mathieu LUX and Nathan RYDIN
####

from heapq import *

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

    def fromArray(self):
        pass

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

    # def isEmpty(self):
    #     return self == None

    def __str__(self):
        return "'%s'" % self.letter

    def __repr__(self):
        return '<'+ str(self.letter)+'.'+str(self.left)+'.'+str(self.right)+'>'

    def print(self, prefix, isTail=False):
        ret = ""
        ret += prefix + ( "└── " if isTail else "├── " ) + ("Leaf '%s'" % self.letter if self.isLeaf() else "Node" ) + "\n"
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


if __name__ == '__main__':  

    F = frequencies()

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
            print(t)

        else:
            raise Exception()

    huffman_tree(F)

    ###  Ex.2  construction du code d'Huffamn

    def parcours(arbre,prefixe,code):
        # à compléter
        pass

    def code_huffman(arbre) :
        # on remplit le dictionnaire du code d'Huffman en parcourant l'arbre
        code = {}
        parcours(arbre,'',code)
        return code

    ###  Ex.3  encodage d'un texte contenu dans un fichier

    def encodage(dico,fichier) :
        # à compléter

        encode = encodage(dico,'leHorla.txt')
        print(encode)


    ###  Ex.4  décodage d'un fichier compresse

    def decodage(arbre,fichierCompresse) :
        # à compléter

        decode = decodage(H,'leHorlaEncoded.txt')
        print(decode)