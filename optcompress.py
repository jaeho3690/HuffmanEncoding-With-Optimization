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
    # Opitmized by creating binary code for frequently appearing words
    def __init__(self,input_path,output_path='./data/optcompress.bin' ):
        self.input_path = input_path
        self.output_path= output_path
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

        self.original_file_size =os.path.getsize(self.input_path)

        # main
        self.read_txt()
        self.word_count()
        self.create_heap()
        self.initialize_mapping()
        self.print_mapping()
        self.encode_txt()

    def read_txt(self):
        # Read Txt that needs to be encoded
        with open(self.input_path)as file:
            # Save input file to original
            self.original= file.read()
        self.word_frequency= Counter(self.original)

    def word_count(self):
        """In ordinary huffman encoding, the code reads alphabet by alphabets. The optimized version reads both word and alphabet
        It will first make a dictionary of n most popular words. If the words are in this dictionary, the words are replaced with the encoding
        Otherwise, we follow the normal Huffman encoding. However, I have found out that we have to choose n based on file size. If the file is 
        too small, n should be small as well.
        Args:
            n: Top n most popular words
        """
        if self.original_file_size > 100000:
            n=200
        else:
            n=50

        print("Using top {} most popular words".format(n))
        counts = dict()
        words = self.original.split()
        # Create word dictionary
        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        self.top_n_vocab = dict(Counter(counts).most_common(n))
        res = list(self.top_n_vocab.keys())
        # Some words such as I are already included in the normal Huffman encoding. We remove words with length 1
        for key in res:
            if len(key)==1:
                self.top_n_vocab.pop(key)
        # Add '\n' as this is the most frequently happening
        self.top_n_vocab['\n']=10000
        self.word_frequency.update(self.top_n_vocab)

    def create_heap(self):
        for word in self.word_frequency:
            node = Node(self.word_frequency[word],word)
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
            if lines.startswith(" "):
                lines = lines.zfill(len(lines)+1)
                words =  [i for j in lines.split(" ") for i in (j, ' ')][1:-1]
            else:
                words = [i for j in lines.split(" ") for i in (j," ") if i!=""][:-1]
            for word in words:
                if word in self.top_n_vocab:
                    self.encoded_txt+=self.mapping[word]
                else:
                    for alphabet in word:
                        self.encoded_txt+= self.mapping[alphabet]


    def print_mapping(self):
        # Print out the mapping as the homework instructed
        for i in self.mapping:
            print(i, end =":")
            print(self.mapping[i], end =" ")
        print('\n')

    def add_padding(self):
        # The computer will add random bits to the end if the whole length is not a multiple of 8
        # This function will also encode the data into byte
        numbers_of_padding = 8- len(self.encoded_txt)%8

        for i in range(numbers_of_padding):
            self.encoded_txt +='0'
        
        padding_info = "{0:08b}".format(numbers_of_padding)
        print("PADDING INFO",padding_info)
        self.encoded_txt = padding_info+self.encoded_txt

        assert len(self.encoded_txt)%8==0 

        self.encoded_byte= bytearray()

        
        for i in range(0,len(self.encoded_txt),8):
            byte = self.encoded_txt[i:i+8]
            self.encoded_byte.append(int(byte,2))
        self.encoded_byte = bytes(self.encoded_byte)
        

    def compare_file_size(self,original_txt,compressed_file):
        # Utility function to compare the change in file size
        original = os.path.getsize(original_txt)
        compressed = os.path.getsize(compressed_file)
        print("File size compressed from {} byte to {} byte".format(original,compressed))
        proportion = (compressed/ original)*100
        self.compressed_file_size = compressed
        self.compressed_proportion = proportion
        print("Compressed proportion {:.2f}%".format(proportion))        
        
    def save_encoded_bin(self):
        start_time = time.time()
        self.add_padding()
        # Write mapping information
        mapping_table = open(self.output_path,'wb')
        mapped_info = str(self.mapping)
        mapping_table.write(mapped_info.encode())
        mapping_table.close()

        # create a separating line
        seperate_line = open(self.output_path,'a')
        seperate_line.write('\n')
        seperate_line.close()

        # write encoded txt to file
        encoded_line = open(self.output_path,'ab')
        encoded_line.write(self.encoded_byte)
        encoded_line.close()

        self.encoding_time = time.time()- start_time
        # The whole structure is as follow
        #  Mapping + '/n' + Padding_info + encoded txt 
        print("Saved binary file to {} directory".format(self.output_path))

        self.compare_file_size(self.input_path,self.output_path)
        print("Encoding Time was {} ".format(self.encoding_time))
        

def main():
    Opt = OptHuffman('./data/input.txt')
    Opt.save_encoded_bin()

if __name__ == "__main__":
    main()