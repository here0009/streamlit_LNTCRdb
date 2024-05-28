import streamlit as st
import json
import pandas as pd
import sys
sys.path.append(f'{sys.path[0]}/..')
import utils
import plotly.graph_objects as go
import plotly.express as px
import utils
import matplotlib.pyplot as plt
import numpy as np
from plotly.subplots import make_subplots
from utils import PROJECT_DIR, RUNNING, LN_TCRDB_LOGO_FILE, Healthy_T_B_colors
pd.options.display.float_format = '{:.2f}'.format


def plotly_barplot(input_tbl, group_col, val_col):
    fig = px.histogram(input_tbl, x=val_col, color=group_col, opacity=0.75, barmode='group', color_discrete_sequence=NATURE_COLORS)
    fig.update_layout(
        margin=dict(l=30,r=30,b=80,t=100,
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        showlegend=True,
        width=1200,
        bargap=0.1,
    )
    fig.update_xaxes(tickfont_family='Arial')
    return fig
    
def plotly_boxplot(input_tbl, group_col, group_vals, col_lst, color_lst):
    length = len(col_lst)
    fig = make_subplots(rows=1, cols=length, subplot_titles=col_lst)
    for j, _gval in enumerate(group_vals):
        _tbl = input_tbl[input_tbl[group_col] == _gval]
        for i, _col in enumerate(col_lst):
            fig.add_trace(
                go.Box
                (
                x=_tbl[group_col],
                y=_tbl[_col],
                name=_col,
                # marker=dict(opacity=0),
                marker_color=color_lst[j],
                boxpoints='outliers',
                # boxpoints=False,
                marker_size=2,line_width=1
                ),
                row=1, col=i+1,
            )
    fig.update_layout(
        margin=dict(l=30,r=30,b=80,t=100,
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        showlegend=False,
        width=1500,
        boxgap = 0.5
    )
    fig.update_xaxes(tickfont_family='Arial')
    
    return fig

def mutliple_boxplots(input_tbl, group_col, value_lst, color_lst, title):
    fig = go.Figure()
    for val, color in zip(value_lst, color_lst):
        fig.add_trace(go.Box(x=input_tbl[group_col],y=input_tbl[val],name=val,marker_color=color,boxpoints='all',
                            jitter=0.5,whiskerwidth=0.2,marker_size=2,line_width=1))

    fig.update_layout(
        title=title,
        margin=dict(l=30,r=30,b=80,t=100,
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        showlegend=True,
        width=1200
    )
    fig.update_layout(boxmode='group',)
    return fig

def get_enrich_seq_tbl(input_file:str):
    input_tbl = pd.read_csv(input_file)
    input_tbl['score'] = input_tbl['score'].map(float)
    input_tbl['count'] = input_tbl['count'].map(int)
    return input_tbl
    
def tbl_visulizer(input_tbl:pd.DataFrame, default_visulize_cols):
    value_cols = input_tbl.columns.tolist()
    group_col = 'Type'
    not_evaluated_cols = set([group_col, 'Sample_ID', 'Sample_Type', 'Type'])
    value_cols = [_v for _v in value_cols if _v not in not_evaluated_cols]
    options = st.multiselect("**Columns for box plots visulization(less than 5)**", value_cols, default_visulize_cols, max_selections=5)
    group_vals = input_tbl[group_col].unique().tolist()
    if len(options) > 0:
        img = plotly_boxplot(input_tbl, group_col, group_vals, options,  Healthy_T_B_colors)
        st.plotly_chart(img)


def tbl_histgram_visulizer(input_tbl:pd.DataFrame):
    value_cols = input_tbl.columns.tolist()
    not_evaluated_cols = set(['Sample_ID'])
    col_1, col_2, _, _ = st.columns((1,1,1, 1))
    cols = [_v for _v in value_cols if _v not in not_evaluated_cols]
    group_col_candi = ['Sample_Type','Type','Sex','Disease']
    with col_1:
        group_col = st.selectbox("Group Column", group_col_candi, index=1)
    cols2 = [_v for _v in cols if _v != group_col]
    with col_2:
        value_col = st.selectbox("Value Column", cols2,  index=1)  
    img = plotly_barplot(input_tbl, group_col, value_col)
    st.plotly_chart(img)
    # options = st.multiselect("**Columns for box plots visulization(less than 5)**", value_cols, max_selections=3)
    # if len(options) > 0:
    #     img = plotly_mutli_barplot(input_tbl, options, NATURE_COLORS)
    #     st.plotly_chart(img)
    

# CONFIG_FILE=f"{PROJECT_DIR}/datapath.json"
# config_fhand = open(CONFIG_FILE, "r")
# config_dict = json.load(config_fhand)
NATURE_COLORS = ['#0C5DA5', '#00B945', '#FF9500', '#FF2C00', '#845B97', '#474747', '#9e9e9e']

st.set_page_config(
    page_title="Data Preview",
    page_icon="👁️",
    layout="wide"
)
with open( f"{PROJECT_DIR}/app/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    
st.sidebar.image(utils.LN_TCRDB_LOGO_FILE, width=200)
st.markdown(utils.header_font.format("Data Preview"), unsafe_allow_html=True)

description_lst = [
    "Clinical and sequencing information of LungTCR.",
"TCR characteristics of LungTCR.",
"Mutation profiles of lung cancer tissues in LungTCR.",
"Lung cancer tissue enriched CDR3 sequences, Lung cancer blood enriched CDR3 sequences, Healthy enriched CDR3 sequences and Super public CDR3 sequences."
]

col_intro_1, col_intro_2 = st.columns((4,6))
with col_intro_1:
    for _str in description_lst:
        st.markdown(utils.list_font.format(_str), unsafe_allow_html=True)

with col_intro_2:
    pass
st.divider()

st.markdown(utils.sub_header_font.format("Sample info and Data QC"), unsafe_allow_html=True)
# st.write("### Sample info and Data QC")

info1, info2 = st.tabs(["Sample Information", "Data QC"])
with info1:
    sample_info_file = f'{PROJECT_DIR}/metadata/features/sample_info.csv'
    sample_info_tbl = pd.read_csv(sample_info_file)
    st.dataframe(sample_info_tbl,column_config={},hide_index=True,width=800)
    tbl_histgram_visulizer(sample_info_tbl)
with info2:
    qc_file = f'{PROJECT_DIR}/metadata/features/data_qc.csv'
    qc_tbl = pd.read_csv(qc_file)
    st.dataframe(qc_tbl,column_config={},hide_index=True,)
    tbl_visulizer(qc_tbl, ['Raw_Yield(G)', 'V_primer_percent', 'J_primer_percent','merge_rate'])
st.divider()
st.markdown(utils.sub_header_font.format("TCR features"), unsafe_allow_html=True)
tcr_features_file = f'{PROJECT_DIR}/metadata/features/TCR_features.csv'
tcr_features_tbl = pd.read_csv(tcr_features_file)

st.dataframe(tcr_features_tbl,column_config={},hide_index=True,)
tbl_visulizer(tcr_features_tbl, ['observedDiversity', 'shannonWienerIndex', 'Evenness'])
st.divider()
LCT_enriched_seqs = f'{PROJECT_DIR}/metadata/features/LCT_enriched.csv'
LCB_enriched_seqs = f'{PROJECT_DIR}/metadata/features/LCB_enriched.csv'
Super_Pulic_seqs = f'{PROJECT_DIR}/metadata/features/Public.csv'
Healthy_enriched_seqs = f'{PROJECT_DIR}/metadata/features/Healthy_enriched.csv'

LCT_enriched_seqs_tbl = get_enrich_seq_tbl(LCT_enriched_seqs)
LCB_enriched_seqs_tbl = get_enrich_seq_tbl(LCB_enriched_seqs)
Super_Pulic_seqs_tbl = get_enrich_seq_tbl(Super_Pulic_seqs)
Healthy_enriched_seqs_tbl = get_enrich_seq_tbl(Healthy_enriched_seqs)

st.markdown(utils.sub_header_font.format("Enriched TCR sequences"), unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["Lung Cancer Tissue", "Lung Cancer Blood", "Super Public", "Healthy"])
# datbase_samples = {
#     'lcb':3443, 'lct':997, 'healthy':2710
# }
def get_config_dict(max_count, max_score):
    enriched_tbl_configs = { 
            "count": st.column_config.ProgressColumn(
            "count",
            format="%d",
            help="count for cdr3aa in dataset",
            min_value=0,
            max_value=max_count
        ),
            "score": st.column_config.ProgressColumn(
            "score",
            format="%.2f",
            help="score for cdr3aa in dataset",
            min_value=0,
            max_value=max_score
        ),
            "cdr3_len": st.column_config.ProgressColumn(
            "cdr3_len",
            format="%d",
            help="length for cdr3aa",
            min_value=0,
            max_value=21
        ),
    }
    return enriched_tbl_configs

def show_enrich_seq_tbl(input_tbl:pd.DataFrame):
    max_count, max_score = int(input_tbl['count'].max()), float(input_tbl['score'].max())
    st.dataframe(input_tbl, column_config=get_config_dict(max_count, max_score), hide_index=True, width=800)

with tab1:
    show_enrich_seq_tbl(LCT_enriched_seqs_tbl)
with tab2:
    show_enrich_seq_tbl(LCB_enriched_seqs_tbl)
with tab3:
    show_enrich_seq_tbl(Super_Pulic_seqs_tbl)
with tab4:
    show_enrich_seq_tbl(Healthy_enriched_seqs_tbl)

# st.divider()
mut_profile = f'{PROJECT_DIR}/metadata/features/Mutation_profile.csv'
mut_detail = f'{PROJECT_DIR}/metadata/features/Mutation_detail.csv'

mut_profile_tbl = pd.read_csv(mut_profile)
mut_detail_tbl = pd.read_csv(mut_detail)
st.markdown(utils.sub_header_font.format("Mutation and other information"), unsafe_allow_html=True)
mut1, mut2 = st.tabs(["TMB/HED/MSI/PD-L1", "Mutation"])
with mut1:
    st.dataframe(mut_profile_tbl, column_config={}, hide_index=True)
with mut2:
    st.dataframe(mut_detail_tbl, column_config={}, hide_index=True)