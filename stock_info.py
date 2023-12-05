import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib 
from io import BytesIO
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.title('무슨 주식을 사야 부자가 되려나..')

stock_name = '삼성전자'

st.sidebar.header('회사 이름과 기간을 입력하세요')

@st.cache_data
def get_stock_info():
    base_url =  "http://kind.krx.co.kr/corpgeneral/corpList.do"    
    method = "download"
    url = "{0}?method={1}".format(base_url, method)   
    df = pd.read_html(url, header=0, encoding='cp949')[0]
    df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}")     
    df = df[['회사명','종목코드']]
    return df

def get_ticker_symbol(company_name):     
    df = get_stock_info()
    code = df[df['회사명']==company_name]['종목코드'].values    
    ticker_symbol = code[0]
    return ticker_symbol

start_date = datetime(2019, 1, 1)
end_date = datetime(2021, 12, 31)


with st.sidebar:
    add_text = st.text_input('회사 이름', stock_name)
    date_range = st.date_input("시작일-종료일", (start_date, end_date))
    button_result = st.button('주가 데이터 확인')
    
    
ticker_symbol = get_ticker_symbol(stock_name)     
start_p = date_range[0]               
end_p = date_range[1] + timedelta(days=1) 
df = fdr.DataReader(ticker_symbol, start_p, end_p, exchange="KRX")
df.index = df.index.date
st.subheader(f"[{stock_name}] 주가 데이터")
st.dataframe(df.head())

graph = df['Close'].plot(grid=True, figsize=(15, 5))
graph.set_title("그래프") 
graph.set_xlabel("기간")             
graph.set_ylabel("주가")                   
fig = graph.get_figure()   

st.pyplot(fig)

csv_data = df.to_csv()  
excel_data = BytesIO()      
df.to_excel(excel_data)     

st.download_button(
    label="CSV 파일 다운로드",
    data=csv_data,
    file_name='stock_df.csv',
)

st.download_button(
    label="엑셀 파일 다운로드",
    data=excel_data,
    file_name='stock_df.xlsx'
)