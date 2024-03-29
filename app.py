import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from src.data_loader import load_data_sql


@st.cache_data
def data_load():
	'''Function for data loading from PostgreSQL db and returning pandas dataframe'''
	df = load_data_sql()
	df['avg_price_sqft'] = round(df['price'] / df['sqft_living'],2)
	df['avg_price_bedroom'] = df.apply(lambda row: calculate_avg_price_bedroom(row), axis=1)
	return df


def calculate_avg_price_bedroom(row):
	'''Function wchich calculates average price per bedroom'''
	x = row['bedrooms']
	if x == 0:
		return 0
	else:
		return round(row['price'] / row['bedrooms'],2)


def create_temp_df(df, start_date, end_date, price, sqft_living, sqft_lot, bedrooms, waterfront, yr_built):
	'''Function takes as arguments a df and parameters defined by user, returns filtered dataframe called temp'''
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
        (df['waterfront'] == waterfront) &
		(df['yr_built'] >= yr_built[0]) &
		(df['yr_built'] <= yr_built[1])]
	temp = temp.sort_values(by='date')
	return temp


def price_metric(temp, price_mod, price_mod_label):
	'''Caclulates average price depending on the option choosed by user'''
	if len(temp) == 0:
		return 0
	else:
		return int(round(temp[price_mod_label[price_mod]].mean(), 0))


def price_metric_delta(temp, df, price_mod, price_mod_label):
	'''Calculates average price delta'''
	if len(temp) == 0:
		return 0
	else: 
		total_average = df[price_mod_label[price_mod]].mean()
		delta = temp[price_mod_label[price_mod]].mean() - total_average
		return str(round((delta/total_average)*100, 1)) + ' %'


def metrics(temp, df):
	'''Calculates and returns metrics such as: number of transactions, avg. house area, avg. lot area and their deltas'''
	transactions = len(temp)
	transactions_delta = round((transactions / len(df))*100,2)

	if len(temp) == 0:
		house_area = 0
		lot_area = 0
	else:
		house_area = int(round(temp['sqft_living'].mean(),0))
		lot_area = int(round(temp['sqft_lot'].mean(),0))

	house_area_delta = round(((house_area - df['sqft_living'].mean()) / df['sqft_living'].mean())*100,1)
	lot_area_delta = round(((lot_area - df['sqft_lot'].mean()) / df['sqft_lot'].mean())*100,1)
	return transactions, str(transactions_delta) + ' %', house_area, str(house_area_delta) + ' %', lot_area, str(lot_area_delta) + ' %'


def plot_avg_price(df, intervals, interval_option, price_mod, price_mod_label):
	'''Line plot of avg. price'''
	data = df.resample(intervals[interval_option], on='date')[price_mod_label[price_mod]].mean()
	fig = px.line(data, y=price_mod_label[price_mod])
	st.plotly_chart(fig)


def plot_bar_avg_price(df, price_mod, price_mod_label):
	'''Bar plot for monthly view of avg. price'''
	data = df.resample('MS', on='date')[price_mod_label[price_mod]].mean()
	fig = px.bar(data, y=price_mod_label[price_mod], text_auto='.2s')
	st.plotly_chart(fig)


def plot_transactions(df, intervals, interval_option):
	'''Line plot of number of transactions'''
	data = df.resample(intervals[interval_option], on='date')['id'].count()
	fig = px.line(data, y='id')
	st.plotly_chart(fig)


def plot_bar_transactions(df, intervals, interval_option):
	'''Bar plot for monthly view of transactions'''
	data = data=df.resample('MS', on='date')['id'].count()
	fig = px.bar(data, y='id', text_auto='.2s')
	st.plotly_chart(fig)


def map_plot(df):
    '''Map plot with houses filtered by criteria defined by user'''
    fig = px.scatter_mapbox(df, lat='lat', lon='long', color='price', size='sqft_living', 
        hover_name='id', size_max=18, zoom=9, 
        color_continuous_scale=px.colors.cyclical.IceFire, 
        mapbox_style="carto-positron", height=600, opacity=0.7,
		hover_data=['sqft_lot','condition','view','yr_built','avg_price_sqft'])
    st.plotly_chart(fig, use_container_width=True)


