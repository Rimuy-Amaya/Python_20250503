import streamlit as st

st.title("我的第一個Streamlit App")

st.write("這是一個簡單的Streamlit應用程式。")

import pandas as pd

df = pd.read_csv("taiwan.csv")
st.dataframe(df)
