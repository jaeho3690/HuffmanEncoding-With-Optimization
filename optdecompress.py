import os
from collections import Counter 
import heapq
import struct
import ast
import time

def read_txt(input):
    with open(input)as file:
        data= file.read()
    return data

class OptimizedDecodeHuffman:
    def __init__(self,encoded_huffman_path):
        self.huffman_file = encoded_huffman_path
        self.huffman_decoded_bits =""
        self.restored_txt =""
        self.mapping ={}
        self.reversed_mapping ={}
        self.decoding_time=0


    def remove_padding(self):
        padding_info = self.huffman_decoded_bits[:8]
        padding_num = int(padding_info,2)
        self.huffman_decoded_bits = self.huffman_decoded_bits[8:-padding_num]
    
    def writetxt(self):
        output = open('optdecompressed.txt','w')
        output.write(self.restored_txt)
        output.close()
        print("saved to optdecompressed.txt")
        
    
    def compare_with_original(self,input='./data/input.txt'):
        print("Sanity Check,,,")
        with open(input)as file:
            input_original =file.read()
        print("RESTORED LENGTH:",len(self.restored_txt))
        print("ORIGINAL LENGTH:",len(input_original))
        if input_original == self.restored_txt:
            print("The restored file is same as original input file.")
        else:
            print("Restored File NOT EQUAL TO ORIGINAL INPUT")



    def decompress(self):
        start_time= time.time()
        mapping = open(self.huffman_file,'rb').readline().decode()
        self.mapping = ast.literal_eval(mapping)
        self.reversed_mapping = {v:k for k,v in self.mapping.items()}

        encoded_lines = open(self.huffman_file,'rb').readlines()[1:]

        join_body = [item for sub in encoded_lines for item in sub]

        for i in join_body:
            self.huffman_decoded_bits+=("{0:08b}".format(i))

        # Remove extra padding done
        self.remove_padding()

        bits =""
        for i in self.huffman_decoded_bits:
            bits+=i
            if bits in self.reversed_mapping:
                self.restored_txt+= self.reversed_mapping[bits]
                bits=""
        self.decoding_time = time.time()-start_time
        self.compare_with_original()
        self.writetxt()
        print("Decoding Time took {}".format(self.decoding_time))






def main():
    DecodeHuff= OptimizedDecodeHuffman('./data/optcompress.bin')
    DecodeHuff.decompress()

if __name__ == "__main__":
    main()