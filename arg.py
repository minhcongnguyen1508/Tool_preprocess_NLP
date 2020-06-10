# include standard modules
import argparse

# initiate the parser
parser = argparse.ArgumentParser()

# add long and short argument
parser.add_argument("--model_tokenizer", "-m", help="get model")
parser.add_argument("--input_filename", "-i", help="input file name")
parser.add_argument("--output_filename", "-o", help="output file name")
args = parser.parse_args()

if args.input_filename:
    print(args.model_tokenizer)
    print(args.input_filename)
    print(args.output_filename)
	
