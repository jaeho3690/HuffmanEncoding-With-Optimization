import os
from collections import Counter 
import heapq
import struct
import ast
import time


class Node:
    def __init__(self,count,word):
        self.count = count
        self.word = word
        self.left = None
        self.right = None
    def __lt__(self,other):
        return self.count < other.count


class OptHuffman:
    def __init__(self,input_path):
        self.input_path = input_path
        self.original = None
        self.word_frequency = dict()
        self.top_n_vocab = dict()
        self.mapping = {}
        self.reversed_mapping = {}
        self.min_heap = []
        self.create_heap()
        self.encoded_txt = ""
        self.encoded_byte = None
        self.encoding_time = 0


        # main
        self.read_txt()
        self.word_count()
        self.create_heap()
        self.initialize_mapping()
        self.print_mapping()
        self.encode_txt()

    def read_txt(self):
        with open(self.input_path)as file:
            # Save input file to original
            self.original= file.read()
        self.word_frequency= Counter(self.original)

    def word_count(self,n=20):
        # It counts the words not the alphabet
        counts = dict()
        words = self.original.split()

        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        self.top_n_vocab = dict(Counter(counts).most_common(n))
        self.word_frequency.update(self.top_n_vocab)

    def create_heap(self):
        for word in self.word_frequency:
            node = Node(self.word_frequency[word],word)
            #print(self.word_frequency[word],word)
            heapq.heappush(self.min_heap,node)

        while len(self.min_heap) >1:
            node1= heapq.heappop(self.min_heap)
            node2= heapq.heappop(self.min_heap)

            merged_node =  Node(node1.count+node2.count,None)
            merged_node.left = node1
            merged_node.right = node2

            heapq.heappush(self.min_heap,merged_node)

    def initialize_mapping(self):
        root = heapq.heappop(self.min_heap)
        encode =""
        self.map_value(root,encoding=encode)
        
    def map_value(self,root,encoding):
        if root is None:
            return

        if root.word is not None:
            self.mapping[root.word]= encoding
            self.reversed_mapping[encoding]= root.word
            return
        self.map_value(root.left,encoding + '0')
        self.map_value(root.right,encoding + '1')

    def encode_txt(self):
        split = self.original.splitlines(keepends=True)
        for lines in split:
            words =  [i for j in lines.split() for i in (j, ' ')][:-1]
            words.append('/n')
            for word in words:
                if word in self.top_n_vocab:
                    self.encoded_txt+=word
                else:
                    for alphabet in word:
                        self.encoded_txt+= self.mapping[alphabet]
            break
        print("THIS IS THE FIRST",self.encoded_txt)


    def print_mapping(self):
        # Print out the mapping as the homework instructed
        for i in self.mapping:
            print(i, end =":")
            print(self.mapping[i], end =" ")
        print('\n')

def main():
    Opt = OptHuffman('./data/input.txt')

if __name__ == "__main__":
    main()