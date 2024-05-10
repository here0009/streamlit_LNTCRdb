import streamlit as st
import json
import pandas as pd
import sys
sys.path.append(f'{sys.path[0]}/..')
import utils
from utils import PROJECT_DIR, RUNNING, LN_TCRDB_LOGO_FILE


# CONFIG_FILE=f"{PROJECT_DIR}/datapath.json"
# config_fhand = open(CONFIG_FILE, "r")
# config_dict = json.load(config_fhand)
st.set_page_config(
    page_title="Data Preview",
    page_icon="👁️",
    layout="wide"
)
with open(LN_TCRDB_LOGO_FILE, 'r') as _f:
    svg = _f.read()
    # st.image(svg, width=400)
    st.sidebar.image(svg)
st.title("Data Preview")
description = """
* Clinical and sequencing information of LCTRDB.
* TCR characteristics of LCTRDB.
* Mutation profiles of lung cancer tissues in LCTRDB.
* Lung cancer tissue enriched CDR3 sequences, Lung cancer blood enriched CDR3 sequences, Healthy enriched CDR3 sequences and Super public CDR3 sequences.
"""
col_intro_1, col_intro_2 = st.columns((4,6))
with col_intro_1:
    st.write(description)
with col_intro_2:
    pass
st.divider()

st.title("Sample info and Data QC")


sample_info_file = f'{PROJECT_DIR}/metadata/features/sample_and_data_info.csv'
sample_info_tbl = pd.read_csv(sample_info_file)
st.dataframe(sample_info_tbl,column_config={},hide_index=True,)

st.title("TCR features")
tcr_features_file = f'{PROJECT_DIR}/metadata/features/TCR_features.csv'
tcr_features_tbl = pd.read_csv(tcr_features_file)
st.dataframe(tcr_features_tbl,column_config={},hide_index=True,)

LCT_enriched_seqs = f'{PROJECT_DIR}/metadata/features/LCT_enriched.csv'
LCB_enriched_seqs = f'{PROJECT_DIR}/metadata/features/LCB_enriched.csv'
Super_Pulic_seqs = f'{PROJECT_DIR}/metadata/features/Public.csv'
Healthy_enriched_seqs = f'{PROJECT_DIR}/metadata/features/Healthy_enriched.csv'

LCT_enriched_seqs_tbl = pd.read_csv(LCT_enriched_seqs)
LCB_enriched_seqs_tbl = pd.read_csv(LCB_enriched_seqs)
Super_Pulic_seqs_tbl = pd.read_csv(Super_Pulic_seqs)
Healthy_enriched_seqs_tbl = pd.read_csv(Healthy_enriched_seqs)

st.title("Enriched TCR sequences")
tab1, tab2, tab3, tab4 = st.tabs(["Lung Cancer Tissue", "Lung Cancer Blood", "Super Public", "Healthy"])
with tab1:
    st.dataframe(LCT_enriched_seqs_tbl, column_config={}, hide_index=True, width=600)
with tab2:
    st.dataframe(LCB_enriched_seqs_tbl, column_config={}, hide_index=True, width=600)
with tab3:
    st.dataframe(Super_Pulic_seqs_tbl, column_config={}, hide_index=True, width=600)
with tab4:
    st.dataframe(Healthy_enriched_seqs_tbl, column_config={}, hide_index=True, width=600)
    


mut_profile = f'{PROJECT_DIR}/metadata/features/Mutation_profile.csv'
mut_detail = f'{PROJECT_DIR}/metadata/features/Mutation_detail.csv'

mut_profile_tbl = pd.read_csv(mut_profile)
mut_detail_tbl = pd.read_csv(mut_detail)

st.title("Mutation and other information")
mut1, mut2 = st.tabs(["TMB/HED/MSI/PD-L1", "Mutaiion"])
with mut1:
    st.dataframe(mut_profile_tbl, column_config={}, hide_index=True)
with mut2:
    st.dataframe(mut_detail_tbl, column_config={}, hide_index=True)