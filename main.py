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
    
    .tactical-guide { background: #080808; border: 1px solid #1a1a1a; padding: 25px; border-radius: 12px; margin-top: 30px; border-left: 5px solid #FFD700; }
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

# --- 2. 터미널 사이드바 ---
st.sidebar.markdown("<h2 style='color:#FFD700; font-family:Orbitron;'>PRO TERMINAL</h2>", unsafe_allow_html=True)
menu = ["🚀 실시간 모멘텀 스캐너", "🔍 주식 정밀 분석기", "🏆 본데 50선", "👤 본데 소개", "👴 오닐 소개", "🎯 미너비니 소개", "🏥 고충 상담소", "💬 커뮤니케이션", "🔒 비밀 대화방"]
page = st.sidebar.radio("CONSOLE", menu, label_visibility="collapsed")

# --- 3. 메뉴별 기능 구현 ---

if page == "🏆 본데 50선":
    st.markdown("<div class='label'>REAL-TIME GOOGLE SHEET SYNC: BONDE TOP 50</div>", unsafe_allow_html=True)
    
    # 구글 시트 GID: 1499398020 연결 (CSV Export URL)
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1xjbe9SF0HsxwY_Uy3NC2tT92BqK0nhArUaYU16Q0p9M/export?format=csv&gid=1499398020"
    
    try:
        with st.spinner("본데 50선 리스트 동기화 중..."):
            df = pd.read_csv(SHEET_URL)
            st.dataframe(df, use_container_width=True, height=500)
            
            # 전술 가이드 박스 유지
            st.markdown(f"""
            <div class='tactical-guide'>
                <h4 class='gold-text'>🛠️ [안티그래비티 분석] 프라딥 본데 모멘텀 50 활용 가이드</h4>
                <p>본 리스트는 단순 순위가 아닌 <b>'에너지의 우선순위'</b>입니다.</p>
                <p><b>1. 상단 (1~10)</b>: RS 압도적 주도주, 이미 시세 분출 중인 '가장 뜨거운' 그룹.</p>
                <p><b>2. 하단 (40~50)</b>: 베이스 탈출 초기 종목. 타점을 놓쳤을 때 미리 공부해야 할 '매수 대기' 그룹.</p>
                <div style='background:rgba(255,0,0,0.1); padding:10px; border-radius:4px; margin-top:15px;'>
                    <b class='gold-text'>⚠️ 마스터 코멘트:</b><br>
                    급등 추격 금지! 거래량이 바짝 마르고 횡보하며 <b>에너지가 응축될 때(Tightness)</b> 비로소 사야 합니다.
                </div>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.error("구글 시트 연동에 실패했습니다. 공유 설정(링크가 있는 모든 사용자)을 확인해 주세요.")

# (기타 8개 메뉴 로직 유지)
elif page == "🔍 주식 정밀 분석기":
    st.markdown("<div class='label'>PRECISION ANALYZER</div>", unsafe_allow_html=True)
    # ... (생략된 분석기 검색 로직)

else: st.info(f"{page} 모듈 로딩 중...")
