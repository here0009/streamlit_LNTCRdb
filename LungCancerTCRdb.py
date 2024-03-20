import sys
import pandas as pd
import streamlit as st
import json
sys.path.append(f'{sys.path[0]}/..')
import utils
from utils import PROJECT_DIR
import plotly.express as px

CONFIG_FILE=f"{PROJECT_DIR}/datapath.json"
config_fhand = open(CONFIG_FILE, "r")
config_dict = json.load(config_fhand)


@st.cache_data()
def get_treemap_plot(): 
    df = pd.read_csv(TOP1000_ENRICHED_SEQ_DATA)
    fig = px.treemap(df, path=['Group','cdr3aa'], values='score', color='cdr3aa')
    fig.update_layout(margin=dict(t=30, l=0, r=0, b=0), template='simple_white', title='LungCancerTCRdb top1000 enriched seqs')
    st.plotly_chart(fig)

def plotly_bubble_plot(df, x_col, y_col, size_col, color_col):
    fig =  px.scatter(df, x=x_col, y=y_col,color=color_col,
                 size=size_col,opacity=0.65,color_discrete_sequence=Healthy_T_B_color_palette,width=800,height=500,
                 template='simple_white')
    fig.update_xaxes(showticklabels=True)
    fig.update_layout(margin = dict(t=30, l=0, r=0, b=0),
                 xaxis_visible=True, xaxis_showticklabels=True)
    return fig

@st.cache_data()
def lntcr_db_score_bubble_plot():
    df = pd.read_csv(LN_TCRDB_SCORE_DATA)
    fig1 = plotly_bubble_plot(df,  'sample', 'LUNG_CANCER_TISSUE_score','LUNG_CANCER_TISSUE_score', 'Type')
    fig2 = plotly_bubble_plot(df,  'sample','LUNG_CANCER_GDNA_score','LUNG_CANCER_GDNA_score', 'Type')
    return fig1, fig2

    
    

st.set_page_config(
    page_title="LungCancerTCRdb",
    page_icon="🏄‍♂️",
)

Healthy_T_B_color_palette = ['#00B945','#FF2C00', '#845B97']
st.sidebar.success("Choose from above")
PROJECT_DIR = '.'
LN_TCRDB_LOGO_FILE = f'{PROJECT_DIR}/img/lung-cancer-tcr-db-logo/svg/logo-no-background.svg'
TOP1000_ENRICHED_SEQ_DATA= f'{PROJECT_DIR}/img/img_data/LungCancerTCRdb_top1000_enriched_seqs.csv'
LN_TCRDB_SCORE_DATA = f'{PROJECT_DIR}/img/img_data/LungCancerTCRdb_score_tbl.csv'
LN_TCRDB_UMAP_PLOT = f'{PROJECT_DIR}/img/lungCancerTCRdb/LungCancerTCRdb_UMAP_plot.png'
LN_TCRDB_stat_index = f'{PROJECT_DIR}/img/lungCancerTCRdb/LungCancerTCRdb_stat_index.png'
LN_TCRDB_freq_group = f'{PROJECT_DIR}/img/lungCancerTCRdb/LungCancerTCRdb_TCR_freq_group3.png'
LN_TCRDB_mut_data = f'{PROJECT_DIR}/img/lungCancerTCRdb//MutationTop20_TCR_immune3.svg'

with open(LN_TCRDB_LOGO_FILE, 'r') as _f:
    svg = _f.read()
    st.image(svg, width=400)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Sample Info", "UMAP plot", "LungCancerTCRdb stat", "Enriched Seqs", "Mutation Info"])

with tab1:
    sample_info_df = pd.DataFrame({'Category':['Healthy Blood', 'Lung Cancer Blood', 'Lung Cancer Tissue'], 'Short':['Healthy', 'Cancer_B', 'Cancer_T'], 'Sample Number':[2699, 3360, 988]})
    st.dataframe(
        sample_info_df,    
        column_config={},
        hide_index=True,
    )
with tab2:
    st.image(LN_TCRDB_UMAP_PLOT, caption='UMAP plot for data in LungCancerTCRdb')
with tab3:
    st.image(LN_TCRDB_stat_index, caption='Stat index for LungCanerTCRdb')
    st.image(LN_TCRDB_freq_group, caption='Freq Gruop for data in LungCancerTCRdb')
with tab4:
    get_treemap_plot()
    col1, col2 = st.tabs(['Lung Cancer Tissue Score', 'Lung Cancer Blood Score'])
    fig1, fig2 = lntcr_db_score_bubble_plot()
    with col1: 
        st.plotly_chart(fig1, theme="streamlit")
    with col2:
        st.plotly_chart(fig2, theme="streamlit")

with tab5:
    st.image(LN_TCRDB_mut_data, width=800, caption='Mutation information for LungCancerTCRdb')
