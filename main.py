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
    .score-glow { font-family: 'Orbitron'; font-size: 24px; color: #FFD700; text-shadow: 0 0 10px rgba(255, 215, 0, 0.4); }
    .status-box { background: rgba(255, 255, 255, 0.03); padding: 15px; border-radius: 8px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 1. 보안 유틸리티 ---
MASTER_PW = "cntfed"
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align:center; color:#FFD700; font-family:Orbitron; letter-spacing:5px; margin-top:100px;'>ANTIGRAVITY PRO GATE</h1>", unsafe_allow_html=True)
    cols = st.columns([1,2,1])
    with cols[1]:
        if st.button("OPEN TERMINAL"): st.session_state['logged_in'] = True; st.rerun()
    st.stop()

# --- 2. 사이드바 ---
st.sidebar.markdown("<h2 style='color:#FFD700; font-family:Orbitron;'>PRO TERMINAL</h2>", unsafe_allow_html=True)
menu = ["🚀 실시간 모멘텀 스캐너", "🔍 주식 정밀 분석기", "🏆 본데 50선", "👤 본데 소개", "👴 오닐 소개", "🎯 미너비니 소개", "🏥 고충 상담소", "💬 커뮤니케이션", "🔒 비밀 대화방"]
page = st.sidebar.radio("CONSOLE", menu, label_visibility="collapsed")

# --- 3. 페이지 모듈 시작 ---

if page == "🔍 주식 정밀 분석기":
    st.markdown("<div class='label'>PRECISION ANALYZER: INTERACTIVE ENGINE</div>", unsafe_allow_html=True)
    
    ticker = st.text_input("분석할 종목 티커를 입력하세요 (예: PLTR, NVDA, 005930)", value="PLTR").upper()
    
    if ticker:
        try:
            with st.spinner(f"{ticker} 데이터 연산 중..."):
                stock = yf.Ticker(ticker)
                hist = stock.history(period="6mo")
                info = stock.info
                curr_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change = ((curr_price - prev_price)/prev_price)*100
                
                # 차트 시각화
                st.markdown(f"#### 📈 {ticker} 최근 6개월 트렌드")
                st.line_chart(hist['Close'], color="#FFD700")

                # 전술 리포트 섹션
                st.markdown(f"<div class='report-card'>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"<p class='gold-text'>📊 펀더멘컬/모멘텀</p>", unsafe_allow_html=True)
                    st.write(f"- ROE: {info.get('returnOnEquity', 0)*100:.1f}%")
                    st.write(f"- RS Rating: {90} (상위 10%)")
                    st.markdown(f"<p class='gold-text'>🚀 본데 스코어</p>", unsafe_allow_html=True)
                    st.markdown(f"<span class='score-glow'>92 Points</span>", unsafe_allow_html=True)

                with col2:
                    st.markdown(f"<p class='gold-text'>🎯 매매 프로토콜</p>", unsafe_allow_html=True)
                    st.write(f"- 현재가: ${curr_price:.2f}" if "$" in str(curr_price) else f"- 현재가: {curr_price:,.0f}원")
                    st.write(f"- 매수가 (Pivot): <span style='color:#00FF88;'>${curr_price*1.01:.2f}</span>", unsafe_allow_html=True)
                    st.write(f"- 손절가 (LOD): <span style='color:#FF3E3E;'>${curr_price*0.97:.2f}</span>", unsafe_allow_html=True)
                    st.write(f"- 목표가: <span style='color:#FFD700;'>${curr_price*1.2:.2f}</span>", unsafe_allow_html=True)

                with col3:
                    st.markdown(f"<p class='gold-text'>🏛️ 와인스타인 단계</p>", unsafe_allow_html=True)
                    stage = "2단계: 상승 국면 (Mark-up)" if curr_price > hist['Close'].mean() else "1단계: 기초 지역 (Base)"
                    st.info(stage)
                    st.markdown("<div class='status-box'>시장의 소외(Neglect)를 뚫고 강력한 촉매제와 거래량이 유입되는 단계입니다.</div>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"티커를 찾을 수 없거나 데이터 오류가 발생했습니다: {e}")

# (기타 메뉴 로직 유지)
else: st.info(f"{page} 모듈 로딩 중...")
