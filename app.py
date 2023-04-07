import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError
from streamlit_autorefresh import st_autorefresh
from streamlit_apexjs import st_apexcharts


# Function that fetch all data from snowflake table 
def get_all_record_from_snowFlake():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from SUPER_MARKET_SALES.RECORDS.SALES_RECORDS")
    return my_cur.fetchall()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_data_rows= get_all_record_from_snowFlake()
data = pd.DataFrame(my_data_rows) 
data.columns = ["Invoice ID","Branch","City","Customer_type","Gender","Product line","Unit price","Quantity","Tax 5%","Total","Date","Time","Payment","cogs","gross margin percentage","gross income","Rating"]
df = streamlit.dataframe(data)



# Chart essay !! 
options = {
    "chart": {
        "toolbar": {
            "show": False
        }
    },

    "labels": data["City"]
    ,
    "legend": {
        "show": True,
        "position": "bottom",
    }
}

series = [44, 55, 41, 17, 15]
st_apexcharts(options, series, 'donut', '600', 'title')

st_autorefresh(interval=2000, limit=100, key="dataframe")

