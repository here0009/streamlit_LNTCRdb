# coding: utf-8
# aggregate the trb result of tcr analysis pipleine


import pandas as pd
import sys
import os
import glob

input_path = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])
# output_file = os.path.join(input_path, 'metadata.tsv')
FILE_TYPE = '*.txt'
output_fhand = open(output_file, 'w')
output_fhand.write('\t'.join(['file_name','sample_id']))

files = glob.glob(os.path.join(input_path, '**', FILE_TYPE), recursive=True)
for _file in files:
    _id = '.'.join(os.path.basename(_file).split('.')[:-1])
    # print(f'Processing {_file}')
    output_fhand.write(f'\n{_file}\t{_id}')


print(f'Meta data is saved in {output_file}')
output_fhand.close()
