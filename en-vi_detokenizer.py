import string
import codecs
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
nltk.download('punkt')

import argparse

# initiate the parser
parser = argparse.ArgumentParser()

# add long and short argument
parser.add_argument("--input_filename", "-i", help="input file name")
parser.add_argument("--output_filename", "-o", help="output file name")
args = parser.parse_args()

def untokenizer(input_filename, output_filename):
    f1 = codecs.open(input_filename, 'r', 'utf-8')
    f2 = codecs.open(output_filename, 'w', 'utf-8')
    count = 0
    for text in f1:
        tok = text.split()
        sentence = TreebankWordDetokenizer().detokenize(tok)
        f2.write(sentence + '\n')
        count += 1

    print("Number of sentences: ", count)
    f1.close()
    f2.close()

untokenizer(args.input_filename, args.output_filename)
