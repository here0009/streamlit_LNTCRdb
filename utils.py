import pandas as pd
import hashlib
import os
import sys


def read_csv_from_uploader(table_file):
    _sep = ',' if table_file.name.endswith(".csv") else '\t'
    try:
        table = pd.read_csv(table_file, sep=_sep)
    except:
        table = pd.read_csv(table_file, sep=_sep, encoding='gbk')
    return table

def read_csv(table_file):
    _sep = ',' if table_file.endswith(".csv") else '\t'
    try:
        table = pd.read_csv(table_file, sep=_sep)
    except:
        table = pd.read_csv(table_file, sep=_sep, encoding='gbk')
    return table


def calculate_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as _file:
        # Read the file in chunks to handle large files
        for chunk in iter(lambda: _file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

PROJECT_DIR = '.'
CONFIG_FILE = f'{PROJECT_DIR}/datapath.json'