import streamlit as st

from src.data_loader import load_csv_data


st.set_page_config(
    page_title="King County House Sales",
    page_icon="🏘️",
    layout='centered'
    )

st.title('🏘️ Home')
st.write('House prices analysis app')
st.markdown('test')


def parameters():
    sqft_living = st.slider('House area [sqft]:',290,13540,(290,13540))
    sqft_lot = st.select_slider('Lot area [sqft]:',options=[520,5000,10000,15000,30000,1700000], value=(520,1700000))
    return [sqft_living, sqft_lot]

def main():
    params = parameters()
        
    st.write(params[0])
    st.write(params[1])



if __name__ == '__main__':
    main()