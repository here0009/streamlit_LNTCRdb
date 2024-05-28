import sys
import os
import streamlit as st
import pandas as pd
sys.path.append(f'{sys.path[0]}/..')
import plotly.express as px
import plotly.graph_objects as go
import utils
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from utils import PROJECT_DIR, RUNNING, LN_TCRDB_LOGO_FILE



def stack_bar_plot(input_tbl, plot_title):
    color_lst = ['#e2514a', '#fca55d', '#fee999', '#edf8a3', '#a2d9a4', '#47a0b3']
    fig = go.Figure(data=[
        go.Bar(name='rare', x=input_tbl['Sample_ID'], y=input_tbl['rare'],  marker_color=color_lst[0]),
        go.Bar(name='small', x=input_tbl['Sample_ID'], y=input_tbl['small'],  marker_color=color_lst[1]),
        go.Bar(name='medium', x=input_tbl['Sample_ID'], y=input_tbl['medium'],  marker_color=color_lst[2]),
        go.Bar(name='large', x=input_tbl['Sample_ID'], y=input_tbl['large'],  marker_color=color_lst[4]),
        go.Bar(name='expanded', x=input_tbl['Sample_ID'], y=input_tbl['expanded'],  marker_color=color_lst[5])
    ])
    # Change the bar mode
    fig.update_layout(barmode='stack')
    fig.update_layout(margin = dict(t=25, l=40, r=40, b=0),width=1200,
                    #margin_autoexpand=True,
                    font_family="Arial",title_font_family="Arial",
                            title=plot_title,autosize=True,showlegend=True,template='xgridoff', xaxis_visible=False, yaxis_visible=False, xaxis_showticklabels=False)
    return fig

def sns_multiple_box_plots_single(input_table, val_cols, color_lst, super_title):
    length = len(val_cols)
    # sns.set(rc={'figure.facecolor':(0,0,0,0), 'figure.backgroundcolor':(0,0,0,0)})
    sns.set_theme(rc={'figure.facecolor':(0,0,0,0), 'axes.facecolor':(0,0,0,0)}, font_scale=2)
    fig, axes = plt.subplots(1, length, figsize=(5*length,8))
    fig.suptitle(super_title)
    for i in range(length):
        sns.boxplot(ax=axes[i], data=input_table, y=val_cols[i], boxprops={'alpha': 0.6},showfliers=False,fill=False,color=color_lst[i],gap=0.2,linewidth=3,
                   ).set(xlabel=None)
        sns.stripplot(ax=axes[i], data=input_table, y=val_cols[i],color=color_lst[i],alpha = 0.7, size=7).set(ylabel=val_cols[i], xlabel=None)
    fig.tight_layout()

    return fig

