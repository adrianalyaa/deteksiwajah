"""
pixel_style.py
----------------
Modul CSS & komponen UI bertema pixel-pink ala PixelFace,
dipakai bersama oleh semua halaman Streamlit (app.py & pages/*.py).
"""

import streamlit as st

PIXEL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&family=Nunito:wght@400;600;700;800&display=swap');

:root {
    --pink: #ffbfe5;
    --pink-dark: #ff8dd4;
    --pink-deeper: #e05fb0;
    --pink-light: #ffd9f0;
    --pixel-black: #1a0a2e;
    --pixel-purple: #6b21a8;
    --white: #ffffff;
    --shadow-pixel: 4px 4px 0px #e05fb0;
    --shadow-dark: 4px 4px 0px #1a0a2e;
}

/* ===== GLOBAL ===== */
html, body, [class*="css"]  {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background-color: var(--pink);
    background-image: radial-gradient(circle, rgba(255,141,212,0.25) 1px, transparent 1px);
    background-size: 28px 28px;
}

/* Sembunyikan header bawaan streamlit biar makin "polos" */
header[data-testid="stHeader"] {
    background: transparent;
}

/* ===== SIDEBAR (dipakai sebagai pengganti navbar) ===== */
section[data-testid="stSidebar"] {
    background: var(--pixel-black);
    border-right: 4px solid var(--pink-dark);
}
section[data-testid="stSidebar"] * {
    color: var(--pink-light) !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-family: 'Press Start 2P', monospace !important;
    color: var(--pink) !important;
    font-size: 13px !important;
    line-height: 1.8 !important;
}

/* ===== HEADINGS ===== */
.pf-eyebrow {
    font-family: 'Press Start 2P', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    color: var(--pixel-purple);
    background: var(--white);
    border: 2px solid var(--pixel-black);
    padding: 6px 14px;
    display: inline-block;
    box-shadow: 3px 3px 0 var(--pixel-black);
    margin-bottom: 18px;
}

.pf-title {
    font-family: 'Press Start 2P', monospace;
    font-size: clamp(18px, 4vw, 34px);
    line-height: 1.7;
    color: var(--pixel-black);
    text-shadow: 4px 4px 0 rgba(255,141,212,0.7);
    margin-bottom: 14px;
}
.pf-title span { color: var(--pixel-purple); display: block; }

.pf-subtitle {
    font-family: 'VT323', monospace;
    font-size: 22px;
    color: #4b0082;
    line-height: 1.5;
    max-width: 700px;
}

.pf-section-tag {
    font-family: 'Press Start 2P', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    color: var(--pixel-purple);
    display: block;
    margin-bottom: 10px;
}

.pf-section-title {
    font-family: 'Press Start 2P', monospace;
    font-size: clamp(13px, 2.4vw, 20px);
    line-height: 1.7;
    color: var(--pixel-black);
    margin-bottom: 14px;
}

.pf-section-desc {
    font-family: 'VT323', monospace;
    font-size: 19px;
    color: #4b0082;
    line-height: 1.5;
    max-width: 720px;
}

/* ===== CARD / BOX ===== */
.pf-card {
    background: var(--white);
    border: 3px solid var(--pixel-black);
    box-shadow: 5px 5px 0 var(--pixel-black);
    padding: 22px;
}
.pf-card-dark {
    background: var(--pixel-black);
    border: 3px solid var(--pink-dark);
    box-shadow: 5px 5px 0 var(--pink-deeper);
    padding: 22px;
    color: var(--pink-light);
}
.pf-card-pink {
    background: var(--pink-light);
    border: 3px solid var(--pixel-black);
    box-shadow: 5px 5px 0 var(--pixel-black);
    padding: 22px;
}

.pf-label {
    font-family: 'Press Start 2P', monospace;
    font-size: 9px;
    color: var(--pixel-purple);
    margin-bottom: 12px;
    letter-spacing: 0.5px;
    display: block;
}
.pf-label-light {
    font-family: 'Press Start 2P', monospace;
    font-size: 9px;
    color: var(--pink-dark);
    margin-bottom: 12px;
    letter-spacing: 0.5px;
    display: block;
}

/* ===== MATH BOX ===== */
.pf-math-box {
    background: #1a0a2e;
    border: 2px solid var(--pink-dark);
    padding: 14px 16px;
    margin-top: 10px;
    font-family: 'VT323', monospace;
    font-size: 17px;
    color: var(--pink-light);
    line-height: 1.7;
}
.pf-math-title {
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    color: var(--pink-dark);
    margin-bottom: 6px;
    display: block;
}

