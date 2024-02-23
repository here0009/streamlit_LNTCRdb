import streamlit as st
import sys
sys.path.append(f'{sys.path[0]}/..')
import utils
from utils import PROJECT_DIR

st.set_page_config(
    page_title="Lung Cancer",
    page_icon="🫁",
)

import streamlit as st
import pandas as pd

def main():
    st.title("Lung Cancer Model")
    st.write('### Upload your TCR feature data')

    # Upload file
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=['csv', 'xlsx', 'txt', 'tsv'])

    if uploaded_file is not None:
        # Read uploaded file as dataframe
        df = utils.read_csv_from_uploader(uploaded_file)
        # Display uploaded table
        st.write("Uploaded Table:")
        st.write(df)


if __name__ == '__main__':
    main()
