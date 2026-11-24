import streamlit as st
import requests
import re

# ==========================================
# [PAGE CONFIG]
# ==========================================
st.set_page_config(
    page_title="NICHERADAR // TECHNICAL GEAR ARCHIVE",
    page_icon="▪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# [MODERN EDITORIAL & DARK MINIMALIST CSS]
# ==========================================
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&display=swap');

/* 전체 배경 및 기본 타이포그래피 */
.stApp {
    background-color: #0A0A0A;
    color: #EAEAEA;
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* 기본 Streamlit 상단 여백/헤더/푸터 정리 */
header[data-testid="stHeader"] {
    background-color: rgba(10, 10, 10, 0.85);
    backdrop-filter: blur(10px);
}
#MainMenu, footer {visibility: hidden;}
.block-container {
    padding-top: 2.2rem;
    padding-bottom: 4rem;
    max-width: 1380px;
}

/* 상단 에디토리얼 마스트헤드 */
.masthead {
    border-bottom: 1px solid #222222;
    padding-bottom: 1.2rem;
    margin-bottom: 1.8rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    flex-wrap: wrap;
    gap: 12px;
}
.masthead-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #FFFFFF;
    line-height: 1;
}
.masthead-accent {
    color: #D4FF00;
}
.masthead-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #777777;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* 라디오 버튼 -> 모던 엣지 탭 스타일 변환 */
div[role="radiogroup"] {
    flex-direction: row;
    gap: 8px;
    flex-wrap: wrap;
    border-bottom: 1px solid #1E1E1E;
    padding-bottom: 14px;
    margin-bottom: 24px;
}
div[role="radiogroup"] > label {
    background-color: #111111;
    border: 1px solid #262626;
    border-radius: 0px !important;
    padding: 8px 16px !important;
    margin: 0 !important;
    transition: all 0.15s ease;
    cursor: pointer;
}
div[role="radiogroup"] > label:hover {
    border-color: #666666;
    background-color: #181818;
}
div[role="radiogroup"] > label[data-checked="true"] {
    background-color: #EAEAEA !important;
    border-color: #EAEAEA !important;
}
div[role="radiogroup"] > label[data-checked="true"] p {
    color: #0A0A0A !important;
    font-weight: 700 !important;
}
div[role="radiogroup"] label > div:first-child {
    display: none !important;
}
div[role="radiogroup"] p {
    font-family: 'JetBrains Mono', 'Pretendard', monospace;
    font-size: 0.82rem;
    letter-spacing: 0.03em;
    color: #A0A0A0;
}

/* 컨테이너 보더(카드) 미니멀 샤프 스타일 */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #111111 !important;
    border: 1px solid #222222 !important;
    border-radius: 0px !important;
    padding: 16px !important;
    transition: border-color 0.2s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #555555 !important;
}

/* 태그 & 배지 */
.tag-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    color: #0A0A0A;
    background-color: #D4FF00;
    padding: 3px 7px;
    display: inline-block;
    margin-bottom: 10px;
    text-transform: uppercase;
}
.tag-outline {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #999999;
    border: 1px solid #333333;
    padding: 2px 7px;
    display: inline-block;
    margin-bottom: 10px;
    text-transform: uppercase;
}

/* 카드 텍스트 */
.card-brand {
    font-family: 'JetBrains Mono', 'Pretendard', monospace;
    font-size: 1.05rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.02em;
    margin-bottom: 6px;
}
.card-desc {
    font-size: 0.82rem;
    color: #7A7A7A;
    line-height: 1.45;
    min-height: 38px;
    margin-bottom: 14px;
}
.prod-title {
    font-size: 0.95rem;
