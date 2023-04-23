import streamlit as st
import pandas as pd
from src.data_loader import load_data_sql


@st.cache_data
def data_load():
	'''Function for data loading from PostgreSQL db and returning pandas dataframe'''
	df = load_data_sql()
	return df

def get_metrics(df):
    '''Getting some basic metrics from df''' 
    df = df.sort_values(by='date')
    total = len(df)
    avg_price = int(round(df['price'].mean(),0))
    avg_area = int(round(df['sqft_living'].mean(),0))
    return total, avg_price, avg_area


def main():
   
    st.set_page_config(
    page_title="House sales in King County | About",
    page_icon="🏘️",
    layout='centered')
    st.title('🏘️ About')

    df = data_load()

    st.markdown('##')

    st.image('img/kingcounty.jpg', caption='credit: Wikimedia', width=600)

    st.markdown('This web application is used to analyze data on home sales in King County, USA. ' +
                'The data has been made available for public use and can be downloaded from the website:  ' +
                 '[https://www.kaggle.com/datasets/harlfoxem/housesalesprediction](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction)')

    st.markdown('##')

    st.markdown('Some basic metrics of the dataset')

    total, avg_price, avg_area = get_metrics(df)

    col1, col2, col3  = st.columns(3)

    with col1:
         st.metric(('Number of transactions'), total)
    with col2:
         st.metric(('Avg. price $'), avg_price)
    with col3:
         st.metric(('Avg. area [sqft]'), avg_area)
    
    st.markdown('###')

    st.markdown('''
    Detailed documentation describing the data set can be found at this link:  
    [https://geodacenter.github.io/data-and-lab/KingCounty-HouseSales2015/](https://geodacenter.github.io/data-and-lab/KingCounty-HouseSales2015/)
    ''')


if __name__ == '__main__':
    main()