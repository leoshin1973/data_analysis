import os
import streamlit as st
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from pygwalker.api.streamlit import StreamlitRenderer

# Streamlit 설정
st.set_page_config(page_title="GPT4 이용 엑셀파일 분석하기", layout="wide")

# 사이드바에서 OpenAI API 키 입력 받기
api_key = st.sidebar.text_input("OPENAI API Key 입력하세요", type="password")

with st.sidebar:
    st.write("컬럼과 데이터레코드가 있는 Table 형태의 파일을 선택하세요")


# OpenAI API 키 설정
if api_key:
    os.environ['OPENAI_API_KEY'] = api_key
else:
    st.warning("Please enter your OpenAI API key.")

st.markdown("[Visit OpenAI](https://www.openai.com)")

# 파일 업로드 처리
upload_file = st.file_uploader("파일 선택", type=["csv", "xlsx"])

def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file, engine='openpyxl')
    else:
        st.error("지원되지 않는 파일 형식입니다. CSV 또는 Excel 파일을 업로드하세요.")
        st.stop()

# 파일이 업로드된 경우 데이터 로드 및 처리
if upload_file:
    df = load_data(upload_file)
    st.write(df)

    st.divider()
    st.write("업로드 파일 내용 살펴보기")
    pyg_app = StreamlitRenderer(df)
    pyg_app.explorer()

    # Chat 모델 설정 및 데이터프레임 에이전트 생성
    model = ChatOpenAI(temperature=0, model='gpt-4-0613')
    agent = create_pandas_dataframe_agent(
        model,
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True,
    )

    # 기본 질문 실행
    initial_query = '파일은 몇개의 컬럼으로 이루어져 있고 총 몇개 레코드로 구성되어 있는지 알려줘. 각각의 컬럼명을 별도로 알려줘'
    initial_response = agent.run(initial_query)
    st.write(initial_response)

    # 사용자 질문 처리
    user_question = st.text_input("질문을 입력하세요. 예시: 첫번째 컬럼에서 이상치 데이터가 있는지 확인해줘")

    if user_question:
        user_response = agent.run(user_question)
        st.write(user_response)
