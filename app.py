import streamlit as st
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

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_data_rows= get_all_record_from_snowFlake()
data = pd.DataFrame(my_data_rows) 
data.columns = ["Invoice ID","Branch","City","Customer_type","Gender","Product line","Unit price","Quantity","Tax 5%","Total","Date","Time","Payment","cogs","gross margin percentage","gross income","Rating"]
df = st.dataframe(data)


with elements("callbacks_sync"):

    # If you just want to store callback parameters into Streamlit's session state
    # like above, you can also use the special function sync().
    #
    # When an onChange event occurs, the callback is called with an event data object
    # as argument. In the example below, we are synchronizing that event data object with
    # the session state item 'my_event'.
    #
    # If an event passes more than one parameter, you can synchronize as many session state item
    # as needed like so:
    # >>> sync("my_first_param", "my_second_param")
    #
    # If you want to ignore the first parameter of an event but keep synchronizing the second,
    # pass None to sync:
    # >>> sync(None, "second_parameter_to_keep")

    from streamlit_elements import sync

    if "my_event" not in st.session_state:
        st.session_state.my_event = None

    if st.session_state.my_event is not None:
        text = st.session_state.my_event.target.value
    else:
        text = ""

    mui.Typography(text)
    mui.TextField(label="Input some text here", onChange=sync("my_event"))

st_autorefresh(interval=2000, limit=100, key="dataframe")

