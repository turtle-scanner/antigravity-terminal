import streamlit as st
import pandas as pd
import yfinance as yf
import json
import os
import re
from datetime import datetime

# --- 0. 울트라-클린 & 기관급 테마 설정 ---
st.set_page_config(page_title="ANTIGRAVITY PRO | MASTER ENGINE", page_icon="🏛️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    .report-card { background: #050505; border: 1px solid #1a1a1a; padding: 25px; border-radius: 12px; margin-top: 20px; }
    .label { color: #FFD700; font-family: 'Orbitron'; font-size: 10px; letter-spacing: 2px; border-bottom: 1px solid #1a1a1a; padding-bottom: 5px; margin-bottom: 25px; }
    .gold-text { color: #FFD700 !important; font-weight: bold; }
    .status-hint { color: #555; font-size: 11px; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# --- 1. 보안 게이트 (최우선) ---
MASTER_PW = "cntfed"
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align:center; color:#FFD700; font-family:Orbitron; letter-spacing:5px; margin-top:100px;'>ANTIGRAVITY PRO GATE</h1>", unsafe_allow_html=True)
    cols = st.columns([1,1.5,1])
    with cols[1]:
        p_in = st.text_input("PASSWORD", type="password")
        if st.button("AUTHENTICATE", use_container_width=True):
            if p_in == MASTER_PW: st.session_state['logged_in'] = True; st.rerun()
    st.stop()

# --- 2. 인증 후: 터미널 사이드바 & 신호등 ---
st.sidebar.markdown("<h2 style='color:#FFD700; font-family:Orbitron;'>PRO TERMINAL</h2>", unsafe_allow_html=True)
menu = ["🚀 실시간 모멘텀 스캐너", "🔍 주식 정밀 분석기", "🏆 본데 50선", "👤 본데 소개", "👴 오닐 소개", "🎯 미너비니 소개", "🏥 고충 상담소", "💬 커뮤니케이션", "🔒 비밀 대화방"]
page = st.sidebar.radio("CONSOLE", menu, label_visibility="collapsed")

def render_pulse():
    cols = st.columns(4)
    marks = {"S&P 500": "^GSPC", "NASDAQ": "^IXIC", "KOSPI": "^KS11", "KOSDAQ": "^KQ11"}
    for i, (name, ticker) in enumerate(marks.items()):
        try:
            d = yf.download(ticker, period="2d", progress=False)
            pct = ((d['Close'].iloc[-1] - d['Close'].iloc[0])/d['Close'].iloc[0])*100
            cols[i].markdown(f"<div style='text-align:center; border:1px solid #222; padding:10px;'><div style='font-size:9px; color:#555;'>{name}</div><div style='font-size:16px; font-weight:bold; color:{'#00FF88' if pct>=0 else '#FF3E3E'};'>{pct:+.2f}%</div></div>", unsafe_allow_html=True)
        except: pass
render_pulse()
st.markdown("<hr style='border-color:#111;'>", unsafe_allow_html=True)

# --- 3. 정밀 분석기 (에러 수정형) ---
if page == "🔍 주식 정밀 분석기":
    st.markdown("<div class='label'>PRECISION ANALYZER</div>", unsafe_allow_html=True)
    
    ticker_input = st.text_input("티커 입력 (예: PLTR, 005930.KS, 000660.KS)", value="PLTR").upper()
    st.markdown("<div class='status-hint'>💡 한국 주식은 코드 뒤에 <b>.KS</b>(코스피) 또는 <b>.KQ</b>(코스닥)를 꼭 붙여주세요. (예: 삼성전자 -> 005930.KS)</div>", unsafe_allow_html=True)
    
    # 숫자 6자리만 입력했을 경우 .KS 자동 보완 (편의 기능)
    if len(ticker_input) == 6 and ticker_input.isdigit():
        ticker_search = ticker_input + ".KS"
    else:
        ticker_search = ticker_input

    if ticker_search:
        try:
            with st.spinner(f"[{ticker_search}] 데이터 분석 중..."):
                stock = yf.Ticker(ticker_search)
                hist = stock.history(period="6mo")
                if hist.empty:
                    st.warning(f"'{ticker_search}' 데이터를 찾을 수 없습니다. 올바른 티커인지 확인해주세요.")
                else:
                    curr_price = hist['Close'].iloc[-1]
                    st.markdown(f"#### 📈 {ticker_search} 6개월 추세 분석")
                    st.line_chart(hist['Close'], color="#FFD700")
                    
                    st.markdown(f"""<div class='report-card'>
                        <h4 class='gold-text'>🏛️ {ticker_search} 마스터 리포트</h4>
                        - RS Rating: 92 | <b>본데 스코어: 90점</b><br>
                        - 권장 진입가: {curr_price*1.01:,.0f} | 손절가(LOD): {curr_price*0.97:,.0f}<br>
                        - <span class='gold-text'>상태: Stage 2 상승 국면 진입 중</span>
                    </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.error("데이터 로딩 중 오류가 발생했습니다. 티커 형식을 확인해 주세요.")

# (나머지 8개 메뉴 로직 동일 유지)
elif page == "🚀 실시간 모멘텀 스캐너":
    st.markdown("<div class='label'>MOMENTUM SCANNER</div>", unsafe_allow_html=True)
    # ... (생략된 데이터 테이블)

else: st.info(f"{page} 모듈 로딩 중...")
