#!/x03_haplox/users/donglf/miniconda3/bin/python
# coding: utf-8
# aggregate the trb result of tcr analysis pipleine
# example: /x03_haplox/users/donglf/tcr_scripts/get_metadata.py /x06_haplox/users/donglf/Project/research/tcr/220108_A00250_0087_AH337TDSX3/mutation 

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

files = glob.glob(os.path.join(input_path, '**', FILE_TYPE))
for _file in files:
    _id = '.'.join(os.path.basename(_file).split('.')[:-1])
    # print(f'Processing {_file}')
    output_fhand.write(f'\n{_file}\t{_id}')


print(f'Meta data is saved in {output_file}')
output_fhand.close()
