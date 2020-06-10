import codecs
import argparse

# initiate the parser
parser = argparse.ArgumentParser()

# add long and short argument
parser.add_argument("--input_filename", "-i", help="input file name")
parser.add_argument("--output_filename", "-o", help="output file name")
args = parser.parse_args()


def rm_noise(file_in, file_out):
    f1 = codecs.open(file_in, "r", "utf-8")
    f2 = codecs.open(file_out, 'w', 'utf-8')
    noise = ["|", "http", "&", "#", "(", ")"]
    for sents in f1:
        if any(t in sents for t in noise):
            continue
        f2.write(sents)

    f1.close()
    f2.close()

rm_noise(args.input_filename, args.output_filename)
