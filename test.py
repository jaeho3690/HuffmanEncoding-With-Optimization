import time
import os

from compress import Huffman
from optcompress import OptHuffman
from decompress import DecodeHuffman
from optdecompress import OptimizedDecodeHuffman


# Load all test cases
test_cases = os.listdir('./testcases/Tests/')



# test compress
for test in test_cases:
    print("********* TESTING {} *********".format(test))
    Huff = Huffman(input_path= './testcases/Tests/{}'.test,output_path ='./testcases/Compressed/')
    Huff.save_encoded_bin()
    time= Huff.encoding_time
    original_file_size = Huff.original_file_size
    compressed_file_size = Huff.compressed_file_size
    compressed_proportion = Huff.compressed_proportion
