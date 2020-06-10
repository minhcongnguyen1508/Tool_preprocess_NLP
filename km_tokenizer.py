from utils import load_model, segment_kcc_phrase
import codecs
import argparse
import datetime

# initiate the parser
parser = argparse.ArgumentParser()

# add long and short argument
parser.add_argument("--model_tokenizer", "-m", help="get model")
parser.add_argument("--input_filename", "-i", help="input file name")
parser.add_argument("--output_filename", "-o", help="output file name")
args = parser.parse_args()
begin_time = datetime.datetime.now()

def tokenizer(_model_filename, _input_filename, _output_filename):
    crf = load_model(_model_filename)
    f1 = codecs.open(_input_filename, 'r', 'utf-8')
    f2 = codecs.open(_output_filename, 'w', 'utf-8')
    count = 0
    for line in f1:
        f2.write(segment_kcc_phrase(crf, line)+'\n')
        count += 1
    print("Number of sentences: ", count)
    f1.close()
    f2.close()
print(datetime.datetime.now() - begin_time)
tokenizer(args.model_tokenizer, args.input_filename, args.output_filename)

# try:
# except:
#     print("ERORR! Kiem tra lai file")
