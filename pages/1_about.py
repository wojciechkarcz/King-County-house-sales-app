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




def main():
   st.write('Placeholder for about page')


if __name__ == '__main__':
    main()