/* ===== STEP FLOW ===== */
.pf-flow-wrap {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}
.pf-flow-step {
    background: var(--pink-light);
    border: 3px solid var(--pixel-black);
    box-shadow: 3px 3px 0 var(--pixel-black);
    padding: 12px 10px;
    width: 150px;
    text-align: center;
}
.pf-flow-step.final {
    background: var(--pixel-black);
    color: var(--pink);
}
.pf-flow-step .num {
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    color: var(--pixel-purple);
    display: block;
    margin-bottom: 6px;
}
.pf-flow-step.final .num { color: var(--pink); }
.pf-flow-step .txt {
    font-family: 'VT323', monospace;
    font-size: 15px;
    line-height: 1.3;
    color: var(--pixel-black);
}
.pf-flow-step.final .txt { color: var(--pink); }
.pf-flow-arrow {
    font-size: 22px;
    color: var(--pixel-purple);
    font-weight: bold;
}

.pf-callout {
    font-family: 'VT323', monospace;
    font-size: 18px;
    color: #3b0072;
    line-height: 1.6;
    background: var(--pink-light);
    border-left: 5px solid var(--pixel-purple);
    padding: 14px 18px;
    margin: 14px 0;
}

/* ===== DIVIDER ===== */
.pf-divider {
    height: 8px;
    background: repeating-linear-gradient(90deg,
        var(--pixel-black) 0px, var(--pixel-black) 16px,
        var(--pink-dark) 16px, var(--pink-dark) 32px,
        var(--pixel-purple) 32px, var(--pixel-purple) 48px,
        var(--pink-dark) 48px, var(--pink-dark) 64px);
    margin: 22px 0;
    border: none;
}

/* ===== BUTTONS (Streamlit native) ===== */
div.stButton > button, div.stDownloadButton > button {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 11px !important;
    background: var(--pixel-black) !important;
    color: var(--pink) !important;
    border: 3px solid var(--pixel-black) !important;
    box-shadow: var(--shadow-pixel) !important;
    border-radius: 0 !important;
    padding: 12px 18px !important;
    transition: transform 0.1s, box-shadow 0.1s !important;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
    background: #2d1a4e !important;
    box-shadow: 6px 6px 0 var(--pink-deeper) !important;
    color: var(--pink) !important;
    border-color: var(--pixel-black) !important;
}
div.stButton > button:active, div.stDownloadButton > button:active {
    transform: translate(3px,3px);
    box-shadow: none !important;
}

/* ===== FILE UPLOADER ===== */
[data-testid="stFileUploaderDropzone"] {
    background: var(--pink-light) !important;
    border: 3px dashed var(--pink-dark) !important;
    border-radius: 0 !important;
}

/* ===== SLIDER ===== */
[data-testid="stSlider"] [role="slider"] {
    background: var(--pixel-purple) !important;
}

/* ===== METRIC / TEAM GRID ===== */
.pf-team-card {
    border: 2px solid var(--pink-dark);
    background: rgba(255,191,229,0.08);
    box-shadow: 3px 3px 0 var(--pink-deeper);
    padding: 16px 10px;
    text-align: center;
}
.pf-team-name {
    font-family: 'Press Start 2P', monospace;
    font-size: 9px;
    color: var(--pink);
    line-height: 1.7;
    margin-bottom: 6px;
}
.pf-team-role {
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    color: var(--pink-dark);
}

/* footer */
.pf-footer {
    text-align: center;
    font-family: 'VT323', monospace;
    color: #4b0082;
    opacity: 0.8;
    padding: 30px 0 10px;
    font-size: 16px;
}
</style>
"""


def inject_css():
    st.markdown(PIXEL_CSS, unsafe_allow_html=True)


def divider():
    st.markdown('<div class="pf-divider"></div>', unsafe_allow_html=True)


def section_header(tag: str, title: str, desc: str = ""):
    st.markdown(f'<span class="pf-section-tag">{tag}</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="pf-section-title">{title}</div>', unsafe_allow_html=True)
    if desc:
        st.markdown(f'<p class="pf-section-desc">{desc}</p>', unsafe_allow_html=True)


def flow_diagram(steps: list[str], final_label: str = "OUTPUT"):
    """Render diagram alur 01 -> 02 -> ... -> OUTPUT ala kartu pixel."""
    html = '<div class="pf-flow-wrap">'
    n = len(steps)
    for i, step in enumerate(steps):
        is_last = i == n - 1
        cls = "pf-flow-step final" if is_last else "pf-flow-step"
        num = f"{i+1:02d}"
        html += f'<div class="{cls}"><span class="num">{num}</span><span class="txt">{step}</span></div>'
        if not is_last:
            html += '<div class="pf-flow-arrow">&rarr;</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def math_box(title: str, body_html: str):
    st.markdown(
        f'<div class="pf-math-box"><span class="pf-math-title">{title}</span>{body_html}</div>',
        unsafe_allow_html=True,
    )


def callout(text: str):
    st.markdown(f'<div class="pf-callout">{text}</div>', unsafe_allow_html=True)