def main():
	'''Main function of the application'''
	
	# Page setup
	st.set_page_config(page_title="House sales in King County", page_icon="🏘️", layout='centered')
	st.title('🏘️ House sales in King County')

	# Data load from SQL db
	df = data_load()
    
	st.markdown('Select below the time range that interests you and the parameters defining the properties sold.')
	st.markdown('###')

	# Date range input
	col_date1, col_date2 = st.columns(2, gap='medium')

	with col_date1:
		start_date = st.date_input('**Start date**',value=datetime.strptime('2014-05-02','%Y-%m-%d') ,min_value=datetime.strptime('2014-05-02','%Y-%m-%d'), max_value=datetime.strptime('2015-05-27','%Y-%m-%d'))

	with col_date2:
		end_date = st.date_input('**End date**',value=datetime.strptime('2015-05-27','%Y-%m-%d') ,min_value=datetime.strptime('2014-05-02','%Y-%m-%d'), max_value=datetime.strptime('2015-05-27','%Y-%m-%d'))
	
	st.markdown('###')

	# Parameters input
	col_input1, col_input2 = st.columns(2, gap='medium')
	with col_input1:
		price = st.select_slider('Price range:',options=[75000, 100000, 250000, 500000,750000,1000000,2000000,7700000], value=(75000,1000000))
		bedrooms = st.select_slider('Number of bedrooms:',options=[0,1,2,3,4,5,6,7,8,9,10,11,33], value=(0,11))
		yr_built = st.slider('Year built:',1900,2015,(1900,2015))	
	
	with col_input2:
		sqft_living = st.slider('House area [sqft]:',290,13540,(290,13540))
		sqft_lot = st.select_slider('Lot area [sqft]:',options=[520,5000,10000,15000,30000,1700000], value=(520,1700000))
		st.markdown('#')
		waterfront = st.checkbox('Property on the waterfront')

	# Creating temp dataframe based on criteria defined by user
	temp = create_temp_df(df, start_date, end_date, price, sqft_living, sqft_lot, bedrooms, waterfront, yr_built)
	
	st.markdown('#')
	st.markdown('#### 📈 Plot and metrics')
	
	# Showing different metrics describing houses filtered by user
	price_mod = st.radio('Show average price per:',('transaction','sqft','number of bedrooms'), horizontal=True)
	price_mod_label = {'transaction':'price','sqft':'avg_price_sqft','number of bedrooms':'avg_price_bedroom'}

	st.markdown('####')

	transactions, transactions_delta, house_area, house_area_delta, lot_area, lot_area_delta = metrics(temp, df)
	
	col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)

	with col_metric1:
		st.metric(('Average price $'), value=price_metric(temp, price_mod, price_mod_label), delta=price_metric_delta(temp, df, price_mod, price_mod_label), delta_color="inverse")

	with col_metric2:
		st.metric(('Number of transactions'), value=transactions, delta=transactions_delta, delta_color='off')

	with col_metric3:
		st.metric(('Average house area [sqft]'), value=house_area, delta=house_area_delta)

	with col_metric4:
		st.metric(('Average lot area [sqft]'), value=lot_area, delta=lot_area_delta)

	st.markdown('#####')

	# Choosing the time interval used to display data
	intervals = {'daily':'D','weekly':'W-MON','monthly':'MS'}
	interval_option = st.radio('Choose time interval:',('daily','weekly','monthly'), horizontal=True)

	# Plot area with 3 tabs: Avg. price, Number of transactions and Price distribution
	tab1, tab2, tab3 = st.tabs([':dollar: Average price', ':handshake: Number of transactions', ':bar_chart: Price distribution'])

	with tab1:
		st.markdown('#####')
		st.write('###### Average price per ', price_mod,)

		if interval_option == 'monthly':
			plot_bar_avg_price(temp, price_mod, price_mod_label)
		else:
			plot_avg_price(temp, intervals, interval_option, price_mod, price_mod_label)

	with tab2:
		if interval_option == 'monthly':
			plot_bar_transactions(temp, intervals, interval_option)
		else:
			plot_transactions(temp, intervals, interval_option)

	with tab3:
		fig2 = px.histogram(temp, x=temp['price'], nbins=50)
		st.plotly_chart(fig2, use_container_width=True)

	st.markdown('#####')

	# Map with houses filtered by user
	st.markdown('#### 🗺️ Map')
	st.markdown('The map shows the location of all houses that meet the defined criteria. The color of the marker corresponds to the price, and the size refers to the area of ​​the house. '+
            "If you hover a mouse over a marker, you'll see more data. The title of the label is transaction id.")

	map_plot(temp)

	# Simple table with temp dataframe
	st.markdown('#### 📑 Raw data')
	st.markdown('Below is a table containing all transaction data that meets all the criteria defined at the top of this page. '+
	     'You can click on each column name to sort the data in ascending or descending order.')

	st.write(temp)


if __name__ == '__main__':
    main()
