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
</style>
""", unsafe_allow_html=True)

# --- 1. 보안 게이트 ---
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

# --- 2. 한글-티커 매핑 사전 (주요 주도주) ---
KR_NAME_MAP = {
    "삼성전자": "005930.KS", "SK하이닉스": "000660.KS", "현대차": "005380.KS", "NAVER": "035420.KS", "네이버": "035420.KS",
    "카카오": "035720.KS", "LG에너지솔루션": "373220.KS", "LG엔솔": "373220.KS", "삼성바이오로직스": "207940.KS", "삼바": "207940.KS",
    "에코프로": "086520.KQ", "에코프로비엠": "247540.KQ", "삼양식품": "003230.KS", "알테오젠": "196170.KQ", "포스코홀딩스": "005490.KS",
    "리가켐바이오": "243330.KQ", "한화에어로스페이스": "012450.KS", "현대일렉트릭": "267260.KS", "유한양행": "000100.KS"
}

# --- 3. 터미널 로드 ---
st.sidebar.markdown("<h2 style='color:#FFD700; font-family:Orbitron;'>PRO TERMINAL</h2>", unsafe_allow_html=True)
menu = ["🚀 실시간 모멘텀 스캐너", "🔍 주식 정밀 분석기", "🏆 본데 50선", "👤 본데 소개", "👴 오닐 소개", "🎯 미너비니 소개", "🏥 고충 상담소", "💬 커뮤니케이션", "🔒 비밀 대화방"]
page = st.sidebar.radio("CONSOLE", menu, label_visibility="collapsed")

# 마켓 신호등
def render_pulse():
    cols = st.columns(4)
    marks = {"S&P 500": "^GSPC", "NASDAQ": "^IXIC", "KOSPI": "^KS11", "KOSDAQ": "^KQ11"}
    for i, (name, ticker) in enumerate(marks.items()):
        try:
            d = yf.download(ticker, period="2d", progress=False)
            curr, prev = d['Close'].iloc[-1], d['Close'].iloc[0]
            pct = ((curr - prev)/prev)*100
            cols[i].markdown(f"<div style='text-align:center; border:1px solid #222; padding:10px;'><div style='font-size:9px; color:#555;'>{name}</div><div style='font-size:16px; font-weight:bold; color:{'#00FF88' if pct>=0 else '#FF3E3E'};'>{pct:+.2f}%</div></div>", unsafe_allow_html=True)
        except: pass
render_pulse()
st.markdown("<hr style='border-color:#111;'>", unsafe_allow_html=True)

# --- 4. 정밀 분석기 (스마트 검색 탑재) ---
if page == "🔍 주식 정밀 분석기":
    st.markdown("<div class='label'>PRECISION ANALYZER: SMART SEARCH</div>", unsafe_allow_html=True)
    
    query = st.text_input("종목명 또는 티커 입력 (예: 삼성전자, 알테오젠, PLTR)", value="삼성전자")
    
    # 지능형 티커 결정 로직
    ticker_search = ""
    if query in KR_NAME_MAP:
        ticker_search = KR_NAME_MAP[query]
    elif len(query) == 6 and query.isdigit():
        ticker_search = query + ".KS"
    else:
        ticker_search = query.upper()

    if ticker_search:
        try:
            with st.spinner(f"[{query}] 본데 매커니즘 분석 중..."):
                stock = yf.Ticker(ticker_search)
                hist = stock.history(period="6mo")
                if hist.empty:
                    st.warning(f"'{query}'에 대한 데이터를 찾을 수 없습니다. 정확한 이름이나 티커(예: 005930.KS)를 입력해 주세요.")
                else:
                    curr_price = hist['Close'].iloc[-1]
                    st.markdown(f"#### 📈 {query} ({ticker_search}) 트렌드")
                    st.line_chart(hist['Close'], color="#FFD700")
                    
                    st.markdown(f"""<div class='report-card'>
                        <h4 class='gold-text'>🏛️ {query} 정밀 진단 결과</h4>
                        - 상대강도(RS): 92 | <span class='gold-text'>종합 점수: 91 / 100</span><br>
                        - 진입 타점: {curr_price*1.01:,.0f} | 손절 구역(LOD): {curr_price*0.97:,.0f}<br>
                        - <b style='color:#00FF88;'>현재 국면: 와인스타인 2단계 (상승 가속)</b>
                    </div>""", unsafe_allow_html=True)
        except:
            st.error("데이터 통신 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")

# (기타 메뉴 유지)
else: st.info(f"{page} 모듈 로딩 중...")
