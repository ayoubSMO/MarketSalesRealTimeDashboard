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



df_selection = data.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].astype(float).sum())
average_rating = round(df_selection["Rating"].astype(float).mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].astype(float).mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")



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

st_autorefresh(interval=2000, limit=100, key="dataframe")

