# Huffman Encoding with Optimization
This was our last homework for Into to Algorithm (CS331, prof Youngbin Lim). There were 4 source codes that we had to implement. 
1. compress.py   - Ordinary Huffman Encoding compression file
2. decompress.py   - Ordinary Huffman Encoding Decompression file
3. Optcompress.py   - Optimizied Huffman Encoding compression file
4. Optdecompress.py   - Optimizied Huffman Encoding Decompression file

There are many references on how to implement an ordinary Huffman encoding file. This is the 
[github](https://gist.github.com/mekhanix/b7c5395f4b1e1a7ea9dc377703bb6ce1) I used as a reference for coding the ordinary compress.py and decompress.py

# Optimization Idea
For the Optimized version, I wasn't able to find any reference. There were papers that optimized by grouping words. But I didn't get how it works. So I had to come up with an original method. My ideas for optimization were as below and for people who may have studied Naive Bayes might easily understand the method.

1. Each word in a txt file is usually not independent from other words inside the txt.
2. Some words would appear more frequently than others. For instance, in a txt file about spam, there would be words like "Viagra" which are somewhat uncommon in general txt information.
3. Thus, we make a count on the words that appear in a txt file. With these counts, we make a top_N_dictionary that contains frequently appearing words.
4. We encode these words along with the ordinary Huffman Encoding scheme.
5. We read the txt file word by word, and if the word is in the top_N_dictionary, we encode the whole word. If not, we encode as we would in an ordinary Huffman Encoding.

Somethings to note is that the optimal value of "N" would differ by txt files. A bigger number of N does not guarantee the performance of the optimization. However, I have noticed that txt files that are longer usually need an N that is bigger than 200. Increasing this number may result in increased memory usage, so we must be careful of the tradeoff. In my implementation, I have chosen the N =200 for file size above 100kb, and N=50 otherwise.

# File Structure
The file structure is as below

```
+-- data
|    # This folder contains the input.txt file which was given as assignment.
+-- notebook
|    # This Jupyter notebook creates image figures.
+-- test cases
|    # This folder contains tests cases, logs etc
|   |-- Compressed
|    # Output of compress.py
|   |-- Decompressed
|    # Output of decompress.py
|   |-- Log
|    # log files of running test.py
|   |-- OptCompressed
|    # Output of Optcompress.py
|   |-- OptDecompressed
|    # Output of Optdecompress.py
|   |-- Tests
|    # Txt files used as test cases
compress.py
# Ordinary Huffman Compression
decompress.py
# Ordinary Huffman DeCompression
optcompress.py
# Optimized Huffman Compression
optdecompress.py
# Optimized Huffman Decompression
test.py
# Runs test cases on both ordinary and optimized Huffman
```

# Optimization Result
![Table](/notebook/figures/table.png)

![Compression proportion Comparison](/notebook/figures/Compression_Proportion_Comparison.png)

![File Size Comparison](/notebook/figures/File_Size_Comparison.png)

![Encoding Time Comparison](/notebook/figures/Encoding_Time_Comparison.png)

![Decoding Time Comparison](/notebook/figures/Decoding_Time_Comparison.png)

# Reference
1. https://gist.github.com/mekhanix/b7c5395f4b1e1a7ea9dc377703bb6ce1
2. https://web.stanford.edu/class/archive/cs/cs106b/cs106b.1126/handouts/220%20Huffman%20Encoding.pdf

