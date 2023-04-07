import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import json
from urllib.error import URLError
from streamlit_autorefresh import st_autorefresh
from streamlit_elements import elements, mui, html, sync,editor, lazy,nivo



# Function that fetch all data from snowflake table 
def get_all_record_from_snowFlake():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from SUPER_MARKET_SALES.RECORDS.SALES_RECORDS")
    return my_cur.fetchall()

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_data_rows= get_all_record_from_snowFlake()
data = pd.DataFrame(my_data_rows) 
data.columns = ["Invoice ID","Branch","City","Customer_type","Gender","Product line","Unit price","Quantity","Tax 5%","Total","Date","Time","Payment","cogs","gross margin percentage","gross income","Rating"]
df = st.dataframe(data)
json_list = json.loads(data.to_json(orient='records'))

st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=data["City"].unique(),
    default=data["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=data["Customer_type"].unique(),
    default=data["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=data["Gender"].unique(),
    default=data["Gender"].unique()
)

df_selection = data.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

df_selection
df_selection["Total"].sum()

st_autorefresh(interval=2000, limit=100, key="dataframe")

