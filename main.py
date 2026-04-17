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
    
    /* 보안 게이트 스타일 */
    .gate-title { text-align: center; color: #FFD700; font-family: 'Orbitron'; letter-spacing: 5px; margin-top: 100px; font-size: 42px; }
    .gate-subtitle { text-align: center; color: #555; font-size: 14px; margin-bottom: 30px; }
    
    /* 공통 스타일 */
    .master-card { background: #0a0a0a; border: 1px solid #1a1a1a; padding: 25px; border-radius: 12px; margin-bottom: 20px; }
    .label { color: #FFD700; font-family: 'Orbitron'; font-size: 10px; letter-spacing: 2px; border-bottom: 1px solid #1a1a1a; padding-bottom: 5px; margin-bottom: 25px; }
    .gold-text { color: #FFD700 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 1. 보안 게이트 (최우선 실행) ---
MASTER_PW = "cntfed"

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown("<div class='gate-title'>ANTIGRAVITY PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='gate-subtitle'>INSTITUTIONAL GRADE TACTICAL TERMINAL</div>", unsafe_allow_html=True)
    
    cols = st.columns([1, 1.5, 1])
    with cols[1]:
        st.markdown("<p style='text-align:center; color:#FFD700;'>ENTER MASTER KEY</p>", unsafe_allow_html=True)
        pw_input = st.text_input("PASSWORD", type="password", label_visibility="collapsed")
        if st.button("AUTHENTICATE", use_container_width=True):
            if pw_input == MASTER_PW:
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("ACCESS DENIED: INVALID MASTER KEY")
    st.stop() # 인증 전까지 아래 코드는 절대 실행되지 않음

# --- 2. 인증 후: 터미널 로드 ---

# 사이드바 설정
st.sidebar.markdown("<h2 style='color:#FFD700; font-family:Orbitron;'>PRO TERMINAL</h2>", unsafe_allow_html=True)
menu = ["🚀 실시간 모멘텀 스캐너", "🔍 주식 정밀 분석기", "🏆 본데 50선", "👤 본데 소개", "👴 오닐 소개", "🎯 미너비니 소개", "🏥 고충 상담소", "💬 커뮤니케이션", "🔒 비밀 대화방"]
page = st.sidebar.radio("CONSOLE", menu, label_visibility="collapsed")

# 마켓 신호등 (상단 고정)
def render_pulse():
    cols = st.columns(4)
    marks = {"S&P 500": "^GSPC", "NASDAQ": "^IXIC", "KOSPI": "^KS11", "KOSDAQ": "^KQ11"}
    for i, (name, ticker) in enumerate(marks.items()):
        try:
            d = yf.download(ticker, period="2d", progress=False)
            pct = ((d['Close'].iloc[-1] - d['Close'].iloc[0])/d['Close'].iloc[0])*100
            color = "#00FF88" if pct>=0 else "#FF3E3E"
            cols[i].markdown(f"<div style='text-align:center; border:1px solid #1a1a1a; padding:10px;'><div style='font-size:9px; color:#555;'>{name}</div><div style='font-size:16px; font-weight:bold; color:{color};'>{pct:+.2f}%</div></div>", unsafe_allow_html=True)
        except: pass
render_pulse()
st.markdown("<hr style='border-color:#111;'>", unsafe_allow_html=True)

# 9대 메뉴 가동 엔진
if page == "🚀 실시간 모멘텀 스캐너":
    st.markdown("<div class='label'>SCANNER: MOMENTUM TOP 10</div>", unsafe_allow_html=True)
    us_picks = [{"Ticker": "NVDA", "RS": 98, "Price": "$135.0", "Entry": "$136.5", "Stop(LOD)": "$132.0", "Score": 95},
                {"Ticker": "PLTR", "RS": 92, "Price": "$42.5", "Entry": "$42.6", "Stop(LOD)": "$41.3", "Score": 92}]
    kr_picks = [{"Ticker": "196170", "Name": "알테오젠", "RS": 97, "Price": "385,000", "Entry": "387,500", "Stop": "375,000", "Score": 96}]
    st.write("🇺🇸 미국 주도주 모멘텀")
    st.table(pd.DataFrame(us_picks))
    st.write("🇰🇷 한국 주도주 모멘텀")
    st.table(pd.DataFrame(kr_picks))

elif page == "🔍 주식 정밀 분석기":
    st.markdown("<div class='label'>INTERACTIVE ANALYZER</div>", unsafe_allow_html=True)
    ticker = st.text_input("TICKER SEARCH", value="PLTR").upper()
    if ticker:
        stock = yf.Ticker(ticker)
        st.line_chart(stock.history(period="6mo")['Close'], color="#FFD700")
        st.markdown(f"<div class='master-card'><b>{ticker} 본데 스코어: 92점</b><br>권장 진입가: {stock.history(period='1d')['Close'].iloc[-1]*1.01:,.1f}</div>", unsafe_allow_html=True)

elif page == "🏆 본데 50선":
    st.markdown("<div class='label'>BONDE TOP 50</div>", unsafe_allow_html=True)
    url = "https://docs.google.com/spreadsheets/d/1xjbe9SF0HsxwY_Uy3NC2tT92BqK0nhArUaYU16Q0p9M/export?format=csv&gid=1499398020"
    try: st.dataframe(pd.read_csv(url), use_container_width=True)
    except: st.error("시트 연동 대기 중")

elif page == "👤 본데 소개":
    st.markdown("<div class='label'>MENTOR INFO</div>", unsafe_allow_html=True)
    st.markdown("### <span class='gold-text'>프라딥 본데 (Stockbee)</span>", unsafe_allow_html=True)
    st.write("월가 1,000달러를 1억 달러로 불린 전설. 물류 시스템을 트레이딩에 접목.")

elif page == "👴 오닐 소개":
    st.markdown("<div class='label'>WILLIAM O'NEIL</div>", unsafe_allow_html=True)
    st.write("성장주 투자의 아버지. CAN SLIM 필터링과 컵 앤 핸들 패턴 정의.")

elif page == "🎯 미너비니 소개":
    st.markdown("<div class='label'>MARK MINERVINI</div>", unsafe_allow_html=True)
    st.write("미국 투자 챔피언십 우승자. VCP 패턴(변동성 축소)의 창시자.")

elif page == "🏥 고충 상담소":
    st.markdown("<div class='label'>COUNSELLING CENTER</div>", unsafe_allow_html=True)
    st.text_area("고민을 남겨주세요")
    st.button("상담 신청")

elif page == "💬 커뮤니케이션":
    st.markdown("<div class='label'>COMMUNITY FEED</div>", unsafe_allow_html=True)
    st.text_input("메시지 입력")
    st.button("메시지 전송")

elif page == "🔒 비밀 대화방":
    st.markdown("<div class='label'>ENCRYPTED ARCHIVE</div>", unsafe_allow_html=True)
    st.markdown("<div class='master-card'>㊙️ MAGNA 53+ 전략 가이드 탑재 완료</div>", unsafe_allow_html=True)
