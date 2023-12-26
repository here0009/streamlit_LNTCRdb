import sys
import os
import streamlit as st
sys.path.append(f'{sys.path[0]}/..')
import utils
from utils import PROJECT_DIR

st.set_page_config(
    page_title="Enriched score calculation",
    page_icon="💻",
)