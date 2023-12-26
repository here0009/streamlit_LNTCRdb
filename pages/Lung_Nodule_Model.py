import streamlit as st
import os
import sys
import pandas as pd
sys.path.append(f'{sys.path[0]}/..')
import utils
from utils import PROJECT_DIR


def save_uploaded_file(uploaded_file):
    input_file = os.path.join(OUTPUT_DIR, 'input_data.csv')
    with open(input_file, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return input_file

def get_results(output_dir, md5_tag):
    roc_plot = os.path.join(output_dir, f'{md5_tag}_roc.svg')
    pred_val_file = os.path.join(output_dir, f'{md5_tag}_pred_val.csv')
    model_metric_file = os.path.join(output_dir, f'{md5_tag}_model_metric.csv')
    roc_file = os.path.join(output_dir, f'{md5_tag}_roc.csv')
    st.write("### Results")
    st.write("#### ROC curve")
    with open(roc_plot, 'r') as _f:
        svg = _f.read()
        st.image(svg)
    roc_tbl = pd.read_csv(roc_file)
    pred_val_tbl = pd.read_csv(pred_val_file)
    model_metric_tbl = pd.read_csv(model_metric_file)
    model_metric_tbl = model_metric_tbl.rename(columns={'Unnamed: 0':'Metrics'})
    model_metric_tbl.set_index('Metrics', inplace=True)
    st.write("#### ROC curve")
    st.dataframe(roc_tbl)
    st.write("#### Prediction value")
    st.dataframe(pred_val_tbl)
    st.write("#### Model metrics")
    st.dataframe(model_metric_tbl.T)

@st.cache_data(show_spinner="Processing...")
def predict_by_model(input_file:str, md5sum:str):
    log_file = os.path.join(OUTPUT_DIR, f'{md5sum}.log')
    os.system(f'{MODEL_prediction_script} {input_file} {OUTPUT_DIR} {THREADS} {MODEL_FILE} {FEATURE_FILE} {md5sum} > {log_file} 2>&1')

st.set_page_config(
    page_title="Lung Nodule",
    page_icon="🫁",
)

PROJECT_DIR = '.'
MODEL_prediction_script = f'{PROJECT_DIR}/scripts/caret_exist_model_predict.R'
OUTPUT_DIR = f'{PROJECT_DIR}/model_data/LungNodule_output'
THREADS = 10
MODEL_FILE = f'{PROJECT_DIR}/model_data/LungNodule_model/models_list.rds'
FEATURE_FILE = f'{PROJECT_DIR}/model_data/LungNodule_model/features.csv'

st.write('### Upload your TCR feature data')
uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    # Display the DataFrame
    st.write("#### Uploaded Data Preview:")
    st.write(df)
    st.write(f'**{len(df)}** samples uploaded')
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    input_file = save_uploaded_file(uploaded_file)
    md5_checksum = utils.calculate_md5(input_file)
    st.write(f'md5 checksum for your input file: **{md5_checksum}**')
    md5_checksum_file = os.path.join(OUTPUT_DIR, f'{md5_checksum}_input.csv')
    os.system(f'mv {input_file} {md5_checksum_file}')
    predict_by_model(md5_checksum_file, md5_checksum)
    get_results(OUTPUT_DIR, md5_checksum)

    
