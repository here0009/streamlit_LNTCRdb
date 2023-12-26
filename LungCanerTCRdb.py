import sys
import pandas as pd
import streamlit as st
import json
sys.path.append(f'{sys.path[0]}/..')
import utils
from utils import PROJECT_DIR

CONFIG_FILE=f"{PROJECT_DIR}/datapath.json"
config_fhand = open(CONFIG_FILE, "r")
config_dict = json.load(config_fhand)


st.set_page_config(
    page_title="LungCancerTCRdb",
    page_icon="🏄‍♂️",
)


st.sidebar.success("Choose from above")
PROJECT_DIR = '.'
LN_TCRDB_LOGO_FILE = f'{PROJECT_DIR}/img/lung-cancer-tcr-db-logo/svg/logo-no-background.svg'
TOP1000_ENRICHED_SEQ = f'{PROJECT_DIR}/img/lungCancerTCRdb/4.3_LungCancerTCRdb_top1000_enriched_seq.png'
LN_TCRDB_UMAP_PLOT = f'{PROJECT_DIR}/img/lungCancerTCRdb/4.2_LungCancerTCRdb_UMAP_feautre_reduction.png'
LN_B_enrich_score = f'{PROJECT_DIR}/img/lungCancerTCRdb/4.5.3_LungCancerTCRdb_LungCancer_tissue_score.png'
LN_T_enrich_score = f'{PROJECT_DIR}/img/lungCancerTCRdb/4.5.4_LungCancerTCRdb_LungCancer_gdna_score.png'
LN_TCRDB_freq_group = f'{PROJECT_DIR}/img/lungCancerTCRdb/6.4_LungCancerTCRdb_freq_group.png'
LN_TCRDB_freq_group2 = f'{PROJECT_DIR}/img/lungCancerTCRdb/6.4.2_LungCancerTCRdb_freq_group.png'
LN_TCRDB_stat_index = f'{PROJECT_DIR}/img/lungCancerTCRdb/6.3.1_LungCancerTCRdb_stat_index.png'
LN_TCRDB_mut_data = f'{PROJECT_DIR}/img/lungCancerTCRdb/mut_preview_25.svg'

with open(LN_TCRDB_LOGO_FILE, 'r') as _f:
    svg = _f.read()
    st.image(svg, width=400)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Sample Info", "UMAP plot", "LungCancerTCRdb stat", "Enriched Seqs", "Mutation Info"])

with tab1:
    sample_info_df = pd.DataFrame({'Category':['Healthy Blood', 'Lung Cancer Blood', 'Lung Cancer Tissue'], 'Sample Number':[2699, 3360, 988]})
    st.dataframe(
        sample_info_df,    
        column_config={},
        hide_index=True,
    )
with tab2:
    st.image(LN_TCRDB_UMAP_PLOT, caption='UMAP plot for data in LungCancerTCRdb')
with tab3:
    st.image(LN_TCRDB_stat_index, caption='Stat index for LungCanerTCRdb')
    st.image(LN_TCRDB_freq_group)
    st.image(LN_TCRDB_freq_group2, caption='Freq Gruop for data in LungCancerTCRdb')
with tab4:
    st.image(TOP1000_ENRICHED_SEQ, caption='Top 1000 enriched seqs for LungCancerTCRdb')
    col1, col2 = st.columns(2)
    with col1: 
        st.image(LN_B_enrich_score, caption='Lung Cancer Blood enrich score')
    with col2:
        st.image(LN_T_enrich_score, caption='Lung Cancer Tissue enrich score')
with tab5:
    st.image(LN_TCRDB_mut_data)
# st.image([LN_B_enrich_score, LN_T_enrich_score], use_column_width=True)

