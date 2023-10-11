import streamlit as st
import requests
import configparser

# configparser 객체 생성
config = configparser.ConfigParser()

# config.toml 파일을 읽기
config.read('config.toml')

# 설정 가져오기
# value = config.get('theme', 'primaryColor')


fastapi_url = "http://43.202.93.56:3001/detail/context"
response = requests.get(fastapi_url)
informaion = response.json()["Information"]["context"]
problem = response.json()["Information"]["problem"]
look = response.json()["Information"]["look"]

fastapi_url2 = "http://43.202.93.56:3001/detail/explanation"
response = requests.get(fastapi_url2)
explanation = response.json()["Information"]["explanation"]

look_lsit = look.split(".")
explanation_lsit = explanation.split(")")

st.title('수능 특강 변형 문제 풀어보기')
st.subheader('지문을 읽고 문제를 풀어보세요')
st.markdown(informaion[1:-2])
st.header('문제 1.')
st.subheader(problem)
st.markdown(look_lsit[0])
st.markdown(look_lsit[1])
st.markdown(look_lsit[2])
st.markdown(look_lsit[3])
st.header('정답 및 해설')
st.markdown(f"정답 : {explanation_lsit[0]}")
st.markdown(f"해설 : {explanation_lsit[1]}")
