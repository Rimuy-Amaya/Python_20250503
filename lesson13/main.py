import streamlit as st

st.title("我的第一個Streamlit App")

st.write("這是一個簡單的Streamlit應用程式。")

name = st.text_input("請輸入你的名字：")

if name:
    st.write(f"你好, {name}!")

number = st.slider("選擇一個數字", 0, 100, 50)
st.write(f"你選擇的數字是: {number}")

if st.button("點擊我"):
    st.success("按鈕被點擊了！")