def plotly_boxplot(input_tbl, col_lst, color_lst, title):
    length = len(col_lst)
    fig = make_subplots(rows=1, cols=length)
    for i, _col in enumerate(col_lst):
        fig.add_trace(
            go.Box(y=input_tbl[_col],
            name=_col,
            marker_color=color_lst[i],boxpoints='all',
            marker_size=2,line_width=1),
            row=1, col=i+1,

        )
    fig.update_layout(
        title=title,
        # yaxis=dict(autorange=True,showgrid=True,zeroline=True,dtick=0.2,gridcolor='rgb(255, 255, 255)',
        #         gridwidth=1,zerolinecolor='rgb(255, 255, 255)',zerolinewidth=2,),
        margin=dict(l=30,r=30,b=80,t=100,
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        showlegend=True,
        width=1200,
        boxgap = 0.5
    )
    return fig

def get_group_freq_col(total_result_info_table):
    total_result_info_table['expanded'] = total_result_info_table['group_freq_2']
    total_result_info_table['large'] = total_result_info_table['group_freq_3']
    total_result_info_table['medium'] = total_result_info_table['group_freq_4']
    total_result_info_table['small'] = total_result_info_table['group_freq_5']
    total_result_info_table['rare'] = total_result_info_table['group_freq_7'] + total_result_info_table['group_freq_6']
    return total_result_info_table

def show_meta_table(meta_file):
    meta_tbl = pd.read_csv(meta_file, sep='\t')
    meta_tbl['file_name'] = meta_tbl['file_name'].map(os.path.basename)
    st.dataframe(meta_tbl,hide_index=True, width=900)

# @st.cache_data(show_spinner="Processing...", max_entries=100) 
def get_tcr_features(input_file, output_dir):
    tcr_feature_data = os.path.join(output_dir, 'all_combined_stat.csv')
    if os.path.exists(f'{output_dir}/metadata.tsv'):
        show_meta_table(f'{output_dir}/metadata.tsv')
    else:
        os.system(f'unzip -o {input_file} -d {output_dir}/metadata/')
        os.system(f'{GET_METADATA_SCRIPT} {output_dir}/metadata/ {output_dir}/metadata.tsv')
        show_meta_table(f'{output_dir}/metadata.tsv')
    if os.path.exists(tcr_feature_data):
        return tcr_feature_data
    os.system(f'bash {STAT_SCRIPT} {output_dir}/metadata.tsv {output_dir} {THREADS}')
    return tcr_feature_data

def run_model(input_file):
    md5_checksum = utils.calculate_md5_zip(input_file)
    st.write(f'md5 checksum for your input file: **{md5_checksum}**')
    md5_checksum_file = os.path.join(OUTPUT_DIR, f'{md5_checksum}.zip')
    os.system(f'cp {input_file} {md5_checksum_file}')
    _dir = os.path.realpath(os.path.join(OUTPUT_DIR, md5_checksum))
    os.makedirs(_dir, exist_ok=True)
    tcr_feature_file = get_tcr_features(md5_checksum_file, _dir)
    tcr_feature_tbl = pd.read_csv(tcr_feature_file)
    st.dataframe(
        tcr_feature_tbl,
        column_config={
        },
        hide_index=True,
    )
    tcr_feature_tbl = get_group_freq_col(tcr_feature_tbl)
    tcr_feature_tbl.rename(columns=STAT_RENAME_DICT, inplace=True)
    group_plot = stack_bar_plot(tcr_feature_tbl, 'cdr3aa freq distribution')
    st.plotly_chart(group_plot, height=600, width=900)
    # stat_plot = sns_multiple_box_plots_single(tcr_feature_tbl, STAT_COLS, NATURE_COLORS, 'stat index box plots')
    # score_plot = sns_multiple_box_plots_single(tcr_feature_tbl, SCORE_COLS, NATURE_COLORS, 'score box plots')
    # st.pyplot(stat_plot)
    # st.pyplot(score_plot)
    stat_plot = plotly_boxplot(tcr_feature_tbl, STAT_COLS, NATURE_COLORS, 'stat index box plots')
    score_plot = plotly_boxplot(tcr_feature_tbl, SCORE_COLS, NATURE_COLORS, 'score box plots')
    st.plotly_chart(stat_plot)
    st.plotly_chart(score_plot)


st.set_page_config(
    page_title="Features Analysis",
    page_icon="💻",
    layout="wide"
)
with open( f"{PROJECT_DIR}/app/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    
OUTPUT_DIR = f'{PROJECT_DIR}/model_data/FeaturesCalculation_output'
THREADS = 10
GET_METADATA_SCRIPT = f'{PROJECT_DIR}/scripts/get_metadata.py'
STAT_SCRIPT = f'{PROJECT_DIR}/scripts/stat_from_metadata.sh'
TEST_DATA_FILE = f'{PROJECT_DIR}/model_data/FeaturesCalculation_data/test.clonotypes.TRB.txt'
TEST_META_ZIP_DATA = f'{PROJECT_DIR}/model_data/FeaturesCalculation_data/metadata2.zip'
TEST_META_DATA = f'{PROJECT_DIR}/model_data/FeaturesCalculation_data/metadata2.csv'
stat_cols_org = ['observedDiversity_mean','d50Index_mean','shannonWienerIndex_mean','normalizedShannonWienerIndex_mean','inverseSimpsonIndex_mean']
# SCORE_COLS = ['KRAS_score','EGFR_score','REF_score','LUNG_CANCER_GDNA_score','LUNG_CANCER_TISSUE_score','Convergence_score']
score_cols_org = ['REF_score','LUNG_CANCER_GDNA_score','LUNG_CANCER_TISSUE_score','Convergence_score']
TYPE_COLS = ['KRAS_type','EGFR_type','REF_type','LUNG_CANCER_GDNA_type','LUNG_CANCER_TISSUE_type','Convergence_type']
GROUP_COLS = ['group_freq_2','group_freq_3','group_freq_4','group_freq_5','group_freq_6','group_freq_7']
GROUP_COLS2 = ['expanded','large','medium','small', 'rare']
NATURE_COLORS = ['#0C5DA5', '#00B945', '#FF9500', '#FF2C00', '#845B97', '#474747', '#9e9e9e']
STAT_RENAME_DICT = {'observedDiversity_mean':'Diversity','d50Index_mean':'d50Index','shannonWienerIndex_mean':'shannonWienerIndex','normalizedShannonWienerIndex_mean':'Evenness','inverseSimpsonIndex_mean':'inverseSimpsonIndex','REF_score':'Public_score','LUNG_CANCER_GDNA_score':'LCB_score','LUNG_CANCER_TISSUE_score':'LCT_score'}

STAT_COLS = ['Diversity','d50Index','shannonWienerIndex','Evenness','inverseSimpsonIndex']
SCORE_COLS = ['Public_score','LCB_score','LCT_score','Convergence_score']

description = """
This module can be applied for general analysis of TCR repertoire.
Upload the TCR clonotype file according to the required format (see Document), several TCR features will be calculated and output, including multiple diversity index, V/J gene usage, clonotype fraction, convergence, and cancer-enriched score.
"""


# type_info = st.selectbox(
#     '**Is sample type information available(Malignant/Benign for Lung Nodule samples, Cancer/Healthy for Lung Cancer samples)**',
#     ('Yes', 'No'))
# st.write('You selected:', type_info)

st.sidebar.image(utils.LN_TCRDB_LOGO_FILE, width=200)

st.markdown(utils.header_font.format('Feature Analysis'), unsafe_allow_html=True)

col_intro_1, col_intro_2 = st.columns((4,6))
with col_intro_1:
    st.markdown(utils.content_font.format(description), unsafe_allow_html=True)
with col_intro_2:
    pass
st.divider()
on = st.toggle('## Show Example Data')
if on:
# if st.button('Show Example Data'):
    st.markdown(utils.small_font.format('Zipped Clonotype files were required for TCR features calculation.'), unsafe_allow_html=True)
    st.markdown(utils.small_font.format('Clonotype files could be generated by:'), unsafe_allow_html=True)
    st.markdown('<p style="color:Green; font-size: 12px; font-family: Arial;"><a href="https://vdjtools-doc.readthedocs.io/en/master/input.html" target="_self">VDJtools</a></p>', unsafe_allow_html=True)
    test_data_tbl = pd.read_csv(TEST_DATA_FILE, sep='\t')
    if st.button('Show Example Result'):
        meta_tbl = pd.read_csv(TEST_META_DATA, sep='\t')
        # st.dataframe(
        #     meta_tbl,
        #     column_config={
        #     },
        #     hide_index=True, width=900
        # )
        run_model(TEST_META_ZIP_DATA)
    st.divider()

st.markdown(utils.sub_header_font.format('Upload your TCR clonotype files'), unsafe_allow_html=True)

uploaded_file = st.file_uploader('', type=['zip'])
if uploaded_file is not None:
    # st.write("#### Uploaded Data Preview:")
    # st.write(df)
    # st.write(f'**{len(df)}** samples uploaded')
    if RUNNING:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        input_file = utils.save_uploaded_file_zip(uploaded_file, OUTPUT_DIR)
        # input_file = zipfile.ZipFile(uploaded_file)
        run_model(input_file)

    else:
        st.write(f'Module not available for now')
