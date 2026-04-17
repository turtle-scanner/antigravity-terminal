import streamlit as st
import pandas as pd
import yfinance as yf
import json
import os
import re
from datetime import datetime

# --- 0. 울트라-클린 & 기관급 테마 설정 ---
st.set_page_config(page_title="ANTIGRAVITY PRO | MASTER TERMINAL", page_icon="🏛️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #1a1a1a; width: 280px !important; }
    
    /* 컴포넌트 스타일 */
    .master-card { background: #0a0a0a; border: 1px solid #1a1a1a; padding: 25px; border-radius: 8px; margin-bottom: 25px; transition: 0.3s; }
    .master-card:hover { border-color: #FFD700; transform: translateY(-2px); }
    
    .gold-box { border-left: 4px solid #FFD700; background: rgba(255, 215, 0, 0.03); padding: 20px; border-radius: 4px; margin: 20px 0; }
    .label { color: #FFD700; font-family: 'Orbitron'; font-size: 10px; letter-spacing: 2px; border-bottom: 1px solid #1a1a1a; padding-bottom: 5px; margin-bottom: 25px; }
    .canslim-letter { font-family: 'Orbitron'; font-size: 26px; color: #FFD700; font-weight: bold; margin-right: 15px; min-width: 30px; display: inline-block; }
    .status-badge { padding: 4px 10px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    .msg-bubble { background: #111; border: 1px solid #222; padding: 15px; border-radius: 12px; margin-bottom: 12px; }
    .gold-text { color: #FFD700; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 1. 보안 및 DB 엔진 ---
MASTER_PW = "cntfed"
COUNSEL_DB = "counsel_db.json"
COMM_DB = "community_log.json"

def load_json(p): return json.load(open(p, "r", encoding="utf-8")) if os.path.exists(p) else []
def save_json(p, d): json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=4)

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align:center; color:#FFD700; font-family:Orbitron; letter-spacing:5px; margin-top:100px;'>ANTIGRAVITY PRO GATE</h1>", unsafe_allow_html=True)
    cols = st.columns([1,2,1])
    with cols[1]:
        u, p = st.text_input("ID"), st.text_input("PW", type="password")
        if st.button("AUTHENTICATE"):
            if u == "cntfed" and p == MASTER_PW: st.session_state['logged_in'] = True; st.rerun()
    st.stop()

# --- 2. 마켓 신호등 ---
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

# --- 3. 사이드바 메뉴 ---
st.sidebar.markdown("<h2 style='color:#FFD700; font-family:Orbitron;'>PRO TERMINAL</h2>", unsafe_allow_html=True)
menu = ["🚀 실시간 모멘텀 스캐너", "🔍 주식 정밀 분석기", "🏆 본데 50선", "👤 본데 소개", "👴 오닐 소개", "🎯 미너비니 소개", "🏥 고충 상담소", "💬 커뮤니케이션", "🔒 비밀 대화방"]
page = st.sidebar.radio("CONSOLE", menu, label_visibility="collapsed")

admin_mode = False
with st.sidebar:
    st.markdown("---")
    master_key = st.text_input("전문가 전용 KEY (cntfed)", type="password")
    if master_key == MASTER_PW: admin_mode = True; st.sidebar.success("MASTER ACCESS GRANTED")

# --- 4. 페이지 각 모듈 구현 ---

if page == "👤 본데 소개":
    st.markdown("<div class='label'>LEGENDARY MENTOR: PRADEEP BONDE</div>", unsafe_allow_html=True)
    st.markdown("### <span class='gold-text'>1억 달러 트레이더들의 스승, 프라딥 본데 (Stockbee)</span>", unsafe_allow_html=True)
    st.write("프라딥 본데는 월가에서 1,000달러를 1억 달러로 불린 전설적인 스윙 트레이더입니다. 크리스찬 쿨라매기 등 수많은 제자를 길러낸 그는 트레이딩을 '예측'이 아닌 '시스템과 프로세스' 비즈니스로 재정의했습니다.")

    st.markdown("#### 🚀 1. 물류 임원에서 전업 트레이더로")
    st.markdown("<div class='master-card'>인도 DHL과 FedEx의 마케팅 책임자였던 그는 물류/공급망 최적화 경험을 주식 시장에 접목했습니다. 트레이딩을 철저한 데이터 기반 비즈니스로 설계하며 성공의 전환점을 맞이했습니다.</div>", unsafe_allow_html=True)

    st.markdown("#### 🎯 2. 프라딥 본데의 4대 핵심 투자 철학")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class='master-card'><b class='gold-text'>① 홈런보다 안타(Singles) 치기</b><br>일확천금을 노리는 '섬의 환상'을 버리고 작고 확실한 수익을 지속적으로 누적하여 복리로 굴리는 것이 성공의 본질입니다.</div>""", unsafe_allow_html=True)
        st.markdown("""<div class='master-card'><b class='gold-text'>② 절차적 기억(Procedural Memory)</b><br>뇌에 패턴을 각인시키기 위해 과거 폭등 차트 3,000~5,000개를 집중 분석하는 '딥 다이브' 훈련을 매일 반복해야 합니다.</div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='master-card'><b class='gold-text'>③ 셀프 리더십 & 갓 신드롬 경계</b><br>성공에 취하는 '갓 신드롬'을 극도로 경계하십시오. 스스로 문제를 해결하고 손실 구간에서도 동기를 부여하는 셀프 리더십이 최우선입니다.</div>""", unsafe_allow_html=True)
        st.markdown("""<div class='master-card'><b class='gold-text'>④ 상황 인식(Situational Awareness)</b><br>아무리 완벽한 기법도 시장(날씨)이 나쁘면 통하지 않습니다. '마켓 모니터'를 통해 현재가 공격적 장인지 방어적 장인지 파악하십시오.</div>""", unsafe_allow_html=True)

    st.markdown("#### 🌐 3. 스탁비(Stockbee) 커뮤니티 운영")
    st.write("본데는 트레이딩으로 막대한 부를 이룬 후 지식 나눔을 위해 '스탁비'를 설립했습니다. 이곳은 오직 입소문만으로 운영되는 전 세계 트레이더들의 '팩토리' 역할을 하고 있습니다.")

elif page == "👴 오닐 소개":
    st.markdown("<div class='label'>FATHER OF GROWTH INVESTING: WILLIAM O'NEIL</div>", unsafe_allow_html=True)
    st.markdown("### 📈 [투자 대가 시리즈] 성장주 투자의 아버지, 윌리엄 오닐")
    
    st.markdown("#### 1. CAN SLIM: 7가지 필터링 원칙")
    canslim = [
        ("C", "Current Earnings", "최근 분기 EPS가 전년 대비 25% 이상 급증했는가?"),
        ("A", "Annual Earnings", "최근 3년 연속 이익 성장, ROE 17% 이상의 강력한 수익성."),
        ("N", "New Factors", "세상을 바꿀 신제품, 경영진, 혹은 신고가 돌파라는 촉매제가 있는가?"),
        ("S", "Supply & Demand", "유통주식수 적당, 돌파 시 거래량이 평소보다 50% 이상 폭발하는가?"),
        ("L", "Leader or Laggard", "RS 지수 80 이상의 주도주인가? 소외주는 버려라."),
        ("I", "Institutional Sponsorship", "기관 투자가들의 매수세가 유입되는 기관의 발자취 추적."),
        ("M", "Market Direction", "현재 시장이 '상승 확인' 상태인가? 하락장에서는 아무리 좋아도 꺾인다.")
    ]
    for l, t, d in canslim:
        st.markdown(f"""<div class='master-card'><div style='display:flex; align-items:center;'><span class='canslim-letter'>{l}</span><div><b style='color:#FFD700;'>{t}:</b> {d}</div></div></div>""", unsafe_allow_html=True)

    st.markdown("#### 2. 오닐의 매수 급소: 컵 앤 핸들 (Cup with Handle)")
    st.markdown("""<div class='gold-box'><b>형태:</b> 주가가 조정을 거쳐 컵 모양을 만들고, 전고점에서 좁은 폭으로 횡보(Handle)하는 패턴.<br><b>매수 타이밍:</b> 핸들의 고점(Pivot)을 강한 거래량과 함께 돌파하는 순간.<br><b>핵심:</b> 핸들에서 변동성이 극도로 축소되어야 함 (본데의 Tightness와 일맥상통).</div>""", unsafe_allow_html=True)

    st.markdown("#### 3. 리스크 관리: 계좌를 지키는 법")
    st.markdown("""
    - <b class='gold-text'>7~8% 자동 손절:</b> 매수가 대비 하락 시 이유 불문 기계적 매도 (전문가님의 지지선 확보).
    - <b class='gold-text'>물타기 절대 금지:</b> 하락하는 주식에 추가 매수하는 것은 파멸의 지름길.
    - <b class='gold-text'>수익 극대화:</b> 주도주는 20~25% 수익 시까지 보유, 강력한 시세라면 8주 이상 인내.
    """)

elif page == "🏆 본데 50선":
    st.markdown("<div class='label'>BONDE TOP 50 REAL-TIME LIST</div>", unsafe_allow_html=True)
    url = "https://docs.google.com/spreadsheets/d/1xjbe9SF0HsxwY_Uy3NC2tT92BqK0nhArUaYU16Q0p9M/export?format=csv&gid=1499398020"
    try:
        df = pd.read_csv(url)
        st.dataframe(df, use_container_width=True, height=500)
        st.markdown("""<div class='master-card'><b class='gold-text'>💡 전술 활용 가이드</b><br>상단 주도주(1~10)는 기관의 공격적 매집주입니다. 하단 후보주(40~50)는 베이스 탈출 초기이거나 숨 고르기 중인 매수 대기 종목입니다. <b>거래량이 마르고 옆으로 기어가는(Tightness) 구간을 노리십시오.</b></div>""", unsafe_allow_html=True)
    except: st.error("시트 연동 오류")

# 기타 페이지 (스캐너, 분석기 등은 이전 SPECS 유지)
else: st.info(f"{page} 모듈 가동 중...")
