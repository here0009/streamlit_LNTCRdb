import streamlit as st
import os
import sys
import pandas as pd
sys.path.append(f'{sys.path[0]}/..')
import utils
from utils import PROJECT_DIR
import plotly.express as px
import plotly.graph_objects as go
from utils import PROJECT_DIR, RUNNING, LN_TCRDB_LOGO_FILE


@st.cache_data(max_entries=100)
def pred_boxplot(pred_val_tbl, method_lst, color_lst, type_info):
    fig = go.Figure()
    if type_info == 'type':
        for method, color in zip(method_lst, color_lst):
            fig.add_trace(go.Box(x=pred_val_tbl['Type'],y=pred_val_tbl[method],name=method,marker_color=color,boxpoints='all',jitter=0.5,whiskerwidth=0.2,marker_size=2,line_width=1))
    else:
        for method, color in zip(method_lst, color_lst):
            fig.add_trace(go.Box(y=pred_val_tbl[method],name=method,marker_color=color,boxpoints='all',jitter=0.5,whiskerwidth=0.2,marker_size=2,line_width=1))
    fig.update_layout(
        title='Prediction score of different methods',
        # yaxis=dict(autorange=True,showgrid=True,zeroline=True,dtick=0.2,gridcolor='rgb(255, 255, 255)',
        #         gridwidth=1,zerolinecolor='rgb(255, 255, 255)',zerolinewidth=2,),
        margin=dict(l=30,r=30,b=80,t=100,
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        showlegend=True,
        width=1200
    )
    if type_info == 'type':
        fig.update_layout(boxmode='group',)
    return fig


def get_results(output_dir, md5_tag, type_info):
    pred_val_file = os.path.join(output_dir, f'{md5_tag}_pred_val.csv')
    st.write("### Results")
    pred_val_tbl = pd.read_csv(pred_val_file)
    st.write("#### Prediction value")
    st.dataframe(pred_val_tbl, hide_index=True, width=700)
    prediction_val_fig = pred_boxplot(pred_val_tbl, METHOD_LST, NATURE_COLORS, type_info)
    st.plotly_chart(prediction_val_fig)
    if type_info == 'type':
        roc_plot = os.path.join(output_dir, f'{md5_tag}_roc.svg')
        model_metric_file = os.path.join(output_dir, f'{md5_tag}_model_metric.csv')
        roc_file = os.path.join(output_dir, f'{md5_tag}_roc.csv')
        roc_tbl = pd.read_csv(roc_file)
        model_metric_tbl = pd.read_csv(model_metric_file)
        model_metric_tbl = model_metric_tbl.rename(columns={'Unnamed: 0':'Metrics'})
        model_metric_tbl.set_index('Metrics', inplace=True)
        st.write("#### Model metrics")
        st.dataframe(model_metric_tbl.T)
        st.write("#### ROC curve")
        st.dataframe(roc_tbl)
        with open(roc_plot, 'r') as _f:
            svg = _f.read()
            st.image(svg)

@st.cache_data(show_spinner="Processing...", max_entries=100)
def predict_by_model(input_file:str, md5sum:str, type_info:str):
    log_file = os.path.join(OUTPUT_DIR, f'{md5sum}.log')
    os.system(f'{MODEL_prediction_script} {input_file} {OUTPUT_DIR} {THREADS} {MODEL_FILE} {FEATURE_FILE} {md5sum} {type_info} > {log_file} 2>&1')


def run_model(input_file, type_info):
    md5_checksum = utils.calculate_md5(input_file)
    st.write(f'md5 checksum for your input file: **{md5_checksum}**')
    md5_checksum_file = os.path.join(OUTPUT_DIR, f'{md5_checksum}_input.csv')
    os.system(f'cp {input_file} {md5_checksum_file}')
    if type_info == 'Yes':
        predict_by_model(md5_checksum_file, md5_checksum, 'type')
        get_results(OUTPUT_DIR, md5_checksum, 'type')
    else:
        predict_by_model(md5_checksum_file, md5_checksum, 'score')
        get_results(OUTPUT_DIR, md5_checksum, 'score')



st.set_page_config(
    page_title="Model Prediction",
    page_icon="🧠",
    layout="wide"
)

with open( f"{PROJECT_DIR}/app/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

PROJECT_DIR = '.'
THREADS = 3
METHOD_LST = ['rf', 'gbm', 'glmnet', 'svmLinear', 'svmRadial']
NATURE_COLORS = ['#0C5DA5', '#00B945', '#FF9500', '#FF2C00', '#845B97', '#474747', '#9e9e9e']
description = """
This module can be applied for evaluating the risk of lung cancer or malignant lung nodule. Upload the TCR feature table according to the required format (see document), the prediction probability for each sample will be generated. If the group label is available in the input file, ROC curve and model performance will also be presented.
"""

st.sidebar.image(utils.LN_TCRDB_LOGO_FILE, width=200)
    
st.markdown(utils.header_font.format("Model Prediction"), unsafe_allow_html=True)
col_intro_1, col_intro_2 = st.columns((4,6))
with col_intro_1:
    st.markdown(utils.content_font.format(description), unsafe_allow_html=True)
with col_intro_2:
    pass
col_select_1, col_select_2, col_select_3 = st.columns((1, 1, 1))
with col_select_1:
    model = st.radio(
        '**Select Model**',
        options = ['Lung Cancer Model', 'Lung Nodule Model']
    )
    # st.write('Your selection:', model)
if model == 'Lung Cancer Model':
    MODEL_prediction_script = f'{PROJECT_DIR}/scripts/lungCancer_model_predict.R'
    OUTPUT_DIR = f'{PROJECT_DIR}/model_data/LungCancer_output'
    MODEL_FILE = f'{PROJECT_DIR}/model_data/LungCancer_model/models_list.rds'
    FEATURE_FILE = f'{PROJECT_DIR}/model_data/LungCancer_model/features.csv'
    TEST_DATA_FILE = f'{PROJECT_DIR}/model_data/LungCancer_model/test_data_concise.csv'
    type_info_hint = '**Is sample type information available(Cancer/Healthy)**'
elif model == 'Lung Nodule Model':
    MODEL_prediction_script = f'{PROJECT_DIR}/scripts/caret_exist_model_predict.R'
    OUTPUT_DIR = f'{PROJECT_DIR}/model_data/LungNodule_output'
    MODEL_FILE = f'{PROJECT_DIR}/model_data/LungNodule_model/models_list.rds'
    FEATURE_FILE = f'{PROJECT_DIR}/model_data/LungNodule_model/features.csv'
    TEST_DATA_FILE = f'{PROJECT_DIR}/model_data/LungNodule_model/lungNodule_val_data_concise.csv'
    type_info_hint = '**Is sample type information available(Malignant/Benign)**'
 
# type_info = st.selectbox(
#     type_info_hint,
#     ('Yes', 'No'))
with col_select_2:
    type_info = st.radio(
        type_info_hint,
        options = ['Yes', 'No']
    )

st.divider()
on = st.toggle('Show Example Data')
if on:
# if st.button('Show Example Data'):
    if model == 'Lung Nodule Model':
        st.markdown(utils.small_font.format('Sample_ID and TCR features in the table below were required for Lung Nodule Model.'), unsafe_allow_html=True)
    st.markdown(utils.small_font.format('TCR features could be generated by:'), unsafe_allow_html=True)
    st.markdown('<p style="color:Green; font-size: 12px; font-family: Arial;"><a href="/TCR_Features_Calculation" target="_self">TCR features calculation</a></p>', unsafe_allow_html=True)
    test_data_tbl = pd.read_csv(TEST_DATA_FILE)
    st.dataframe(
        test_data_tbl,
        column_config={
        },
        hide_index=True,
    )
    if st.button('Show Example Result'):
        run_model(TEST_DATA_FILE, type_info)
    st.divider()


st.markdown(utils.sub_header_font.format("Upload your TCR feature data(csv format)"),unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=['csv'])

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    # Display the DataFrame
    st.markdown(utils.sub_header_font.format("Upload your TCR feature data(csv format)"), unsafe_allow_html=True)
    st.markdown(utils.content_font.format("Uploaded Data Preview:"), unsafe_allow_html=True)
    st.write(df)
    st.write(f'**{len(df)}** samples uploaded')
    if RUNNING:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        input_file = utils.save_uploaded_file(uploaded_file, OUTPUT_DIR)
        run_model(input_file, type_info)
    else:
        st.write(f'Module not available for now')
