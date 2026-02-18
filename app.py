import streamlit as st
from twilio.rest import Client
from datetime import datetime, timezone, timedelta
import os
import requests
from io import BytesIO

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Azaz AlBena Support | ازاز البناء",
    page_icon="🏗️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    .main { direction: rtl; text-align: right; }
    .arabic-text { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .bilingual-label { display: flex; justify-content: space-between; direction: ltr; }
    .english-text { color: #2c3e50; font-weight: 600; }
    .arabic-text-inline { color: #c41e3a; font-weight: 700; font-family: 'Tajawal', sans-serif; }
    .stButton>button {
        background: linear-gradient(135deg, #c41e3a 0%, #8b0000 100%);
        color: white; font-weight: bold; border-radius: 8px; padding: 12px 24px;
        width: 100%; font-size: 16px; border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #8b0000 0%, #c41e3a 100%);
        transform: translateY(-2px);
    }
    .success-message {
        background-color: #d4edda; color: #155724; padding: 15px;
        border-radius: 8px; border-right: 5px solid #28a745;
        direction: rtl; text-align: right; font-family: 'Tajawal', sans-serif;
    }
    .error-message {
        background-color: #f8d7da; color: #721c24; padding: 15px;
        border-radius: 8px; border-right: 5px solid #dc3545;
        direction: rtl; text-align: right; font-family: 'Tajawal', sans-serif;
    }
    .logo-container { text-align: center; padding: 20px; background: white; 
                     border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .form-container {
        background-color: #f8f9fa; padding: 30px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 4px solid #c41e3a;
    }
    .header-title {
        text-align: center; margin-bottom: 30px; padding: 20px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 12px;
    }
    .debug-box {
        background-color: #fff3cd; border: 1px solid #ffeaa7; 
        padding: 10px; border-radius: 5px; margin: 10px 0; font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- CHECK SECRETS ---
def check_secrets():
    """Check if all required secrets are present"""
    required_secrets = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_WHATSAPP_FROM', 'MY_WHATSAPP_NUMBER']
    missing = []
    
    for secret in required_secrets:
        if secret not in st.secrets:
            missing.append(secret)
    
    return missing

# --- SAUDI TIME ---
def get_saudi_time():
    saudi_tz = timezone(timedelta(hours=3))
    return datetime.now(saudi_tz)

# --- LOGO DISPLAY ---
def display_logo():
    try:
        github_url = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/logo%20azaz.jpg"
        response = requests.get(github_url, timeout=5)
        if response.status_code == 200:
            logo_image = BytesIO(response.content)
            st.image(logo_image, use_column_width=True)
            return True
    except:
        pass
    
    for logo_file in ["logo azaz.jpg", "logo_azaz.jpg", "logo.jpg"]:
        if os.path.exists(logo_file):
            st.image(logo_file, use_column_width=True)
            return True
    return False

# --- WHATSAPP LOGIC WITH ERROR HANDLING ---
def send_whatsapp_notification(name, mobile, category, description):
    try:
        # Check secrets first
        missing_secrets = check_secrets()
        if missing_secrets:
            return False, f"Missing secrets: {', '.join(missing_secrets)}"
        
        account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
        auth_token = st.secrets["TWILIO_AUTH_TOKEN"]
        from_whatsapp = st.secrets["TWILIO_WHATSAPP_FROM"]
        to_whatsapp = st.secrets["MY_WHATSAPP_NUMBER"]
        
        # Validate credentials format
        if not account_sid.startswith('AC'):
            return False, "Invalid Account SID format (should start with 'AC')"
        
        if len(auth_token) != 32:
            return False, "Invalid Auth Token length (should be 32 characters)"
        
        client = Client(account_sid, auth_token)
        timestamp = get_saudi_time().strftime("%Y-%m-%d %H:%M:%S")
        
        message_body = (
            f"🏗️ *Azaz AlBena Ready Mix* | *مصنع عزاز البناء*\n"
            f"New Support Ticket | تذكرة دعم جديدة\n\n"
            f"*Name | الاسم:* {name}\n"
            f"*Mobile | الجوال:* {mobile}\n"
            f"*Type | النوع:* {category}\n"
            f"*Description | الوصف:* {description}\n\n"
            f"*Time | الوقت:* {timestamp} 🇸🇦"
        )
        
        message = client.messages.create(
            body=message_body, 
            from_=from_whatsapp, 
            to=to_whatsapp
        )
        
        return True, message.sid
        
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg:
            return False, "Authentication failed. Please check your Twilio Account SID and Auth Token."
        elif "404" in error_msg:
            return False, "WhatsApp number not found. Please check the 'from' and 'to' numbers."
        else:
            return False, error_msg

# --- LOGO SECTION ---
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    if not display_logo():
        st.markdown("""
            <div style="text-align: center; color: #c41e3a;">
                <h1 style="font-size: 3rem; margin: 0;">🏗️ Azaz AlBena</h1>
                <h2 style="font-size: 1.5rem; color: #333;">مصنع عزاز البناء</h2>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- DEBUG INFO (Remove in production) ---
if st.checkbox("Show Debug Info | عرض معلومات التصحيح"):
    missing = check_secrets()
    if missing:
        st.error(f"Missing Secrets | الأسرار المفقودة: {missing}")
    else:
        st.success("All secrets present | جميع الأسرار موجودة")
        st.write(f"Account SID: {st.secrets['TWILIO_ACCOUNT_SID'][:6]}...")

# --- MAIN HEADING ---
st.markdown("""
    <div class="header-title">
        <h2 style="color: #c41e3a; font-family: 'Tajawal', sans-serif;">
            <span class="english-text">Customer Support System</span> | 
            <span class="arabic-text-inline">نظام دعم العملاء</span>
        </h2>
    </div>
""", unsafe_allow_html=True)

# --- FORM ---
with st.container():
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    with st.form("support_form", clear_on_submit=True):
        st.markdown("""<div class="bilingual-label">
            <span class="english-text">Full Name *</span>
            <span class="arabic-text-inline">الاسم الكامل *</span>
        </div>""", unsafe_allow_html=True)
        name = st.text_input("", key="name", placeholder="Mohammed Ahmed | محمد أحمد")
        
        st.markdown("""<div class="bilingual-label">
            <span class="english-text">Mobile Number *</span>
            <span class="arabic-text-inline">رقم الجوال *</span>
        </div>""", unsafe_allow_html=True)
        mobile = st.text_input("", key="mobile", placeholder="05xxxxxxxx")
        
        st.markdown("""<div class="bilingual-label">
            <span class="english-text">Request Type *</span>
            <span class="arabic-text-inline">نوع الطلب *</span>
        </div>""", unsafe_allow_html=True)
        
        category_options = {
            "Technical Support | دعم فني": "Support",
            "Complaint | شكوى": "Complaint", 
            "Inquiry | استفسار": "Query",
            "Order Request | طلب توريد": "Order",
            "Other | أخرى": "Other"
        }
        category_display = st.selectbox("", options=list(category_options.keys()))
        category = category_options[category_display]
        
        st.markdown("""<div class="bilingual-label">
            <span class="english-text">Description *</span>
            <span class="arabic-text-inline">الوصف بالتفصيل *</span>
        </div>""", unsafe_allow_html=True)
        description = st.text_area("", key="desc", height=120)
        
        submit_button = st.form_submit_button("🚀 Submit | إرسال")
        
        if submit_button:
            if not name or not mobile or not description:
                st.markdown("""<div class="error-message">
                    ⚠️ Please fill all fields | يرجى ملء جميع الحقول
                </div>""", unsafe_allow_html=True)
            elif not mobile.startswith('05') or len(mobile) != 10:
                st.markdown("""<div class="error-message">
                    ⚠️ Invalid Saudi mobile number | رقم جوال سعودي غير صحيح
                </div>""", unsafe_allow_html=True)
            else:
                with st.spinner("Sending... | جاري الإرسال..."):
                    success, result = send_whatsapp_notification(name, mobile, category, description)
                    if success:
                        st.markdown(f"""<div class="success-message">
                            ✅ Success | تم بنجاح<br>
                            Ticket ID: {result}
                        </div>""", unsafe_allow_html=True)
                        st.balloons()
                    else:
                        st.markdown(f"""<div class="error-message">
                            ❌ Error | خطأ<br>{result}
                        </div>""", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px; font-family: 'Tajawal', sans-serif;">
        <p style="color: #c41e3a; font-weight: bold;">
            🏗️ Azaz AlBena Ready Mix | مصنع عزاز البناء للخرسانة الجاهزة
        </p>
        <p>📍 Saudi Arabia | المملكة العربية السعودية<br>© 2026</p>
    </div>
""", unsafe_allow_html=True)
