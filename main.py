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
    
    /* 텍스트 박스 및 카드 스타일 */
    .master-card { background: #0a0a0a; border: 1px solid #1a1a1a; padding: 25px; border-radius: 8px; margin-bottom: 25px; transition: 0.3s; }
    .master-card:hover { border-color: #FFD700; transform: translateY(-2px); }
    .gold-glow { color: #FFD700; font-weight: bold; text-shadow: 0 0 10px rgba(255, 215, 0, 0.3); }
    .canslim-letter { font-family: 'Orbitron'; font-size: 24px; color: #FFD700; font-weight: bold; margin-right: 15px; }
    .vcp-step { display: flex; align-items: center; justify-content: space-between; background: rgba(255, 255, 255, 0.03); padding: 10px 20px; border-radius: 4px; margin-bottom: 10px; }
    .label { color: #FFD700; font-family: 'Orbitron'; font-size: 10px; letter-spacing: 2px; border-bottom: 1px solid #1a1a1a; padding-bottom: 5px; margin-bottom: 25px; }
    .msg-bubble { background: #111; border: 1px solid #222; padding: 15px; border-radius: 12px; margin-bottom: 12px; }
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
            else: st.error("ACCESS DENIED")
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
            color = "#FF0000" if "KOS" in name and pct>=0 else "#00FF88" if pct>=0 else "#FF3E3E"
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
    if master_key == MASTER_PW: admin_mode = True; st.sidebar.success("마스터 권한 승인")

# --- 4. 페이지 구현 (Full Spec) ---

if page == "🏆 본데 50선":
    st.markdown("<div class='label'>BONDE TOP 50 REAL-TIME LIST</div>", unsafe_allow_html=True)
    url = "https://docs.google.com/spreadsheets/d/1xjbe9SF0HsxwY_Uy3NC2tT92BqK0nhArUaYU16Q0p9M/export?format=csv&gid=1499398020"
    try:
        df = pd.read_csv(url)
        st.dataframe(df, use_container_width=True, height=600)
    except: st.error("구글 시트 연동 오류. 공유 설정을 확인하세요.")

elif page == "👤 본데 소개":
    st.markdown("<div class='label'>PRADEEP BONDE (STOCKBEE)</div>", unsafe_allow_html=True)
    st.markdown("### <span class='gold-glow'>1,000달러를 1억 달러로 만든 시대의 스승</span>", unsafe_allow_html=True)
    st.write("프라딥 본데는 물류 전문가의 시각으로 트레이딩을 '프로세스'화하여 10만 배의 수익률을 거둔 전설입니다.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='master-card'><b>Singles 전략</b>: 일확천금 대신 작고 확실한 수익을 무한 복리로 쌓는 방식.</div>", unsafe_allow_html=True)
        st.markdown("<div class='master-card'><b>Deep Dive</b>: 폭등 차트 3천 개 이상을 분석하여 뇌에 패턴을 각인시키는 훈련.</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='master-card'><b>God Syndrome 경계</b>: 단기 성공에 취한 자만심을 버리고 셀프 리더십 유지.</div>", unsafe_allow_html=True)
        st.markdown("<div class='master-card'><b>상황 인식</b>: 시장 전체의 온도(Breadth)를 측정하여 공격과 방어 결정.</div>", unsafe_allow_html=True)

elif page == "👴 오닐 소개":
    st.markdown("<div class='label'>WILLIAM O'NEIL (CAN SLIM)</div>", unsafe_allow_html=True)
    st.markdown("### 📈 성장주 투자의 아버지, 윌리엄 오닐")
    canslim = [("C", "최근 분기 EPS 25%↑"), ("A", "3년 연속 이익 성장, ROE 17%↑"), ("N", "신제품/신고가 촉매제"), ("S", "공급과 수요(거래량 폭발)"), ("L", "업종 내 주도주(RS 80↑)"), ("I", "기관의 매수 추적"), ("M", "마켓의 상승 확인")]
    for l, d in canslim:
        st.markdown(f"<div class='master-card'><div style='display:flex; align-items:center;'><span class='canslim-letter'>{l}</span><span>{d}</span></div></div>", unsafe_allow_html=True)
    st.info("🎯 컵 앤 핸들: 전고점 부근 변동성 축소(Tightness) 후 대량 거래 돌파 시 매수.")

elif page == "🎯 미너비니 소개":
    st.markdown("<div class='label'>MARK MINERVINI (SEPA/VCP)</div>", unsafe_allow_html=True)
    st.markdown("### 🏆 미국 투자 챔피언, 마크 미너비니")
    st.markdown("#### VCP 패턴 (변동성 축소)")
    st.markdown("""<div class='vcp-step'><span>1차 수축</span><span>-25%</span></div><div class='vcp-step'><span>2차 수축</span><span>-10%</span></div><div class='vcp-step'><span>3차 수축 (Pivot)</span><span style='color:#00FF88;'>-3% (Dry-up)</span></div>""", unsafe_allow_html=True)
    st.success("리스크 관리: 5~7% 기계적 손절, 수익 대 손실 비율 2:1 이상 유지.")

elif page == "🏥 고충 상담소":
    st.markdown("<div class='label'>COUNSELLING CENTER</div>", unsafe_allow_html=True)
    with st.expander("📝 상담 신청"):
        with st.form("c", clear_on_submit=True):
            n, s, c = st.text_input("닉네임"), st.text_input("종목"), st.text_area("내용")
            if st.form_submit_button("상담 신청") and c:
                db = load_json(COUNSEL_DB)
                db.append({"id": len(db)+1, "nickname": n, "stock": s, "content": c, "reply": "", "status": "대기"})
                save_json(COUNSEL_DB, db); st.success("접수완료")
    for p in reversed(load_json(COUNSEL_DB)):
        st.markdown(f"<div class='master-card'><b>{p['nickname']}님</b>: {p['content']}{f'<br><hr>🐢 <b>처방:</b> {p['reply']}' if p['reply'] else ''}</div>", unsafe_allow_html=True)
        if admin_mode:
            with st.expander("답변 달기"):
                ans = st.text_area("의견", key=f"a_{p['id']}")
                if st.button("처방전 전송", key=f"b_{p['id']}"):
                    db = load_json(COUNSEL_DB)
                    for i in db:
                        if i['id'] == p['id']: i['reply'] = ans; i['status'] = "완료"
                    save_json(COUNSEL_DB, db); st.rerun()

elif page == "💬 커뮤니케이션":
    st.markdown("<div class='label'>COMMUNICATION FEED</div>", unsafe_allow_html=True)
    with st.form("msg"):
        msg = st.text_input("메시지 입력 (#NVDA 가즈아!)")
        if st.form_submit_button("PUSH") and msg:
            db = load_json(COMM_DB)
            db.append({"id": len(db)+1, "nick": "사용자", "msg": msg, "time": datetime.now().strftime("%H:%M")})
            save_json(COMM_DB, db); st.rerun()
    for m in reversed(load_json(COMM_DB)):
        st.markdown(f"<div class='msg-bubble'><b>{m['nick']}</b>: {m['msg']}</div>", unsafe_allow_html=True)
        if admin_mode and st.button(f"삭제 #{m['id']}"):
            db = [i for i in load_json(COMM_DB) if i['id'] != m['id']]
            save_json(COMM_DB, db); st.rerun()

else: st.info(f"{page} 모듈 활성화 대기 중")
