import streamlit as st
from st_aggrid import AgGrid,GridOptionsBuilder,GridUpdateMode,DataReturnMode,ColumnsAutoSizeMode

import pandas as pd
from base64 import b64encode
import os
import sys
from zipfile import ZipFile
sys.path.append(f'{sys.path[0]}/..')
import utils
from utils import PROJECT_DIR


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=None).encode("utf-8")


def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True), "file_name":None},
        disabled=df.columns,width=600
    )
    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)

def download_files(selected_files):
    zip_file_name = 'selected_files.zip'
    with ZipFile(zip_file_name, 'w') as zipf:
        for file_name in selected_files:
            zipf.write(file_name, f'{os.path.basename(file_name)}')

    with open(zip_file_name, 'rb') as file:
        contents = file.read()
    b64 = b64encode(contents).decode()
    href = f'<a href="data:application/zip;base64,{b64}" download="{zip_file_name}">Click to download zip file</a>'
    st.markdown(href, unsafe_allow_html=True)

def select_data_download(meta_data_file:str, subtitle):
    st.markdown(utils.sub_header_font.format(subtitle), unsafe_allow_html=True)
    meta_tbl = utils.read_csv(meta_data_file)

    selection = dataframe_with_selections(meta_tbl)
    st.markdown(utils.sub_header_font.format("Selected"), unsafe_allow_html=True)
    st.dataframe(selection, column_config={"file_name":None}, width=600)
    checked_files = selection['file_name'].tolist()
    # st.write(checked_files)
    if st.button(f"Download Selected Files from {subtitle}") and len(checked_files) > 0:
        download_files(checked_files)

def request_download(meta_data_file:str, subtitle):
    st.markdown(utils.sub_header_font.format(subtitle), unsafe_allow_html=True)
    meta_tbl = utils.read_csv(meta_data_file)
    selection = dataframe_with_selections(meta_tbl)
    st.dataframe(selection, column_config={"file_name":None}, width=600)
    checked_files = selection['file_name'].tolist()
    # st.write(checked_files)
    if st.button(f"Download Request for {subtitle}") and len(checked_files) > 0:
        col1, col2, col3 = st.columns((1, 1, 1))
        with col1:
            st.text_input('Email')
            st.text_input('Name')
            st.text_input('Institue')
        with col2:
            with st.container():
                st.text_area('Research purpose', height=200)
        submision = st.button('Submit Request')

