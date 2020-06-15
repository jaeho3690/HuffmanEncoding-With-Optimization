import time
import os
import pandas as pd 

from compress import Huffman
from optcompress import OptHuffman
from decompress import DecodeHuffman
from optdecompress import OptimizedDecodeHuffman


# Load all test cases
test_cases = os.listdir('./testcases/Tests/')


log= pd.DataFrame(index=[],columns= ['Name','File_Size','Encoded_File_Size','Encoding_Time','Compression_Proportion','Diversity_of_alphabets','Decoding_Time'])
# test compress
for test in test_cases:
    print("*"*43)   
    print("********* TESTING {} *********".format(test))
    print("*"*43)
    Huff = Huffman(input_path= './testcases/Tests/{}'.format(test),output_path ='./testcases/Compressed/{}.bin'.format(test[:5]))
    Huff.save_encoded_bin()
    time= Huff.encoding_time
    original_file_size = Huff.original_file_size
    compressed_file_size = Huff.compressed_file_size
    compressed_proportion = Huff.compressed_proportion
    diversity_of_alphabets = len(Huff.word_frequency)

    DecodeHuff = DecodeHuffman(encoded_huffman_path= './testcases/Compressed/{}.bin'.format(test[:5]),original_path='./testcases/Tests/{}'.format(test),output_path='./testcases/Decompressed/{}_decompressed_output.txt'.format(test[:5]))
    DecodeHuff.decompress()
    decoding_time = DecodeHuff.decoding_time


    tmp = pd.Series([
        test,original_file_size,compressed_file_size,time,compressed_proportion,diversity_of_alphabets,decoding_time
    ], index=['Name','File_Size','Encoded_File_Size','Encoding_Time','Compression_Proportion','Diversity_of_alphabets','Decoding_Time'])

    log = log.append(tmp, ignore_index=True)
    log.to_csv('./testcases/Log/Normal_Huffman_log.csv', index=False)
    print("Saved to csv")
    print("*"*44)
    print(" ")

optimized_log= pd.DataFrame(index=[],columns= ['Name','File_Size','Optimized_Encoded_File_Size','Optimized_Encoding_Time','Optimized_Compression_Proportion','Diversity_of_alphabets','Optimized_Decoding_Time'])
# test Optimized Compress

for test in test_cases:
    print("*"*43)
    print("**** TESTING for Optimized {} *****".format(test))
    print("*"*43)
    OptHuff = OptHuffman(input_path= './testcases/Tests/{}'.format(test),output_path ='./testcases/OptCompressed/{}.bin'.format(test[:5]))
    OptHuff.save_encoded_bin()
    time= OptHuff.encoding_time
    original_file_size = OptHuff.original_file_size
    compressed_file_size = OptHuff.compressed_file_size
    compressed_proportion = OptHuff.compressed_proportion
    diversity_of_alphabets = len(OptHuff.word_frequency)

    OptDecodeHuff = OptimizedDecodeHuffman(encoded_huffman_path= './testcases/OptCompressed/{}.bin'.format(test[:5]),original_path='./testcases/Tests/{}'.format(test),output_path='./testcases/OptDecompressed/{}_optimized_output.txt'.format(test[:5]))
    OptDecodeHuff.decompress()
    decoding_time = OptDecodeHuff.decoding_time


    tmp = pd.Series([
        test,original_file_size,compressed_file_size,time,compressed_proportion,diversity_of_alphabets,decoding_time
    ], index=['Name','File_Size','Optimized_Encoded_File_Size','Optimized_Encoding_Time','Optimized_Compression_Proportion','Diversity_of_alphabets','Optimized_Decoding_Time'])

    optimized_log = optimized_log.append(tmp, ignore_index=True)
    optimized_log.to_csv('./testcases/Log/Optimized_Huffman_log.csv', index=False)
    print("Saved to csv")
    print("*"*44)
    print(" ")