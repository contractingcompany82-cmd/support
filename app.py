import streamlit as st
from twilio.rest import Client
from datetime import datetime
import os

# --- CONFIGURATION & WHATSAPP LOGIC ---
def send_whatsapp_notification(name, mobile, category, description):
    try:
        account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
        auth_token = st.secrets["TWILIO_AUTH_TOKEN"]
        from_whatsapp = st.secrets["TWILIO_WHATSAPP_FROM"]
        to_whatsapp = st.secrets["MY_WHATSAPP_NUMBER"]

        client = Client(account_sid, auth_token)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message_body = (
            f"🏗️ *مصنع عزاز البناء للخرسانة الجاهزة*\n"
            f"----------------------------------\n"
            f"🔔 *إشعار تذكرة دعم جديدة*\n\n"
            f"*👤 العميل:* {name}\n"
            f"*📞 الجوال:* {mobile}\n"
            f"*📂 النوع:* {category}\n"
            f"*📝 الوصف:* {description}\n\n"
            f"🗓️ *التاريخ:* {timestamp}\n"
            f"----------------------------------"
        )

        message = client.messages.create(body=message_body, from_=from_whatsapp, to=to_whatsapp)
        return True, message.sid
    except Exception as e:
        return False, str(e)

# --- STREAMLIT UI ---
st.set_page_config(page_title="عزاز البناء - نظام الدعم", page_icon="🏗️", layout="centered")

# Solid CSS for RTL and UI Fix
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    .main, .stApp {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }
    .block-container {
        padding-top: 2rem !important;
        background-color: #f9f9f9;
        border-radius: 15px;
    }
    h1, h2, h3 {
        color: #e31e24 !important;
        text-align: center !important;
    }
    input, textarea, select {
        text-align: right !important;
        direction: RTL !important;
    }
    div.stButton > button {
        background-color: #e31e24 !important;
        color: white !important;
        border-radius: 10px !important;
        height: 3em !important;
        width: 100% !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }
    .stMarkdown p, label {
        text-align: right !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Logo Display ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("logo_azaz.jpg"):
        st.image("logo_azaz.jpg", use_container_width=True)
    else:
        st.markdown("### مصنع عزاز البناء")

st.markdown("<h1 style='text-align: center;'>نظام تقديم البلاغات والشكاوى</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>يرجى تعبئة البيانات التالية وسنقوم بالتواصل معكم فوراً</p>", unsafe_allow_html=True)

# --- Form ---
with st.form("support_form", clear_on_submit=True):
    name = st.text_input("اسم العميل أو الشركة*")
    mobile = st.text_input("رقم الجوال السعودي*")
    
    category = st.selectbox(
        "نوع البلاغ*",
        ["شكوى جودة خرسانة", "تأخير توريد", "طلب دعم فني", "استفسار مالي", "أخرى"]
    )
    
    description = st.text_area("تفاصيل البلاغ*", height=150)
    
    submit = st.form_submit_button("إرسال البلاغ الآن")

    if submit:
        if not name or not mobile or not description:
            st.error("⚠️ يرجى تعبئة جميع الخانات المطلوبة")
        else:
            with st.spinner("جاري إرسال البيانات..."):
                success, msg = send_whatsapp_notification(name, mobile, category, description)
                if success:
                    st.success("✅ تم الإرسال بنجاح! شكراً لتعاونكم مع عزاز البناء.")
                    st.balloons()
                else:
                    st.error(f"❌ حدث خطأ في النظام: {msg}")

st.markdown("---")
# Fixed potential syntax error line below
st.markdown("<p style='text-align: center; font-size: 0.8rem;'>نظام آلي مخصص لمصنع عزاز البناء - 2026</p>", unsafe_allow_html=True)
