import sys
import pandas as pd
import streamlit as st
import json
sys.path.append(f'{sys.path[0]}/..')
import utils
from utils import PROJECT_DIR, RUNNING, LN_TCRDB_LOGO_FILE
import plotly.express as px

CONFIG_FILE=f"{PROJECT_DIR}/datapath.json"
config_fhand = open(CONFIG_FILE, "r")
config_dict = json.load(config_fhand)


@st.cache_data()
def get_treemap_plot(): 
    df = pd.read_csv(TOP1000_ENRICHED_SEQ_DATA)
    fig = px.treemap(df, path=['Group','cdr3aa'], values='score', color='cdr3aa')
    fig.update_layout(margin=dict(t=20, l=0, r=0, b=60), template='simple_white', title={'text':'LungCancerTCRdb top1000 enriched seqs', 'y':0.1, 'x':0.3, 'font':{'size':14, 'color':'rgba(49, 51, 63, 0.6)'}}, 
    title_font_color='rgba(49, 51, 63, 0.6)', 
    title_font_size=14,
    font_family="Arial", title_font_family="Arial", width=800)
    st.plotly_chart(fig)

def plotly_bubble_plot(df, x_col, y_col, size_col, color_col):
    fig =  px.scatter(df, x=x_col, y=y_col,color=color_col,
                 size=size_col,opacity=0.65,color_discrete_sequence=Healthy_T_B_color_palette,width=500,height=400,
                 template='simple_white')
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(margin = dict(t=30, l=0, r=0, b=0),
                 xaxis_visible=True, xaxis_showticklabels=True,width=500)
    return fig

