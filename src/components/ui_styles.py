import streamlit as st
from textwrap import dedent

def inject_global_css():
    st.markdown(dedent("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@700&display=swap');
        
        * {
            box-sizing: border-box;
        }
        
        html, body, [class*="css"], .stApp {
            font-family: 'Inter', sans-serif !important;
            font-size: 15px !important;
            line-height: 1.6 !important;
        }

        h1, h2, h3, h4, h5, h6, .sora-font {
            font-family: 'Sora', sans-serif !important;
            font-weight: 700 !important;
        }

        /* Hide Streamlit elements */
        #MainMenu, header[data-testid="stHeader"], footer {
            visibility: hidden !important;
            display: none !important;
        }
        
        /* Background */
        .stApp {
            background-color: #F5F7FF !important;
            background-image: radial-gradient(rgba(79, 110, 247, 0.06) 2px, transparent 2px) !important;
            background-size: 20px 20px !important;
        }
        
        /* Surface / Cards */
        div[data-testid="stVerticalBlock"] > div[style*="border"], .glass-container, .card {
            background: #FFFFFF !important;
            border-radius: 16px !important;
            box-shadow: 0 2px 16px rgba(80, 100, 200, 0.08) !important;
            border: 1px solid #E2E8F0 !important;
            padding: 24px !important;
        }

        /* Typography */
        p, span, div {
            color: #64748B;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #0F172A !important;
        }
        
        /* Ensure button inner text inherits the correct button color */
        .stButton > button p, .stButton > button span, .stButton > button div {
            color: inherit !important;
        }
        
        /* Welcome Section */
        .welcome-heading {
            font-family: 'Sora', sans-serif !important;
            font-weight: 700 !important;
            color: #0F172A !important;
            font-size: 32px !important;
            margin-bottom: 4px !important;
        }
        
        .welcome-subheading {
            color: #4F6EF7 !important;
            font-size: 12px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.12em !important;
            font-weight: 600 !important;
        }
        
        /* Take AI Attendance Section */
        .attendance-heading {
            background: linear-gradient(90deg, #4F6EF7, #7C3AED) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-family: 'Sora', sans-serif !important;
            font-weight: 700 !important;
            margin-bottom: 16px !important;
            font-size: 28px !important;
        }

        .stSelectbox label {
            color: #64748B !important;
            font-size: 13px !important;
            font-weight: 500 !important;
        }

        /* Buttons */
        
        /* "Take Attendance" CTA (Primary) */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #4F6EF7 0%, #7C3AED 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 10px rgba(79, 110, 247, 0.2) !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            box-shadow: 0 4px 20px rgba(79, 110, 247, 0.4) !important;
            transform: translateY(-2px) !important;
            color: #ffffff !important;
        }
        
        /* Secondary Action Button (Manage Subjects, Attendance Records) */
        .stButton > button[kind="secondary"] {
            background: #ffffff !important;
            color: #0F172A !important;
            border: 1.5px solid #CBD5E1 !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton > button[kind="secondary"]:hover {
            border-color: #4F6EF7 !important;
            color: #4F6EF7 !important;
            background: #F0F4FF !important;
            transform: translateY(-1px) !important;
        }
        
        /* Tertiary Buttons (used for clear all photos, etc) */
        .stButton > button[kind="tertiary"] {
            background: #ffffff !important;
            color: #64748B !important;
            border: 1.5px solid #E2E8F0 !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton > button[kind="tertiary"]:hover {
            border-color: #CBD5E1 !important;
            color: #0F172A !important;
            background: #F8FAFC !important;
        }

        /* "Add Photos" CTA Pill (Custom class handled in python or apply to specific buttons if needed) */
        button[key*="add_photos"] {
            border-radius: 999px !important;
        }

        /* Danger / Logout Button */
        button[key="header_logout_btn"], .btn-danger button {
            background: #ffffff !important;
            color: #EF4444 !important;
            border: 1px solid #EF4444 !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }
        
        button[key="header_logout_btn"]:hover, .btn-danger button:hover {
            background: #EF4444 !important;
            color: #ffffff !important;
        }

        /* Inputs */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div,
        .stNumberInput > div > div > input,
        .stCameraInput > div {
            background: #FFFFFF !important;
            border: 1.5px solid #CBD5E1 !important;
            color: #0F172A !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            font-size: 15px !important;
            transition: all 0.2s ease !important;
            box-shadow: none !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > div:focus,
        .stNumberInput > div > div > input:focus {
            border-color: #4F6EF7 !important;
            box-shadow: 0 0 0 3px rgba(79, 110, 247, 0.15) !important;
            outline: none !important;
        }

        /* Divider */
        hr {
            border-color: #E2E8F0 !important;
            border-top-width: 1px !important;
            margin: 32px 0 !important;
        }
        
        /* DataFrames */
        .stDataFrame, div[data-testid="stTable"] {
            border-radius: 12px !important;
            overflow: hidden !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
            background: #FFFFFF !important;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(100, 116, 139, 0.2);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(100, 116, 139, 0.4);
        }
        
        .main .block-container {
            padding-top: 100px !important;
        }
    </style>
    """), unsafe_allow_html=True)
