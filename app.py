import streamlit as st
from twilio.rest import Client
from datetime import datetime
import os

# --- WHATSAPP LOGIC ---
def send_whatsapp_notification(name, mobile, category, description):
    try:
        account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
        auth_token = st.secrets["TWILIO_AUTH_TOKEN"]
        from_whatsapp = st.secrets["TWILIO_WHATSAPP_FROM"]
        to_whatsapp = st.secrets["MY_WHATSAPP_NUMBER"]

        client = Client(account_sid, auth_token)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message_body = (
            f"🏗️ *Azaz AlBena Readymix*\n"
            f"New Support Ticket\n\n"
            f"*Name:* {name}\n"
            f"*Mobile:* {mobile}\n"
            f"*Type:* {category}\n"
            f"*Description:* {description}\n\n"
            f"*Time:* {timestamp}"
        )

        client.messages.create(body=message_body, from_=from_whatsapp, to=to_whatsapp)
        return True, "Success"
    except Exception as e:
        return False, str(e)

# --- SIMPLE & CLEAN UI (Like the First Version) ---
st.set_page_config(page_title="Azaz AlBena Support", page_icon="🏗️")

# 1. Logo Section (Simple Center)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("logo_azaz.jpg"):
        st.image("logo_azaz.jpg")
    else:
        st.write("### Azaz AlBena Ready Mix")

# 2. Main Heading
st.title("📩 Azaz AlBena Support System")
st.markdown("Please fill out the form below for any complaints or queries.")

# 3. Simple Form (Original Style)
with st.form("support_form", clear_on_submit=True):
    name = st.text_input("Full Name / الاسم الكامل*")
    mobile = st.text_input("Mobile Number / رقم الجوال*")
    
    category = st.selectbox(
        "Type / نوع الطلب*",
        ["Support", "Complaint", "Query", "Other"]
    )
    
    description = st.text_area("Description / الوصف بالتفصيل*")
    
    submit_button = st.form_submit_button("Submit / إرسال")

    if submit_button:
        if not name or not mobile or not description:
            st.error("Please fill all fields / يرجى تعبئة جميع الحقول")
        else:
            with st.spinner("Sending..."):
                success, result = send_whatsapp_notification(name, mobile, category, description)
                if success:
                    st.success("Submitted successfully! / تم الإرسال بنجاح")
                    st.balloons()
                else:
                    st.error(f"Error: {result}")

st.markdown("---")
st.caption("© 2026 Azaz AlBena Ready Mix")
