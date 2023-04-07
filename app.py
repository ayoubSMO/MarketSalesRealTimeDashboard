import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

def get_all_record_from_snowFlake():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from SUPER_MARKET_SALES.RECORDS.SALES_RECORDS")
    return my_cur.fetchall()
  
  
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows= get_all_record_from_snowFlake()
  df = streamlit.dataframe(my_data_rows)

  print('salam')