# @st.cache_data()
def score_scatter_plot(input_tbl, x_col, y_col, size_col, color_col, facet_col, title):
    fig = px.scatter(input_tbl, x=x_col, y=y_col, size=size_col, opacity=0.5,color=color_col,
                 color_discrete_sequence=Healthy_T_B_color_palette,
                 template='ygridoff', facet_col=facet_col, facet_col_wrap=2, width=1000, height=600)
    for axis in fig.layout:
       if axis.startswith("xaxis") or axis.startswith("yaxis"):
          fig.layout[axis].title = ""
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_xaxes(visible=False)
    fig.update_layout(
        margin_autoexpand=True, font_family="Arial",title_font_family="Arial",
        title=title,
        margin=dict(l=30,r=30,b=80,t=100,
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        showlegend=True
    )
    return fig

# @st.cache_data()
# def lntcr_db_score_bubble_plot():
#     df = pd.read_csv(LN_TCRDB_SCORE_DATA)
#     fig1 = plotly_bubble_plot(df,  'sample', 'LUNG_CANCER_TISSUE_score','LUNG_CANCER_TISSUE_score', 'Type')
#     fig2 = plotly_bubble_plot(df,  'sample','LUNG_CANCER_GDNA_score','LUNG_CANCER_GDNA_score', 'Type')
#     return fig1, fig2


st.set_page_config(
    page_title="LungCancerTCRdb",
    page_icon="🏄‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# with open( f"{PROJECT_DIR}/app/style.css" ) as css:
#     st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

Healthy_T_B_color_palette = ['#00B945','#FF2C00', '#845B97']
# st.sidebar.success("Choose from above")
PROJECT_DIR = '.'
WORK_FLOW_PLOT = f'{PROJECT_DIR}/img/lungCancerTCRdb/WorkFlowDiagram.png'
# LN_TCRDB_LOGO_FILE = f'{PROJECT_DIR}/img/lung-cancer-tcr-db-logo/svg/logo-no-background.svg'
TOP1000_ENRICHED_SEQ_DATA= f'{PROJECT_DIR}/img/img_data/LungCancerTCRdb_top1000_enriched_seqs.csv'
LN_TCRDB_SCORE_DATA = f'{PROJECT_DIR}/img/img_data/LungCancerTCRdb_score_tbl.csv'
LN_TCRDB_UMAP_PLOT = f'{PROJECT_DIR}/img/lungCancerTCRdb/LungCancerTCRdb_UMAP_plot.png'
LN_TCRDB_stat_index = f'{PROJECT_DIR}/img/lungCancerTCRdb/LungCancerTCRdb_stat_index.png'
LN_TCRDB_freq_group = f'{PROJECT_DIR}/img/lungCancerTCRdb/LungCancerTCRdb_TCR_freq_group3.png'
# LN_TCRDB_mut_data = f'{PROJECT_DIR}/img/lungCancerTCRdb//MutationTop20_TCR_immune3.svg'
LN_TCRDB_mut_data = f'{PROJECT_DIR}/img/lungCancerTCRdb//MutationTop20_TCR_immune3.png'

with open(LN_TCRDB_LOGO_FILE, 'r') as _f:
    svg = _f.read()
    # st.image(svg, width=400)
    st.sidebar.image(svg)

# sample_info_df = pd.DataFrame({'Category':['Healthy Blood', 'Lung Cancer Blood', 'Lung Cancer Tissue'], 'Short':['Healthy', 'Cancer_B', 'Cancer_T'], 'Sample Number':[2699, 3360, 988]})
# st.dataframe(
#         sample_info_df,    
#         column_config={},
#         hide_index=True,
#     ) 

# tab1, tab2, tab3, tab4, tab5 = st.tabs(["Sample Info", "UMAP plot", "LungCancerTCRdb stat", "Enriched Seqs", "Mutation Info"])
with open(LN_TCRDB_LOGO_FILE, 'r') as _f:
    svg = _f.read()
    st.image(svg, width=600)
introduction = """
### Introduction for LCTRDB
LCTRDB(Lung Cancer TCR Database) provides a comprehensive TCR repertoire data in lung cancer, including TCR clonotype frequency, TCR diversity, TRB V/J gene usage, and lung cancer-enriched CDR3 signatures. This database contains over 4,000 tissue/blood samples from lung cancer and over 2,500 peripheral blood samples from healthy individuals. 

Moreover, the tumor mutation profiles, PD-L1 expression and HLA genotypes of lung cancer were integrated with TCR characteristics, demonstrating an intrinsic relationship between tumor mutations and TCR repertoire. 

A predictive model was offered to users for evaluating the risk of lung cancer by inputting the TCR features matrix.
"""
overview = """
### Overview
* Display the difference in TCR repertoire between lung cancer and  healthy individuals.
* Identify the cancer-enriched CDR3 sequences.
* Calculate multiple TCR features and visualization.
* Analysis the correlation between tumor mutations and TCR characteristics.
* Construct the predictive model for evaluating risk of lung cancer.
"""
describe = """
### Study Summary
In LCTRDB study, we performed TCR β-chain sequencing using a multiplex PCR approach with the panels of V and J primers. The difference of CDR3 sequences between lung cancer (include tissue and blood) and healthy individuals was investigated. Significant difference in TCR shannon entropy, clonality, V/J gene usage, and clonotype was demonstrated.  

We identified thousands of unique CDR3 sequences which are specifically enriched in lung cancer tissue/blood. By applying these cancer-enriched TCR features, we developed a pipeline to measure the content of lung cancer-related TCRs by alignment.
"""
mutation = """
### Mutatioin Data
To characterize the mutation profile and calculate the Tumor Mutational Burden (TMB), whole-exome sequencing (WES) was conducted on partial lung cancer tissue specimens. 

HLA Genotyping was also determined by whole exome sequencing. HLA evolutionay divergence (HED) was calculated by midasHLA, with the averge HLA evolutionay divergence of HLA-A, HLA-B and HLA-C loci used as the final HED score.

PD-L1 expression was determined by immunohistochemistry (IHC) on formalin-fixed paraffin-embedded (FFPE) tissue sections. PD-L1 expression levels were categorized into three groups based on the tumor proportion score(TPS): Neagtive(TPS ≤  1%), low expression(1% < TPS expression ≤ 50%), and high expression(TPS > 50%)
"""
col_intro_1, col_intro_2 = st.columns((4,6))
with col_intro_1:
    st.write(introduction)
with col_intro_2:
    st.image(WORK_FLOW_PLOT, caption='Study workflow', width=800)
st.divider()
col_treemap_1, col_treemap_2 = st.columns((4, 6))
with col_treemap_1:
    st.write(overview)
with col_treemap_2:
    get_treemap_plot()
st.divider()
col_feature_1, col_feature_2 = st.columns((4,6))
with col_feature_1:
    st.write(describe)
    
with col_feature_2:
    # st.image(LN_TCRDB_stat_index, caption='Stat index for LungCanerTCRdb')
    st.image(LN_TCRDB_UMAP_PLOT, caption='UMAP plot for data in LungCancerTCRdb', width=800)
    
    
# st.divider()
# col_group_1, col_group_2 = st.columns((5,5))
# with col_group_1:
#     st.image(LN_TCRDB_freq_group)
# with col_group_2:
#     st.image(LN_TCRDB_stat_index, width=700)
    # st.image(LN_TCRDB_freq_group, caption='Freq Gruop for data in LungCancerTCRdb')

    # col1, col2 = st.tabs(['Lung Cancer Tissue Score', 'Lung Cancer Blood Score'])
# st.divider()
# col_enrich_1, col_enrich_2 = st.columns((1, 4))
# enrich_score_tbl = pd.read_csv(LN_TCRDB_SCORE_DATA)
# enrich_fig = score_scatter_plot(enrich_score_tbl, 'sample', 'score', 'score', 'Type', 'Group', 
#                    'LCT score and LCB score for LungCancerTCRdb samples')
# with col_enrich_1:
#     st.write('#### Enriched Score')
# with col_enrich_2: 
#     st.plotly_chart(enrich_fig)

st.divider()
col_mut1, col_mut2 = st.columns((4, 6))
with col_mut1:
    st.write(mutation)
with col_mut2:
    st.image(LN_TCRDB_mut_data, caption='Mutation information for LungCancerTCRdb', width=800)
