import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import json
from urllib.error import URLError
from streamlit_autorefresh import st_autorefresh
from streamlit_elements import elements, mui, html, sync,editor, lazy,nivo
import plotly.express as px  # pip install plotly-express
import numpy as np 

st.set_page_config(page_title="Market Sales Dashboard", page_icon=":bar_chart:", layout="wide")


# Function that fetch all data from snowflake table 
def get_all_record_from_snowFlake():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from SUPER_MARKET_SALES.RECORDS.SALES_RECORDS")
    return my_cur.fetchall()

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_data_rows= get_all_record_from_snowFlake()
data = pd.DataFrame(my_data_rows)
data.columns = ["Invoice ID","Branch","City","Customer_type","Gender","Product line","Unit price","Quantity","Tax 5%","Total","Date","Time","Payment","cogs","gross margin percentage","gross income","Rating"]
json_list = json.loads(data.to_json(orient='records'))

data["hour"] = pd.to_datetime(data["Time"]).dt.hour
#data["hour"] = data["hour"].astype(int)

data["Invoice ID"] =data["Invoice ID"].astype(str)
data["Branch"]=data["Branch"].astype(str)
data["City"]=data["City"].astype(str)
data["Customer_type"]=data["Customer_type"].astype(str)
data["Gender"]=data["Gender"].astype(str)
data["Product line"]=data["Product line"].astype(str)
data["Unit price"]=data["Unit price"].astype(float)
#data["Quantity"]=data["Quantity"].astype(int)
data["Tax 5%"]=data["Tax 5%"].astype(float)
data["Total"]=data["Total"].astype(float)
data["Payment"]=data["Payment"].astype(str)
data["cogs"]=data["cogs"].astype(float)
data["gross margin percentage"]=data["gross margin percentage"].astype(float)
data["Rating"]=data["Rating"].astype(float)


st.sidebar.image(
            "https://mail.google.com/mail/u/0?ui=2&ik=f84a0aba7a&attid=0.1&permmsgid=msg-f:1751659840764464914&th=184f255830154f12&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ9MhmfflXcF02tA97hulNBaLi8lPU9KhZ-nmoiOaK7jzKLWhvQKX0HntrVgz060igt8PIgAlq67QA1VcRGbTbgVepyHwed_J6PwrX71ytzrDgckUXZrOhjFepU&disp=emb",
            width=200, # Manually Adjust the width of the image as per requirement
        )
st.sidebar.header("Please Filter Here:")

st.markdown(
    """
<style>
span[data-baseweb="tag"] {
  background-color: #4b84ec !important;
}
</style>
""",
    unsafe_allow_html=True,
)
city = st.sidebar.multiselect(
    "Select the City:",
    options=data["City"].unique(),
    default=data["City"].unique(),
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


# ---- MAINPAGE ----
st.title(":bar_chart: Market Sales Dashboard")
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


st.markdown("##")


df = st.dataframe(data)

st.markdown("""---""")

new_groupe = df_selection.groupby(by=["Product line"])

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
     new_groupe.aggregate(np.sum)[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#40E0D0"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#FF4500"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

# SALES BY HOUR [line]
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.line(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#4B0082"] * len(sales_by_hour),
    
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
   
)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)

sales_per_city = df_selection.groupby(by=["City"]).sum()[["Total"]]
fig = px.pie(
    sales_per_city,
    values='Total',
    names=sales_per_city.index,
    title='Sales per City',
)
right_column.plotly_chart(fig, use_container_width=True)


with left_column:
    st.subheader("Filtred Data:")
df = st.dataframe(data)

pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.width', 1000)  # Set the width of the display
pd.set_option('display.precision', 2)  # Set the precision of floating-point numbers



st_autorefresh(interval=20000, limit=100, key="dataframe")

st.markdown( 
   f""" 
   <style> 
   .reportview-container .main .block-container{{ 
      max-width: 800px; 
      padding-top: 3rem; 
      padding-right: 1rem; 
      padding-left: 1rem; 
      padding-bottom: 3rem; 
      }} 
      </style> """, 
      unsafe_allow_html=True 
      )
