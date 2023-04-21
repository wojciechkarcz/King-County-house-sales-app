import pandas as pd
import streamlit as st

csv = '../data/kc_house_data.csv'

@st.cache_data
def load_csv_data(csv):
    df = pd.read_csv(csv, parse_dates=['date'], dayfirst=True)
    return df


