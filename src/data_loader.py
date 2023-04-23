import pandas as pd
import psycopg2
import streamlit as st

# Credentials for connecting to external PostgreSQL database hidden using Streamlit st.secrets
db = st.secrets['db']
user = st.secrets['user']
password = st.secrets['password']
host = st.secrets['host']

# Column names corresponding to the names of the columns in the database 
column_names = ['id', 'date', 'price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'condition',
    'grade', 'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated', 'zipcode', 'lat', 'long', 'sqft_living15', 'sqft_lot15']

# Simple query to fetch all the data from the table
query = 'SELECT * FROM kchouses2;'


def connect(db, user, password, host):
    '''Establishing connection to remote database'''
    conn = psycopg2.connect(database=db, user=user,
    password=password, host=host,
    port=5432)
    return conn


def sql_to_df(conn, query, column_names):
    '''Downloading data from database and converting to pandas dataframe'''
    cursor = conn.cursor()
    cursor.execute(query)
   
    tuples_list = cursor.fetchall()
    cursor.close()

    df = pd.DataFrame(tuples_list, columns=column_names)
    return df


def transform_df(df):
    '''Transforming and cleaning the dataframe'''
    df['date'] = pd.to_datetime(df['date'])
    df[['id','bathrooms','floors','zipcode','lat','long',]] = df[['id','bathrooms','floors','zipcode','lat','long',]].astype(float)
    df[['id','zipcode']] = df[['id','zipcode']].astype(int)
    df['id'] = df['id'].apply(abs)
    return df


def load_data_sql():
    '''Utility function to download, transform, clean and return a dataframe ready to perform further operations'''
    conn = connect(db, user, password, host)
    df = sql_to_df(conn, query, column_names)
    conn.close()
    df = transform_df(df)
    return df


def load_csv_data(csv):
    '''Temp function to test application with upload data from local .csv file'''
    df = pd.read_csv(csv, parse_dates=['date'], dayfirst=True)
    return df


