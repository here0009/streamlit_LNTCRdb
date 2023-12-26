import streamlit as st
import json
import pandas as pd
import sys
sys.path.append(f'{sys.path[0]}/..')
import utils
from utils import PROJECT_DIR

# CONFIG_FILE=f"{PROJECT_DIR}/datapath.json"
# config_fhand = open(CONFIG_FILE, "r")
# config_dict = json.load(config_fhand)
st.set_page_config(
    page_title="Data Preview",
    page_icon="👁️",
)
st.title("Data Preview")

sample_info_file = f'{PROJECT_DIR}/metadata/LungNodule_sample_info.csv'
sample_info_tbl = pd.read_csv(sample_info_file)

st.dataframe(
    sample_info_tbl,
    column_config={
    },
    hide_index=True,
)
