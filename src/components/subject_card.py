import streamlit as st

def subject_card(name , code, section, stats=None, footer_callback=None):
    html = f"""
       <div class="glass-container" style="padding: 28px; transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); cursor: default;">
           <div style="display: flex; justify-content: space-between; align-items: flex-start;">
               <div>
                   <h3 style="margin-top: 0; margin-bottom: 8px; color:#f8fafc; font-size:1.6rem; font-weight:800; letter-spacing:-0.5px; line-height: 1.2;">{name}</h3>
                   <p style="color:#cbd5e1; margin:0; font-size:1rem; font-weight:600;">Section: <span style="color:#38bdf8;">{section}</span></p>
               </div>
               <span class="badge" style="background: rgba(249, 115, 22, 0.15); color: #f97316; padding: 6px 14px; border-radius: 8px; font-size: 0.85rem; font-weight: 700; box-shadow: 0 2px 6px rgba(249, 115, 22, 0.15); border: 1px solid rgba(249, 115, 22, 0.3);">{code}</span>
           </div>
    """
    if stats:
       html += """
       <div style="display: flex; gap: 14px; margin-top: 24px; flex-wrap: wrap;">
       """
       for icon, label, value in stats:
            html += f"""
            <div style="background: rgba(30, 41, 59, 0.6); padding: 14px 18px; border-radius: 14px; display: flex; align-items: center; gap: 12px; border: 1px solid rgba(255, 255, 255, 0.05); transition: transform 0.2s ease, box-shadow 0.2s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 20px -4px rgba(0,0,0,0.5), 0 0 10px rgba(56,189,248,0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                <div style="background: rgba(15, 23, 42, 0.8); width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 1px 2px rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.05);">
                    <span style="font-size: 1.4rem;">{icon}</span>
                </div>
                <div style="display: flex; flex-direction: column;">
                    <span style="font-size: 0.75rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">{label}</span>
                    <span style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; line-height: 1.2;">{value}</span>
                </div>
            </div>
            """
       html += "</div>"

    html += "</div>"
    st.markdown(html.replace('\n', ''), unsafe_allow_html=True)
    if footer_callback:
        footer_callback()
