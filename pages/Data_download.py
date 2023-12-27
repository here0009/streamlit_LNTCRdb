import streamlit as st
import pandas as pd
from base64 import b64encode
import os
import sys
from zipfile import ZipFile
sys.path.append(f'{sys.path[0]}/..')
import utils
from utils import PROJECT_DIR


st.set_page_config(
    page_title="Data Download",
    page_icon="🔗",
)

LungCancer_meta_data = f"{PROJECT_DIR}/metadata/LungCancer_TCR_data.csv"
LungNodule_meta_data = f"{PROJECT_DIR}/metadata/LungNodule_TCR_data.csv"


def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True), "file_name":None},
        disabled=df.columns,
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
    st.markdown(f"### {subtitle}")
    meta_tbl = utils.read_csv(meta_data_file)

    selection = dataframe_with_selections(meta_tbl)
    st.write('#### Selected')
    st.dataframe(selection, column_config={"file_name":None})
    checked_files = selection['file_name'].tolist()
    # st.write(checked_files)
    if st.button(f"Download Selected Files from {subtitle}") and len(checked_files) > 0:
        download_files(checked_files)

def main():
    st.title("Data Download")
    tab1, tab2 = st.tabs(["Lung Cancer TCR", "Lung Noduel TCR"])
    with tab1:
        select_data_download(LungCancer_meta_data, "Lung Cacner TCR Data")
    with tab2:
        select_data_download(LungNodule_meta_data, "Lung Nodule TCR Data")


if __name__ == '__main__':
    main()

