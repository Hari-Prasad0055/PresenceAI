import streamlit as st
import base64
from pathlib import Path

def global_header(show_auth=False, user_name=None, portal_type="AI Portal", show_home=True):
    logo_path = Path(r"C:/Users/uhari/Downloads/ChatGPT Image May 9, 2026, 11_33_26 AM.png")
    img_src = ""
    if logo_path.exists():
        logo_base64 = base64.b64encode(logo_path.read_bytes()).decode()
        img_src = f"data:image/png;base64,{logo_base64}"

    greeting_html = f'<span style="color:#64748B;font-weight:600;font-size:14px;margin-right:110px;">Hi, {user_name}</span>' if show_auth and user_name else ''

    # ── CSS (no HTML here) ────────────────────────────────────────────────────
    st.markdown(f"""<style>
        .presence-nav{{position:fixed;top:0;left:0;width:100vw;height:72px;background:#fff;
            border-bottom:1px solid #E2E8F0;box-shadow:0 1px 8px rgba(0,0,0,.06);
            z-index:99999;display:flex;align-items:center;justify-content:center;}}
        .presence-nav-inner{{width:100%;max-width:1200px;padding:0 24px;display:flex;
            align-items:center;justify-content:space-between;}}
        .nav-brand-name{{font-size:22px;font-weight:900;color:#0f172a;line-height:1.1;letter-spacing:-.5px;}}
        .nav-brand-name span{{background:linear-gradient(90deg,#4F6EF7,#7C3AED);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
        .nav-badge{{font-size:11px;font-weight:700;color:#64748B;letter-spacing:.12em;text-transform:uppercase;margin-top:2px;}}
        .nav-logo-el{{width:44px;height:44px;border-radius:12px;object-fit:cover;
            border:1.5px solid rgba(0,0,0,.05);box-shadow:0 4px 12px rgba(0,0,0,.05);
            background:url('{img_src}') center/cover no-repeat;flex-shrink:0;}}
    </style>""", unsafe_allow_html=True)

    # ── HTML (tiny — no base64 here) ─────────────────────────────────────────
    st.markdown(f"""<div class="presence-nav"><div class="presence-nav-inner">
        <div style="display:flex;align-items:center;gap:16px;">
            <div class="nav-logo-el"></div>
            <div><div class="nav-brand-name">presence<span>Ai</span></div>
            <div class="nav-badge">{portal_type}</div></div>
        </div>
        <div style="display:flex;align-items:center;gap:12px;">{greeting_html}</div>
    </div></div>""", unsafe_allow_html=True)

    # ── Logout / Home button ──────────────────────────────────────────────────
    if show_auth:
        st.markdown("""<style>
            div[data-testid="stElementContainer"]:has(#nav-anchor){display:none;}
            div[data-testid="stElementContainer"]:has(#nav-anchor)+div[data-testid="stElementContainer"]{
                position:fixed;top:16px;right:24px;z-index:100000;width:auto!important;}
            @media(min-width:1200px){
                div[data-testid="stElementContainer"]:has(#nav-anchor)+div[data-testid="stElementContainer"]{
                    right:calc((100vw - 1200px)/2 + 24px);}}
            div[data-testid="stElementContainer"]:has(#nav-anchor)+div[data-testid="stElementContainer"] button{
                background:#fff!important;color:#EF4444!important;border:1px solid #EF4444!important;
                border-radius:8px!important;font-weight:600!important;
                min-height:40px!important;height:40px!important;padding:0 16px!important;}
            div[data-testid="stElementContainer"]:has(#nav-anchor)+div[data-testid="stElementContainer"] button:hover{
                background:#EF4444!important;color:#fff!important;}
            div[data-testid="stElementContainer"]:has(#nav-anchor)+div[data-testid="stElementContainer"] button p{
                color:inherit!important;}
        </style>""", unsafe_allow_html=True)
        st.markdown('<span id="nav-anchor"></span>', unsafe_allow_html=True)
        if st.button("Logout", key="header_logout_btn", type="secondary"):
            st.session_state["login_type"] = None
            if "teacher_data" in st.session_state: del st.session_state["teacher_data"]
            if "student_data" in st.session_state: del st.session_state["student_data"]
            st.rerun()

    elif show_home:
        st.markdown("""<style>
            div[data-testid="stElementContainer"]:has(#nav-anchor){display:none;}
            div[data-testid="stElementContainer"]:has(#nav-anchor)+div[data-testid="stElementContainer"]{
                position:fixed;top:16px;right:24px;z-index:100000;width:auto!important;}
            @media(min-width:1200px){
                div[data-testid="stElementContainer"]:has(#nav-anchor)+div[data-testid="stElementContainer"]{
                    right:calc((100vw - 1200px)/2 + 24px);}}
            div[data-testid="stElementContainer"]:has(#nav-anchor)+div[data-testid="stElementContainer"] button{
                min-height:40px!important;height:40px!important;padding:0 16px!important;}
        </style>""", unsafe_allow_html=True)
        st.markdown('<span id="nav-anchor"></span>', unsafe_allow_html=True)
        if st.button("🏠 Home", key="header_home_btn", type="secondary"):
            st.session_state["login_type"] = None
            if "teacher_auth_mode" in st.session_state:
                del st.session_state["teacher_auth_mode"]
            st.rerun()