import streamlit as st
from src.data_loader import test_load

st.set_page_config(
    page_title="King County House Sales",
    page_icon="🏘️",
    layout='centered'
    )

st.title('🏘️ Home')
st.write('House prices analysis app')