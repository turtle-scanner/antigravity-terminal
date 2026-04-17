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
    .msg-bubble { background: #111; border: 1px solid #222; padding: 15px; border-radius: 12px; margin-bottom: 12px; }
    .counsel-box { background: #1E1E2E; border: 1px solid #3E3E5E; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
    .label { color: #FFD700; font-family: 'Orbitron'; font-size: 10px; letter-spacing: 2px; border-bottom: 1px solid #1a1a1a; padding-bottom: 5px; margin-bottom: 25px; }
    .tag-badge { background: rgba(255, 215, 0, 0.1); color: #FFD700; padding: 2px 6px; border-radius: 4px; font-family: 'Orbitron'; font-size: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 1. 데이터베이스 유틸리티 ---
COUNSEL_DB = "counsel_db.json"
COMM_DB = "community_log.json"

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f: return json.load(f)
    return []

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)

# --- 2. 보안 게이트웨이 ---
MASTER_PW = "cntfed"

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align:center; color:#FFD700; font-family:Orbitron; letter-spacing:5px; margin-top:100px;'>ANTIGRAVITY PRO GATE</h1>", unsafe_allow_html=True)
    cols = st.columns([1,2,1])
    with cols[1]:
        u, p = st.text_input("ID"), st.text_input("PW", type="password")
        if st.button("AUTHENTICATE"):
            if u == "cntfed" and p == MASTER_PW: st.session_state['logged_in'] = True; st.rerun()
    st.stop()

# --- 3. 마켓 신호등 ---
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

# --- 4. 사이드바 메뉴 ---
st.sidebar.markdown("<h2 style='color:#FFD700; font-family:Orbitron;'>PRO TERMINAL</h2>", unsafe_allow_html=True)
menu = ["🚀 실시간 모멘텀 스캐너", "🔍 주식 정밀 분석기", "🏆 본데 50선", "👤 본데 소개", "👴 오닐 소개", "🎯 미너비니 소개", "🏥 고충 상담소", "💬 커뮤니케이션", "🔒 비밀 대화방"]
page = st.sidebar.radio("CONSOLE", menu, label_visibility="collapsed")

# 전문가 마스터 권한 (통합 암호 적용)
admin_mode = False
with st.sidebar:
    st.markdown("---")
    master_auth = st.text_input("전문가 전용 KEY (cntfed)", type="password")
    if master_auth == MASTER_PW: admin_mode = True; st.sidebar.success("마스터 권한 승인됨")

# --- 5. 페이지 구현 모듈 ---

# [상담소 로직]
if page == "🏥 고충 상담소":
    st.markdown("<div class='label'>COUNSELLING CENTER</div>", unsafe_allow_html=True)
    with st.expander("💌 상담 신청서 작성"):
        with st.form("c_form", clear_on_submit=True):
            nick, stock = st.text_input("닉네임"), st.text_input("종목")
            cont = st.text_area("고민 내용")
            if st.form_submit_button("신청") and cont:
                db = load_json(COUNSEL_DB)
                db.append({"id": len(db)+1, "date": datetime.now().strftime("%Y-%m-%d"), "nickname": nick, "stock": stock, "content": cont, "reply": "", "status": "답변 대기"})
                save_json(COUNSEL_DB, db); st.success("접수됨")
    
    posts = load_json(COUNSEL_DB)
    for p in reversed(posts):
        st.markdown(f"<div class='counsel-box'><b>{p['nickname']}님</b> ({p['status']})<br>{p['content']}{f'<br><hr><b>🐢 처방:</b> {p['reply']}' if p['reply'] else ''}</div>", unsafe_allow_html=True)
        if admin_mode:
            with st.expander("답변 달기"):
                ans = st.text_area("내용", key=f"ans_{p['id']}")
                if st.button("발송", key=f"btn_{p['id']}"):
                    db = load_json(COUNSEL_DB)
                    for item in db:
                        if item['id'] == p['id']: item['reply'] = ans; item['status'] = "상담 완료"
                    save_json(COUNSEL_DB, db); st.rerun()

# [커뮤니케이션 피드 로직]
elif page == "💬 커뮤니케이션":
    st.markdown("<div class='label'>DIGITAL AGORA</div>", unsafe_allow_html=True)
    with st.form("feed_form", clear_on_submit=True):
        msg = st.text_input("메시지 입력 (#티커 태그 가능)")
        if st.form_submit_button("PUSH") and msg:
            db = load_json(COMM_DB)
            db.append({"id": len(db)+1, "time": datetime.now().strftime("%H:%M"), "nick": "사용자", "msg": msg})
            save_json(COMM_DB, db); st.rerun()
    
    msgs = load_json(COMM_DB)
    for m in reversed(msgs):
        st.markdown(f"<div class='msg-bubble'><b>{m['nick']}</b>: {m['msg']}</div>", unsafe_allow_html=True)
        if admin_mode:
            if st.button(f"삭제 #{m['id']}", key=f"del_{m['id']}"):
                db = [i for i in load_json(COMM_DB) if i['id'] != m['id']]
                save_json(COMM_DB, db); st.rerun()

else: st.info(f"{page} 모듈 활성화 대기 중")
