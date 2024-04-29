import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu 
from numerize.numerize import numerize
from query import * 
import time

st.set_page_config(page_title="Realtime Dashboard", page_icon="🇻🇳", layout="wide")
st.subheader("🔔 Interactive dashboard live Analytics")
st.markdown("##")

result = view_all_data()
df = pd.DataFrame(result, columns=['year','make','model','trim','body','transmission','vin','state','condition','odometer','color','interior','seller','mmr','sellingprice'])
#st.dataframe(df)
#viet sidebar
st.sidebar.image("image/logo.png", caption="HO CHINH MINH UNIVERSITY OF NATURAL RESOURCES AND ENVIROMENTS")
#witcher
st.sidebar.header("Please Filter")
state = st.sidebar.multiselect(
    "Select State",
    options=df['state'].unique(),
    default=df["state"].unique(),
)
body = st.sidebar.multiselect(
    "Select Body",
    options=df['body'].unique(),
    default=df["body"].unique(),
)
make = st.sidebar.multiselect(
    "Select make",
    options=df['make'].unique(),
    default=df['make'].unique(),
)

#tao dataframe
df_selection = df.query(
    "state==@state & body==@body & make==@make"
)
# st.dataframe(df_selection)

def Home():
    with st.expander("Tabular"):
        showData = st.multiselect('Filter: ', df_selection.columns, default=[])
        st.write(df_selection[showData])

#Tong so lương 
total_quantity=df_selection['sellingprice'].sum()
max_quantity= df_selection['sellingprice'].max()
mean_quantity = df_selection['sellingprice'].mean()
median_quantity = df_selection['sellingprice'].median()
min_quantity = df_selection['sellingprice'].min()

total1, total2, total3, total4, total5 = st.columns(5, gap='large')
with total1:
    st.info('Total Sold', icon="📌")
    st.metric(label="Sum Sold car", value=f"{total_quantity:,.0f}")
    
with total2:
    st.info('Max Sold Car', icon="📌")
    st.metric(label="maximum car", value=f"{max_quantity:,.0f}")

with total3:
    st.info('Mean Sold', icon="📌")
    st.metric(label="Mean car", value=f"{mean_quantity:,.0f}")

with total4:
    st.info('Median Sold', icon="📌")
    st.metric(label="Median Sold", value=f"{median_quantity:,.0f}")
    
with total5:
    st.info('Min Sold Car', icon="📌")
    st.metric(label="Mininum Sold", value=f"{min_quantity:,.0f}")

st.markdown("""-----""")

#Xay dung bieu do

def graphs():
    # total_soldcar = int(df_selection['sellingprice']).sum()
    # average_sold = int(round(df_selection['sellingprice']).mean(),2)
    
    sold_by_type = (
        df_selection.groupby(by='make').count()[['sellingprice']].sort_values(by="sellingprice")
    )
    
    #simple bar graph
    fig_selling = px.bar(
        sold_by_type,
        x ="sellingprice",
        y = sold_by_type.index,
        orientation='h',
        title= "<b>Tong luong xe ban ra</b>",
        color_discrete_sequence=["#0083b8"]*len(sold_by_type),
        template="plotly_white", 
    )
    
    fig_selling.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    #simple line graph
    sold_by_state = df_selection.groupby(by='state').count()[['sellingprice']]

    fig_state = px.line(
        sold_by_state,
        x=sold_by_state.index,
        y="sellingprice",
        orientation='v',
        title= "<b>Tong luong xe ban ra theo tung bang</b>",
        color_discrete_sequence=["#0083b8"]*len(sold_by_state),
        template="plotly_white", 
    )
    fig_state.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickmode='linear'),
        yaxis=(dict(showgrid=False)),
    )
    #bieu đồ pie
    category_df= df_selection.groupby(by=["make"], as_index= False)["sellingprice"].sum()
    pie_state = px.pie(
        category_df,
        values="sellingprice",
        names= "make",
        hole=0.5
    )
    pie_state.update_traces(
        text= df_selection["make"],
        textposition="outside")
    
    
    left, right, bottom = st.columns(3)
    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_selling, use_container_width=True)
    bottom.plotly_chart(pie_state, use_container_width=True)

def scatter_plot():
    scatter_chart = px.scatter(
        df_selection,
        x = "condition",
        y = "sellingprice",
        color="make"
        
    )
    scatter_chart.update_traces(marker=dict(size=12))
    
    st.plotly_chart(scatter_chart, use_container_width=True)

def progresbar():
    st.markdown("""<style>.stProgress > div > div > div > {background-image: linear-gradient(to right, #99ff99, #FFFF00)}</style>""", unsafe_allow_html=True,)
    target=3000000000
    current=df_selection["sellingprice"].sum()
    percent=round((current/target*100))
    mybar=st.progress(0)
    
    if percent > 100:
        st.subheader("Hoàn thành mục tiêu thị trường")
    else:
        st.write("Thị trường cần đạt", percent, " % ", " của ", (format(target, 'd')), "Đô")
    for percent_complete in range(percent):
        time.sleep(0.1)
        mybar.progress(percent_complete+1, text="Phần trăm thị trường" )
        
def sideBar():
    selected=option_menu(
            menu_title="Màn hình chính",
            options=["Home", "Progress"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0,
            orientation="v"
        )
    with st.sidebar:
        selected=option_menu(
            menu_title="Màn hình chính",
            options=["Home", "Progress"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0
        )
    if selected=="Home":
        st.subheader(f"Trang: {selected}")
        Home()
        graphs()
        scatter_plot()
    if selected=="Progress":
        st.subheader(f"Trang: {selected}")
        progresbar()
        graphs()
        
        
sideBar()

#theme
hide_st_style="""
<style>
#mainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

    