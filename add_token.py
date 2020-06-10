import string
import codecs
import argparse

# initiate the parser
parser = argparse.ArgumentParser()

# add long and short argument
parser.add_argument("--languages", "-l", help="language target")
parser.add_argument("--input_filename", "-i", help="input file name")
parser.add_argument("--output_filename", "-o", help="output file name")
args = parser.parse_args()

def add_token(tgt_lang, input_filename, output_filename):
    f1 = codecs.open(input_filename, 'r', 'utf-8')
    f2 = codecs.open(output_filename, 'w', 'utf-8')
    count = 0
    for text in f1:
        # print(text)
        # tokens = [word for sent in sent_tokenize(text) for word in word_tokenize(sent)]
        token = '<' + tgt_lang + '> '
        sentence = token + text
        f2.write(sentence + '\n')
        count += 1

    print("Number of sentences: ", count)
    f1.close()
    f2.close()

add_token(args.languages, args.input_filename, args.output_filename)
