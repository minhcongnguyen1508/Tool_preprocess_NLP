import string
import codecs
import argparse
import xlsxwriter

# initiate the parser
parser = argparse.ArgumentParser()

# add long and short argument
parser.add_argument("--input_filename", "-i", help="input file name")
parser.add_argument("--output_filename", "-o", help="output file name")
args = parser.parse_args()

def write_excell(input_filename, output_filename):
    f1 = codecs.open(input_filename, 'r', 'utf-8')
    count = 0
    workbook = xlsxwriter.Workbook(output_filename+'.xlsx') 
    worksheet = workbook.add_worksheet()
    # Applying multiple styles 
    # Writing on specified sheet 
    for text in f1:
        worksheet.write(count, 0, text) 
        count += 1

    print("Number of sentences: ", count)
    f1.close()
    workbook.close() 
 	
write_excell(args.input_filename, args.output_filename)
