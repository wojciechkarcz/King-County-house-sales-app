#import sys
#sys.path.append('../')
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from src.data_loader import load_csv_data


def data_load():
    csv = 'data/kc_house_data.csv'
    df = load_csv_data(csv)
    return df

def parameters():
	start_date = st.date_input('Select start date',value=datetime.strptime('2014-05-02','%Y-%m-%d') ,min_value=datetime.strptime('2014-05-02','%Y-%m-%d'), max_value=datetime.strptime('2015-05-27','%Y-%m-%d'))
	end_date = st.date_input('Select end date',value=datetime.strptime('2015-05-27','%Y-%m-%d') ,min_value=datetime.strptime('2014-05-02','%Y-%m-%d'), max_value=datetime.strptime('2015-05-27','%Y-%m-%d'))
	
	intervals = {'daily':'D','weekly':'W-MON','monthly':'MS'}
	interval_option = st.radio('Choose time interval',('daily','weekly','monthly'))
	
	price = st.select_slider('Price range:',options=[75000, 100000, 250000, 500000,750000,1000000,2000000,7700000], value=(75000,1000000))
	
	sqft_living = st.slider('House area [sqft]:',290,13540,(290,13540))
	sqft_lot = st.select_slider('Lot area [sqft]:',options=[520,5000,10000,15000,30000,1700000], value=(520,1700000))
	
	bedrooms = st.select_slider('Number of bedrooms:',options=[0,1,2,3,4,5,6,7,8,9,10,11,33], value=(0,11))
	waterfront = st.checkbox('Waterfront')
	
	return start_date, end_date, intervals, interval_option, price, sqft_living, sqft_lot, bedrooms, waterfront


def create_temp_df(df, start_date, end_date, price, sqft_living, sqft_lot, bedrooms, waterfront):
	temp = df.loc[(df['date'].dt.date >= start_date) & 
        (df['date'].dt.date <= end_date) &
        (df['price'] >= price[0]) &
        (df['price'] <= price[1]) &
        (df['sqft_living'] >= sqft_living[0]) &
        (df['sqft_living'] <= sqft_living[1]) &
        (df['sqft_lot'] >= sqft_lot[0]) &
        (df['sqft_lot'] <= sqft_lot[1]) &
        (df['bedrooms'] >= bedrooms[0]) &
        (df['bedrooms'] <= bedrooms[1]) &
        (df['waterfront'] == waterfront)]

	return temp


def plot_temp_df(df, intervals, interval_option):
     st.line_chart(data=df.resample(intervals[interval_option], on='date')['id'].count())
     

def map_plot(df):
    fig = px.scatter_mapbox(df, lat='lat', lon='long', color='price', size='sqft_living', 
        hover_name='id', size_max=15, zoom=9, 
        color_continuous_scale=px.colors.cyclical.IceFire, 
        mapbox_style="carto-positron")
    st.write(fig)


def main():
	st.set_page_config(page_title="Transactions | King County", page_icon=":handshake:", layout='wide')
	st.title(':handshake: Transactions')

	df = data_load()
    
	start_date, end_date, intervals, interval_option, price, sqft_living, sqft_lot, bedrooms, waterfront = parameters()
    
	temp = create_temp_df(df, start_date, end_date, price, sqft_living, sqft_lot, bedrooms, waterfront)
	
	plot_temp_df(temp,intervals, interval_option)

	st.write(temp)
    
	map_plot(temp)


if __name__ == '__main__':
    main()
