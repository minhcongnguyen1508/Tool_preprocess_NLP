import codecs
import argparse

# initiate the parser
parser = argparse.ArgumentParser()

# add long and short argument
parser.add_argument("--input_filename", "-i", help="input file name")
parser.add_argument("--output_filename", "-o", help="output file name")
args = parser.parse_args()


def write2text(file_in, file_out):
    f1 = codecs.open(file_in, "r", "utf-8")
    f2 = codecs.open(file_out, 'w', 'utf-8')

    for sents in f1:
        tokenized_text = sents.split("។")
        for i in tokenized_text:
            if len(i) < 5:
                continue
            f2.write(i+"។"+"\n")

    f1.close()
    f2.close()

write2text(args.input_filename, args.output_filename)
