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
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #1a1a1a; width: 280px !important; }
    
    .secret-box { background: #080808; border: 1px solid #222; padding: 30px; border-radius: 8px; border-top: 4px solid #FFD700; margin-bottom: 30px; }
    .stage-title { font-family: 'Orbitron'; color: #FFD700; margin-top: 25px; margin-bottom: 10px; border-bottom: 1px solid #222; padding-bottom: 5px; }
    .secret-ticker { background: rgba(255, 215, 0, 0.05); border: 1px dashed #FFD700; padding: 15px; border-radius: 4px; margin-top: 15px; }
    .label { color: #FFD700; font-family: 'Orbitron'; font-size: 10px; letter-spacing: 2px; border-bottom: 1px solid #1a1a1a; padding-bottom: 5px; margin-bottom: 25px; }
    .gold-text { color: #FFD700; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 1. 보안 유틸리티 ---
MASTER_PW = "cntfed"
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align:center; color:#FFD700; font-family:Orbitron; letter-spacing:5px; margin-top:100px;'>ANTIGRAVITY PRO GATE</h1>", unsafe_allow_html=True)
    cols = st.columns([1,2,1])
    with cols[1]:
        if st.button("OPEN ARCHIVE"): st.session_state['logged_in'] = True; st.rerun()
    st.stop()

# --- 2. 사이드바 메뉴 ---
st.sidebar.markdown("<h2 style='color:#FFD700; font-family:Orbitron;'>PRO TERMINAL</h2>", unsafe_allow_html=True)
menu = ["🚀 실시간 모멘텀 스캐너", "🔍 주식 정밀 분석기", "🏆 본데 50선", "👤 본데 소개", "👴 오닐 소개", "🎯 미너비니 소개", "🏥 고충 상담소", "💬 커뮤니케이션", "🔒 비밀 대화방"]
page = st.sidebar.radio("CONSOLE", menu, label_visibility="collapsed")

# --- 3. 마켓 신호등 ---
def render_pulse():
    cols = st.columns(4)
    marks = {"S&P 500": "^GSPC", "NASDAQ": "^IXIC", "KOSPI": "^KS11", "KOSDAQ": "^KQ11"}
    for i, (name, ticker) in enumerate(marks.items()):
        try:
            d = yf.download(ticker, period="2d", progress=False)
            curr, prev = d['Close'].iloc[-1], d['Close'].iloc[0]
            pct = ((curr - prev)/prev)*100
            color = "#00FF88" if pct>=0 else "#FF3E3E"
            cols[i].markdown(f"<div style='text-align:center; border:1px solid #1a1a1a; padding:10px;'><div style='font-size:9px; color:#555;'>{name}</div><div style='font-size:16px; font-weight:bold; color:{color};'>{pct:+.2f}%</div></div>", unsafe_allow_html=True)
        except: pass
render_pulse()
st.markdown("<br>", unsafe_allow_html=True)

# --- 4. 페이지 구현 ---

if page == "🔒 비밀 대화방":
    st.markdown("<div class='label'>ENCRYPTED ARCHIVE: MAGNA 53+ PROTOCOL</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='secret-box'>
        <h3 style='color:#FFD700; margin-top:0;'>㊙️ [금기된 전략] 본데의 MAGNA 53+ CAP 10x10 마스터 플랜</h3>
        <p style='color:#888;'>이곳의 정보는 외부 유출을 금하며, 오직 데이터의 힘을 믿는 마스터 트레이더만을 위해 공개됩니다.</p>
        
        <h4 class='stage-title'>1단계: 펀더멘탈 및 수급 조건 검색</h4>
        <ul>
            <li><b class='gold-text'>시가총액 (CAP 10)</b>: 100억 달러 이하 (폭발력은 1억~10억 달러 사이 중소형주에서 극대화)</li>
            <li><b class='gold-text'>상장 주기 (10x10)</b>: IPO 후 10년 이내의 젊은 기업</li>
            <li><b class='gold-text'>이익 가속 (M)</b>: EPS 성장률 100% 이상 (세 자릿수) 또는 흑자 전환</li>
            <li><b class='gold-text'>매출 가속 (A)</b>: 2분기 연속 39%↑ (속이기 힘든 선행 지표)</li>
            <li><b class='gold-text'>숏 스퀴즈 연료 (5)</b>: 공매도 상환 소요일(DTC) 5일 이상</li>
        </ul>

        <h4 class='stage-title'>2단계: 기술적 검색식 (TC2000/트레이딩뷰)</h4>
        <ul>
            <li><b class='gold-text'>시가 갭 상승 (G)</b>: O >= C(1) * 1.04 (최소 4% 이상 갭상승)</li>
            <li><b class='gold-text'>폭발적 거래량 (Vol)</b>: V >= AVGV50 * 2 (이상적으로는 3~5배 폭발)</li>
            <li><b class='gold-text'>9 Million 룰</b>: 사유를 모르더라도 9,000,000주 이상 터진 종목은 즉각 포착</li>
        </ul>

        <h4 class='stage-title'>3단계: 정성적 필터링 (수동 체크)</h4>
        <ul>
            <li><b class='gold-text'>소외 (N - Neglect)</b>: 최근 3년 이내 철저한 시장 무관심과 횡보를 거쳤는가?</li>
            <li><b class='gold-text'>사회적 증거 (A & 3)</b>: 발표 직후 최소 3곳의 애널리스트가 목표가 상향했는가?</li>
            <li><b class='gold-text'>강력한 촉매제</b>: 어닝 서프라이즈, FDA 승인 등 기업의 운명을 바꿀 뉴스가 있는가?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔍 [LIVE] MAGNA 53+ 필터 적용 종목 (High-Conviction)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='secret-ticker'>
            <b class='gold-text'>🇺🇸 CAVA (Cava Group)</b><br>
            - 상태: <b>Classic EP 포진</b><br>
            - 사유: CAP 10B 이내, 매출 50%↑, 상장 초기, 강력한 갭돌파 완료
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='secret-ticker'>
            <b class='gold-text'>🇰🇷 알테오젠 (196170)</b><br>
            - 상태: <b>스토리/계약형 EP</b><br>
            - 사유: 장기 소외 구간 탈출, 빅파마 독점 계약 촉매제, 거래량 10배 폭발
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><p style='font-size:12px; color:#555;'>💡 프라딥 본데 조언: 클래식 EP는 1년에 10~12번뿐입니다. 무작정 매수하기보다 '소외된 상태(N)'에서 '폭발적 거래량'이 동반되는 핵심 종목에 장 초반 30분 내로 승부를 보십시오.</p>", unsafe_allow_html=True)

elif page == "🚀 실시간 모멘텀 스캐너":
    # (기존 모직 유지)
    st.markdown("<div class='label'>MOMENTUM SCANNER</div>")
    # ... (생략)

else: st.info(f"{page} 모듈 로딩 중...")
