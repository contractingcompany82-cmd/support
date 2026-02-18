import streamlit as st
from twilio.rest import Client
from datetime import datetime
import os
from datetime import timezone, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Azaz AlBena Support | ازاز البناء",
    page_icon="🏗️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR SAUDI/ARABIC STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;700&display=swap');
    
    .main {
        direction: rtl;
        text-align: right;
    }
    
    .arabic-text {
        font-family: 'Noto Naskh Arabic', serif;
        direction: rtl;
        text-align: right;
    }
    
    .bilingual-label {
        display: flex;
        justify-content: space-between;
        direction: ltr;
    }
    
    .english-text {
        color: #2c3e50;
        font-weight: 600;
    }
    
    .arabic-text-inline {
        color: #1e88e5;
        font-weight: 600;
        font-family: 'Noto Naskh Arabic', serif;
    }
    
    .stButton>button {
        background-color: #1e88e5;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 24px;
        width: 100%;
        font-size: 16px;
    }
    
    .stButton>button:hover {
        background-color: #1565c0;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        border-right: 5px solid #28a745;
        direction: rtl;
        text-align: right;
    }
    
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 8px;
        border-right: 5px solid #dc3545;
        direction: rtl;
        text-align: right;
    }
    
    .header-container {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        margin-bottom: 30px;
        color: white;
    }
    
    .logo-text {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .logo-subtext {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .form-container {
        background-color: #f8f9fa;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Saudi Flag Colors Accent */
    .saudi-accent {
        border-top: 4px solid #006C35;
        border-bottom: 4px solid #006C35;
    }
    </style>
""", unsafe_allow_html=True)

# --- SAUDI ARABIA TIMEZONE ---
def get_saudi_time():
    """Get current time in Saudi Arabia (UTC+3)"""
    saudi_tz = timezone(timedelta(hours=3))
    return datetime.now(saudi_tz)

# --- WHATSAPP LOGIC ---
def send_whatsapp_notification(name, mobile, category, description):
    try:
        account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
        auth_token = st.secrets["TWILIO_AUTH_TOKEN"]
        from_whatsapp = st.secrets["TWILIO_WHATSAPP_FROM"]
        to_whatsapp = st.secrets["MY_WHATSAPP_NUMBER"]

        client = Client(account_sid, auth_token)
        timestamp = get_saudi_time().strftime("%Y-%m-%d %H:%M:%S")
        
        # Bilingual message
        message_body = (
            f"🏗️ *Azaz AlBena Ready Mix* | *ازاز البناء للخرسانة الجاهزة*\n"
            f"New Support Ticket | تذكرة دعم جديدة\n\n"
            f"*Name | الاسم:* {name}\n"
            f"*Mobile | الجوال:* {mobile}\n"
            f"*Type | النوع:* {category}\n"
            f"*Description | الوصف:* {description}\n\n"
            f"*Time | الوقت:* {timestamp} (Saudi Arabia | السعودية)"
        )

        client.messages.create(body=message_body, from_=from_whatsapp, to=to_whatsapp)
        return True, "Success"
    except Exception as e:
        return False, str(e)

# --- LOGO SECTION ---
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Try to load logo, fallback to styled text
    if os.path.exists("logo_azaz.jpg"):
        st.image("logo_azaz.jpg", use_column_width=True)
    else:
        # Styled text logo with Saudi colors
        st.markdown("""
            <div class="header-container saudi-accent">
                <div class="logo-text">🏗️ Azaz AlBena</div>
                <div class="logo-subtext">ازاز البناء للخرسانة الجاهزة</div>
                <div style="font-size: 0.9rem; margin-top: 10px; opacity: 0.8;">
                    Ready Mix Concrete | مورد خرسانة جاهزة
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- MAIN HEADING ---
st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h2 style="color: #2c3e50; margin-bottom: 10px;">
            <span class="english-text">Support System</span> | 
            <span class="arabic-text-inline">نظام الدعم</span>
        </h2>
        <p style="color: #666; font-size: 1.1rem;">
            Please fill out the form below | يرجى ملء النموذج أدناه
        </p>
    </div>
""", unsafe_allow_html=True)

# --- FORM SECTION ---
with st.container():
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    with st.form("support_form", clear_on_submit=True):
        
        # Full Name - Bilingual
        st.markdown("""
            <div class="bilingual-label">
                <span class="english-text">Full Name</span>
                <span class="arabic-text-inline">الاسم الكامل *</span>
            </div>
        """, unsafe_allow_html=True)
        name = st.text_input("", key="name", placeholder="Mohammed Ahmed | محمد أحمد")
        
        # Mobile Number - Saudi Format
        st.markdown("""
            <div class="bilingual-label">
                <span class="english-text">Mobile Number</span>
                <span class="arabic-text-inline">رقم الجوال *</span>
            </div>
        """, unsafe_allow_html=True)
        mobile = st.text_input("", key="mobile", placeholder="05xxxxxxxx | مثال: 0551234567")
        
        # Category - Bilingual options
        st.markdown("""
            <div class="bilingual-label">
                <span class="english-text">Request Type</span>
                <span class="arabic-text-inline">نوع الطلب *</span>
            </div>
        """, unsafe_allow_html=True)
        
        category_options = {
            "Support | دعم فني": "Support",
            "Complaint | شكوى": "Complaint", 
            "Query | استفسار": "Query",
            "Order Request | طلب توريد": "Order",
            "Other | أخرى": "Other"
        }
        
        category_display = st.selectbox("", options=list(category_options.keys()))
        category = category_options[category_display]
        
        # Description
        st.markdown("""
            <div class="bilingual-label">
                <span class="english-text">Description</span>
                <span class="arabic-text-inline">الوصف بالتفصيل *</span>
            </div>
        """, unsafe_allow_html=True)
        description = st.text_area("", key="desc", height=120, 
                                   placeholder="Describe your issue here... | اصف مشكلتك هنا...")
        
        # Submit Button - Bilingual
        submit_button = st.form_submit_button("🚀 Submit | إرسال الطلب")
        
        if submit_button:
            # Validation
            if not name or not mobile or not description:
                st.markdown("""
                    <div class="error-message">
                        ⚠️ Please fill all required fields | يرجى ملء جميع الحقول المطلوبة
                    </div>
                """, unsafe_allow_html=True)
            elif not mobile.startswith('05') or len(mobile) != 10:
                st.markdown("""
                    <div class="error-message">
                        ⚠️ Please enter valid Saudi mobile number (05xxxxxxxx) | 
                        يرجى إدخال رقم جوال سعودي صحيح
                    </div>
                """, unsafe_allow_html=True)
            else:
                with st.spinner("Sending... | جاري الإرسال..."):
                    success, result = send_whatsapp_notification(name, mobile, category, description)
                    if success:
                        st.markdown("""
                            <div class="success-message">
                                ✅ <strong>Submitted Successfully!</strong> | <strong>تم الإرسال بنجاح!</strong><br>
                                We will contact you soon | سنتواصل معك قريباً
                            </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                    else:
                        st.error(f"Error | خطأ: {result}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px; direction: rtl;">
        <p>
            <strong>Azaz AlBena Ready Mix</strong> | 
            <strong>ازاز البناء للخرسانة الجاهزة</strong>
        </p>
        <p style="font-size: 0.9rem;">
            📍 Saudi Arabia | المملكة العربية السعودية<br>
            © 2026 All Rights Reserved | جميع الحقوق محفوظة
        </p>
    </div>
""", unsafe_allow_html=True)
