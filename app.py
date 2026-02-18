import streamlit as st
from twilio.rest import Client
from datetime import datetime
import os

# --- CONFIGURATION & WHATSAPP LOGIC ---
def send_whatsapp_notification(name, mobile, category, description):
    try:
        # Fetching secrets
        account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
        auth_token = st.secrets["TWILIO_AUTH_TOKEN"]
        from_whatsapp = st.secrets["TWILIO_WHATSAPP_FROM"]
        to_whatsapp = st.secrets["MY_WHATSAPP_NUMBER"]

        client = Client(account_sid, auth_token)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Professional WhatsApp Message Body
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

        message = client.messages.create(
            body=message_body,
            from_=from_whatsapp,
            to=to_whatsapp
        )
        return True, message.sid
    except Exception as e:
        return False, str(e)

# --- STREAMLIT UI (ARABIC & AZAZ BRANDING) ---
st.set_page_config(page_title="عزاز البناء - نظام الدعم", page_icon="🏗️")

# RTL CSS and Custom Saudi Red/Black Theme from Logo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }
    
    .stApp {
        background-color: #ffffff;
    }

    /* Main Container */
    .block-container {
        padding-top: 2rem;
    }

    /* Input Fields Styling */
    input, textarea, select {
        direction: RTL !important;
        text-align: right !important;
        border: 1px solid #e0e0e0 !important;
    }

    /* Submit Button Styling (Red like the logo) */
    .stButton > button {
        background-color: #e31e24; /* Red from logo */
        color: white;
        font-weight: bold;
        width: 100%;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    .stButton > button:hover {
        background-color: #b31419;
        color: white;
    }

    h1 {
        color: #000000;
        border-bottom: 2px solid #e31e24;
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section with Logo ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Make sure logo_azaz.jpg is in your GitHub main folder
    if os.path.exists("logo_azaz.jpg"):
        st.image("logo_azaz.jpg", use_container_width=True)
    else:
        # Fallback if image not found
        st.subheader("مصنع عزاز البناء للخرسانة الجاهزة")

st.markdown("<h1 style='text-align: center;'>نظام الشكاوى والدعم الفني</h1>", unsafe_allow_html=True)
st.write("")

# --- Form Section ---
with st.form("azaz_support_form", clear_on_submit=True):
    name = st.text_input("الاسم الكامل*", placeholder="أدخل اسمك هنا")
    mobile = st.text_input("رقم الجوال*", placeholder="05xxxxxxxx")
    
    category = st.selectbox(
        "نوع الطلب*",
        ["دعم فني", "شكوى على جودة الخرسانة", "استفسار عن طلبية", "أخرى"]
    )
    
    description = st.text_area("تفاصيل المشكلة*", placeholder="يرجى كتابة التفاصيل هنا...")
    
    submit_button = st.form_submit_button("إرسال الآن عبر واتساب")

    if submit_button:
        if not name or not mobile or not description:
            st.error("⚠️ يرجى تعبئة جميع الحقول المطلوبة.")
        elif not (len(mobile) >= 9):
            st.warning("⚠️ رقم الجوال غير صحيح.")
        else:
            with st.spinner("جاري معالجة طلبك..."):
                success, result = send_whatsapp_notification(name, mobile, category, description)
                
                if success:
                    st.success(f"✅ تم استلام طلبك يا {name}. سيقوم فريق عزاز البناء بالتواصل معك قريباً.")
                    st.balloons()
                else:
                    st.error(f"❌ حدث خطأ: {result}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>حقوق الطبع والنشر © 2026 مصنع عزاز البناء للخرسانة الجاهزة</p>", unsafe_allow_html=True)
