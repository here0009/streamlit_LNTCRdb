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

def calculate_md5_zip(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as _file:
        # Read the file in chunks to handle large files
        data = _file.read()
        md5_hash.update(data)
    return md5_hash.hexdigest()

def save_uploaded_file_zip(uploaded_file, output_dir):
    input_file = os.path.join(output_dir, 'input_data.zip')
    with open(input_file, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return input_file

def save_uploaded_file(uploaded_file, output_dir):
    input_file = os.path.join(output_dir, 'input_data.csv')
    with open(input_file, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return input_file

PROJECT_DIR = '.'
CONFIG_FILE = f'{PROJECT_DIR}/datapath.json'
RUNNING = True
small_font = '<p style="color:Gray; font-size: 12px; font-family: Arial;">{}</p>'
# LN_TCRDB_LOGO_FILE = f'{PROJECT_DIR}/img/lung-cancer-tcr-db-logo/svg/logo-no-background.svg'
LN_TCRDB_LOGO_FILE = f'{PROJECT_DIR}/img/lung-cancer-tcr-db-logo/LungTCR2.svg'
Healthy_T_B_colors = ['#00B945','#FF2C00', '#845B97']
header_font = '<p style="color:Black; font-size: 27px; font-family: Arial; font-weight:bold;">{}</p>'
sub_header_font = '<p style="color:Black; font-size: 21px; font-family: Arial; font-weight:bold;">{}</p>'
content_font = '<p style="color:Black; font-size: 15px; font-family: Arial;">{}</p>'
list_font  = '<li style="color:Black; font-size: 15px; font-family: Arial;">{}</li>'
note_font = '<p style="color:Gray; font-size: 12px; font-family: Arial;">{}</p>'
