import streamlit as st
from src.database.db import create_subject
import segno  ## for generating QR code
import io

@st.dialog("Share Subject")
def share_subject_dialog(subject_name,subject_code):
    app_domain = st.secrets["app_domain"]
    join_url = f"{app_domain}join?subject_code={subject_code}"

    st.header("Scan QR code to Join")

    qr = segno.make(join_url)

    out = io.BytesIO()

    qr.save(out, kind='png',scale=10,border=1)

    c1 , c2 = st.columns(2)

    with c1:
        st.markdown('###Copy Link')
        st.code(join_url,language='text')
        st.code(subject_code,language='text')
        st.info("Share the above link or subject code with your students to let them join the class.")
    with c2:
        st.markdown('###QR Code')
        st.image(out.getvalue(),caption="QR code to join the class")