def request_download_agrid(meta_data_file:str, subtitle):
    st.markdown(utils.sub_header_font.format(subtitle), unsafe_allow_html=True)
    meta_tbl = utils.read_csv(meta_data_file)
    file_path_dict = dict(zip(meta_tbl['Sample_ID'], meta_tbl['file_name']))
    meta_tbl['file_name'] = meta_tbl['file_name'].map(os.path.basename)
    meta_tbl = meta_tbl[DOWNLOAD_TBL_COLS]
    gb = GridOptionsBuilder.from_dataframe(meta_tbl)
    # gb.configure_default_column(enablePivot=True, enableValue=True, min_column_width=200)
    # gb.configure_default_column(min_column_width=200, enableRowGroup=True)
    gb.configure_column("Sample_ID", width=500, headerCheckboxSelection=True, headerCheckboxSelectionFilteredOnly=True)
    gb.configure_column("Type", width=200)
    gb.configure_column("file_name", width=700)
    gb.configure_default_column(enableRowGroup=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    # gb.configure_side_bar()
    gridoptions = gb.build()
    custom_css = {
    ".ag-cell":{"font-size":'13px', "font-family":"Arial"}, # "background-color":"#F2FFE9", 
    ".ag-header-cell-label":{"font-size":'13px',  "font-family":"Arial"},
    ".ag-theme-alpine": {'--ag-background-color': '#F2FFE9', '--ag-header-background-color':'#97E7E1',  '--ag-font-family': 'Arial', '--ag-borders': 'none', '--ag-row-border-color': 'rgb(150, 150, 200)', '--ag-row-border-style': 'dashed',
                         '--ag-subheader-toolbar-background-color':'black'
                         },
    ".ag-root-wrapper": {"border": "none"},
    ".ag-root": {"background-color": "#F2FFE9", 'color': 'F2FFE9'},
    }
    response = AgGrid(
        meta_tbl,
        height=600,
        width='100%',
        gridOptions=gridoptions,
        # columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED,
        header_checkbox_selection_filtered_only=False,
        use_checkbox=True,
        checkboxSelection=True,
        headerCheckboxSelection=True,
        custom_css=custom_css,
        allow_unsafe_jscode=True,
        theme="alpine",
        )
    # options for theme: {'STREAMLIT': <AgGridTheme.STREAMLIT: 'streamlit'>, 'ALPINE': <AgGridTheme.ALPINE: 'alpine'>, 'BALHAM': <AgGridTheme.BALHAM: 'balham'>, 'MATERIAL': <AgGridTheme.MATERIAL: 'material'>}
    st.markdown(utils.sub_header_font.format("Selected"), unsafe_allow_html=True)
    v = response['selected_rows']
    # st.write(v)
    if not v is None:
        selected_tbl = pd.DataFrame(v)
        selected_tbl = selected_tbl[DOWNLOAD_TBL_COLS]
        st.dataframe(selected_tbl, width=1000)
        checked_files = [file_path_dict.get(_c, '') for _c in selected_tbl['Sample_ID'].tolist()]
        selected_num = len(checked_files)
        selected_num_str = f'{selected_num} files were selected'
        st.markdown(utils.content_font.format(selected_num_str), unsafe_allow_html=True)
        on = st.toggle('Show Download Request')
        # if st.button(f"Download Request for {subtitle}") and selected_num > 0:
        if on and selected_num > 0:
            col1, col2, col3 = st.columns((1, 1, 1))
            with col1:
                email = st.text_input('Email', key='email')
                name = st.text_input('Name', key='name')
                institute = st.text_input('Institute', key='institute')
            with col2:
                with st.container():
                    r_purpose = st.text_area('Research purpose', height=200, key='research_purpose')
            submision = st.button('Submit Request')
            if submision:
                request_info_dict = {'Email':[email], 'Name':[name], 'Institute':[institute], 'Research purpose':[r_purpose]}
                request_info_df = pd.DataFrame(request_info_dict)
                st.dataframe(request_info_df, column_config={}, hide_index=True)
                st.markdown(utils.content_font.format('Your download request has been submitted. You will receive a download link via email upon approval'), unsafe_allow_html=True)
            
# total_metadata_dir = '/haplox/users/donglf/web_services/TCR/total_data/'
# LungCancer_meta_data = f"{total_metadata_dir}/metadata/LungCancer_TCR_data.csv"
# LungNodule_meta_data = f"{total_metadata_dir}/metadata/LungNodule_TCR_data.csv"
LungCancer_meta_data = f"{PROJECT_DIR}/metadata/LungCancer_TCR_data.csv"
LungNodule_meta_data = f"{PROJECT_DIR}/metadata/LungNodule_TCR_data.csv"
DOWNLOAD_TBL_COLS = ['Sample_ID', 'Type', 'file_name']
access_policy = """
This agreement governs the terms and conditions on which access will be granted to users of the sequencing and personal data generated by The HAPLOX Lung Cancer T-cell Receptor Database Research Group (LungTCR). 
<br><br>
By signing this agreement, You agree to be bound by the terms and conditions of access set out in this agreement.
<br><br>
1. You agree to use the Data only for the advancement of medical and scientific research, according to the consent given by Data Subjects.
<br><br>
2. You agree not to use the Data for the creation of products for sale or for any commercial purpose. 
<br><br>
3. You agree to preserve, at all times, the confidentiality of information and Data pertaining to Data Subjects.
<br><br>
4. You agree not to transfer or disclose the Data, in whole or in part, or any information/material derived from the Data, to others.
<br><br>
5. You agree to use the Data for the approved purpose and project described in your application only.
<br>
"""

st.set_page_config(
    page_title="Data Download",
    page_icon="⏬",
    layout="wide"
)
with open( f"{PROJECT_DIR}/app/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.sidebar.image(utils.LN_TCRDB_LOGO_FILE, width=200)
st.markdown(utils.sub_header_font.format("Data Download"), unsafe_allow_html=True)

def download_button(text:str, input_file:str):
    input_tbl = pd.read_csv(input_file)
    st.download_button(label=f"Download {text}",data=convert_df(input_tbl),file_name=os.path.basename(input_file))

tab1, tab2, tab3, tab4 = st.tabs(["Access Policy", "Lung Cancer TCR", "Lung Noduel TCR", 'Other Information'])
with tab1:
    col_intro_1, col_intro_2 = st.columns((7,3))
    with col_intro_1:
        st.markdown(utils.header_font.format("Data Access Agreement"), unsafe_allow_html=True)
        st.markdown(utils.content_font.format(access_policy), unsafe_allow_html=True)
with tab2:
    request_download_agrid(LungCancer_meta_data, "Lung Cancer TCR Data")
    # request_download(LungCancer_meta_data, "Lung Cacner TCR Data")
with tab3:
    request_download_agrid(LungNodule_meta_data, "Lung Nodule TCR Data")
    # request_download(LungNodule_meta_data, "Lung Nodule TCR Data")
with tab4:
    st.markdown(utils.sub_header_font.format('Other information download'), unsafe_allow_html=True)
    info_dict = {
        'Sample Information':f'{PROJECT_DIR}/metadata/features/sample_info.csv',
        'Data QC':f'{PROJECT_DIR}/metadata/features/data_qc.csv',
        'TCR features':f'{PROJECT_DIR}/metadata/features/TCR_features.csv',
        'Lung Cancer Tissue enriched sequences':f'{PROJECT_DIR}/metadata/features/LCT_enriched.csv',
        'Lung Cancer Blood enriched sequences':f'{PROJECT_DIR}/metadata/features/LCB_enriched.csv',
        'Super Public sequences':f'{PROJECT_DIR}/metadata/features/Public.csv',
        'Healthy enriched sequences':f'{PROJECT_DIR}/metadata/features/Healthy_enriched.csv',
        'TMB/HED/MSI/PD-L1':f'{PROJECT_DIR}/metadata/features/Mutation_profile.csv',
        'Mutation information':f'{PROJECT_DIR}/metadata/features/Mutation_detail.csv',
    }
    for _text, _file in info_dict.items():
        download_button(_text, _file)
        
