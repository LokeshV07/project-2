import streamlit as st
import pandas as pd


import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')


st.set_page_config(page_title="NAME",layout="wide")

st.title("Operational Data")

fl=st.file_uploader("file_folder: upload a file",type=(["csv","xls","xlsx"]))


def dashboard(df):

    current_directory = os.getcwd()
    st.write("Current Working Directory:", current_directory)

    col1,col2 =st.columns((2))
    df["TRANSDATE"]=pd.to_datetime(df["TRANSDATE"])

    fromdate=pd.to_datetime(df["TRANSDATE"]).min()
    todate=pd.to_datetime(df["TRANSDATE"]).max()

    with col1:
        date1=pd.to_datetime(st.date_input("From Date",fromdate))

    with col2:
        date2=pd.to_datetime(st.date_input("To Date",todate))
            
    df=df[(df["TRANSDATE"] >= date1) & (df["TRANSDATE"] <= date2)].copy()

    st.sidebar.header("Filters")

    Location = st.sidebar.multiselect("Select the Plant Location",df["Location"].unique())
    if not Location:
        df2=df.copy()
    else:
        df2=df[df["Location"].isin(Location)]


    SALESENGINEER = st.sidebar.multiselect("Select the Sales Engineer",df2["SALESENGINEER"].unique())
    if not SALESENGINEER:
        df3=df2.copy()
    else:
        df3=df2[df2["SALESENGINEER"].isin(SALESENGINEER)]



    if not Location and not SALESENGINEER:
        filtered_df=df
    elif not SALESENGINEER:
        filtered_df=df[df["Location"].isin(Location)]
    elif SALESENGINEER:
        filtered_df=df[df["SALESENGINEER"].isin(SALESENGINEER)]
    else:
        filtered_df=df3[df["Location"].isin(Location) & df["SALESENGINEER"].isin(SALESENGINEER)]

    SalesTime_df=filtered_df.groupby(by =["Time Slots (2Hrs)"], as_index = False)["DESPATCHEDQTY"].sum()
    SalesDayNight_df=filtered_df.groupby(by =["Day/Night"], as_index = False)["DESPATCHEDQTY"].sum()

    with col1:
        st.subheader("Sales wrt Time")
        fig= px.bar(SalesTime_df, x="Time Slots (2Hrs)",y= "DESPATCHEDQTY", template= "seaborn")
        fig.update_traces(text=SalesTime_df["DESPATCHEDQTY"], textposition='outside')
        st.plotly_chart(fig, use_container_width=True, height=200)


    with col2:
        st.subheader("Sales wrt Day and Night")
        fig = px.pie(SalesDayNight_df, names="Day/Night", values="DESPATCHEDQTY",labels={"DESPATCHEDQTY": "Sales"}, template="seaborn")
        fig.update_traces(text=filtered_df["Day/Night"] ,textposition="inside", textinfo="percent+label", showlegend = True)
        st.plotly_chart(fig, use_container_width=True,  height=200)

    cl1, cl2 = st.columns(2)
    with cl1:
        with st.expander("Sales Data"):
            st.write(SalesTime_df.style.background_gradient(cmap="Blues"))
            csv=SalesTime_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download",data = csv, file_name="Sales.csv", mime= "text/csv")

    with cl2:
        with st.expander("Day Night"):
            st.write(SalesDayNight_df.style.background_gradient(cmap="Oranges"))
            csv=SalesDayNight_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download",data = csv, file_name="Day_Night.csv", mime= "text/csv")


    Sales_df=filtered_df.groupby(by =["TRANSDATE"], as_index = False)["DESPATCHEDQTY"].sum()

    st.subheader("Sales")
    fig= px.line(Sales_df, x="TRANSDATE",y= "DESPATCHEDQTY", template= "seaborn")
    fig.update_traces(text=Sales_df["DESPATCHEDQTY"], textposition='top center')
    st.plotly_chart(fig, use_container_width=True, height=200)

    with st.expander("Sales"):
            st.write(Sales_df.style.background_gradient(cmap="Blues"))
            csv=Sales_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data",data = csv, file_name="Sales.csv", mime= "text/csv")


    Sales_Engineer_df=filtered_df.groupby(by =["SALESENGINEER"], as_index = False)["DESPATCHEDQTY"].sum()
    st.write(Sales_Engineer_df.style.background_gradient(cmap="Blues"))
    csv=Sales_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data",data = csv, file_name="SalesEngineer.csv", mime= "text/csv")

if fl is not None:
    filename= fl.name
    st.write(filename)
    df=pd.read_excel(filename)
    dashboard(df)
else:
    st.write("Upload File")
    #os.chdir(r"H:\Web project")
    #df=pd.read_excel("05 May 2023.xlsx")
