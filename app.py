import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError
from streamlit_autorefresh import st_autorefresh

def get_all_record_from_snowFlake():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from SUPER_MARKET_SALES.RECORDS.SALES_RECORDS")
    return my_cur.fetchall()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_data_rows= get_all_record_from_snowFlake()
df = streamlit.dataframe(my_data_rows ,columns = ["Invoice ID","Branch","City","Customer_type","Gender","Product line","Unit price","Quantity","Tax 5%","Total","Date","Time","Payment","cogs","gross margin percentage","gross income","Rating"])


st_autorefresh(interval=2000, limit=100, key="dataframe")

