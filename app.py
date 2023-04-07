import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError
from streamlit_autorefresh import st_autorefresh
from streamlit_elements import elements, mui, html

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


with elements("properties"):

    # You can add properties to elements with named parameters.
    #
    # To find all available parameters for a given element, you can
    # refer to its related documentation on mui.com for MUI widgets,
    # on https://microsoft.github.io/monaco-editor/ for Monaco editor,
    # and so on.
    #
    # <Paper elevation={3} variant="outlined" square>
    #   <TextField label="My text input" defaultValue="Type here" variant="outlined" />
    # </Paper>

    with mui.Paper(elevation=3, variant="outlined", square=True):
        mui.TextField(
            label="My text input",
            defaultValue="Type here",
            variant="outlined",
        )

    # If you must pass a parameter which is also a Python keyword, you can append an
    # underscore to avoid a syntax error.
    #
    # <Collapse in />

    mui.Collapse(in_=True)

    # mui.collapse(in=True)
    # > Syntax error: 'in' is a Python keyword:

st_autorefresh(interval=2000, limit=100, key="dataframe")

