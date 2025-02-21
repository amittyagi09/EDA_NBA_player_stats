import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import base64

st.title("NBA Player Stats Data")
st.write("This webapp perform web scrapping of NBA players stats data")
st.write("**Python Libraries:** base64, pandas, matplotlib")
st.write("**Data Source:**[basketball-reference.com](https://www.basketball-reference.com)")
st.write("***")

st.sidebar.header("User Input Features")
selected_year=st.sidebar.selectbox("Year", list(reversed(range(1995, 2025))))

@st.cache_data
def load_data(year):
    url="https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"
    html=url.format(str(year))
    data=pd.read_html(html, header=0)
    data=data[0]
    newdata=data.drop(data[data["Age"]=="Age"].index)
    newdata=newdata.fillna(0)
    return newdata

newdata=load_data(selected_year)

unique_team=newdata["Team"].unique()
selected_team=st.sidebar.multiselect("Team", unique_team)

unique_pos=["C", "PF","SF", "PG", "SG"]
selected_pos=st.sidebar.multiselect("Position", unique_pos)

df_data=newdata[(newdata["Team"].isin(selected_team)) & newdata["Pos"].isin(selected_pos)]

st.header("Display Stats of Selected Team")
st.write("Data Dimensions:"+str(df_data.shape[0])+" rows and "+str(df_data.shape[1])+" columns")
st.dataframe(df_data)


if st.button("Intercorrelation Heatmap"):
    st.header("Intercorrelation Matrix Heatmap")
    remove_columns=["Rk", "Player", "Team", "Awards", "Pos"]
    df_data=df_data.drop(columns=remove_columns, errors="ignore")
    df_data.to_csv("output.csv", index=False)
    data=pd.read_csv("output.csv")
    fig, ax=plt.subplots(figsize=(10,8))
    sns.heatmap(data.corr(), ax=ax)
    st.pyplot(fig)