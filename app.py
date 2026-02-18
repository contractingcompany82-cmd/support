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

# --- CUSTOM CSS FOR SAUDI/ARABIC STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;700&family=Tajawal:wght@400;700&display=swap');
    
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
        color: #c41e3a;
        font-weight: 700;
        font-family: 'Tajawal', sans-serif;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #c41e3a 0%, #8b0000 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 24px;
        width: 100%;
        font-size: 16px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #8b0000 0%, #c41e3a 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        border-right: 5px solid #28a745;
        direction: rtl;
        text-align: right;
        font-family: 'Tajawal', sans-serif;
    }
    
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 8px;
        border-right: 5px solid #dc3545;
        direction: rtl;
        text-align: right;
        font-family: 'Tajawal', sans-serif;
    }
    
    .logo-container {
        text-align: center;
        padding: 20px;
        background: white;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .form-container {
        background-color: #f8f9fa;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-top: 4px solid #c41e3a;
    }
    
    .header-title {
        text-align: center;
        margin-bottom: 30px;
        padding: 20px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SAUDI ARABIA TIMEZONE ---
def get_saudi_time():
    """Get current time in Saudi Arabia (UTC+3)"""
    saudi_tz = timezone(timedelta(hours=3))
    return datetime.now(saudi_tz)

# --- LOGO DISPLAY FUNCTION ---
def display_logo():
    """Display logo from GitHub or local file"""
    try:
        # Try GitHub raw URL first (replace with your actual GitHub raw URL)
        # Example: https://raw.githubusercontent.com/username/repo/main/logo%20azaz.jpg
        github_url = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/logo%20azaz.jpg"
        
        response = requests.get(github_url, timeout=5)
        if response.status_code == 200:
            logo_image = BytesIO(response.content)
            st.image(logo_image, use_column_width=True)
            return True
    except:
        pass
    
    # Fallback to local file
    if os.path.exists("logo azaz.jpg"):
        st.image("logo azaz.jpg", use_column_width=True)
        return True
    elif os.path.exists("logo_azaz.jpg"):
        st.image("logo_azaz.jpg", use_column_width=True)
        return True
    
    return False

# --- WHATSAPP LOGIC ---
def send_whatsapp_notification(name, mobile, category, description):
    try:
        account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
        auth_token = st.secrets["TWILIO_AUTH_TOKEN"]
        from_whatsapp = st.secrets["TWILIO_WHATSAPP_FROM"]
        to_whatsapp = st.secrets["MY_WHATSAPP_NUMBER"]

        client = Client(account_sid, auth_token)
        timestamp = get_saudi_time().strftime("%Y-%m-%d %H:%M:%S")
        
        # Bilingual message with logo reference
        message_body = (
            f"🏗️ *Azaz AlBena Ready Mix* | *مصنع عزاز البناء*\n"
            f"New Support Ticket | تذكرة دعم جديدة\n\n"
            f"*Name | الاسم:* {name}\n"
            f"*Mobile | الجوال:* {mobile}\n"
            f"*Type | النوع:* {category}\n"
            f"*Description | الوصف:* {description}\n\n"
            f"*Time | الوقت:* {timestamp} 🇸🇦"
        )

        client.messages.create(body=message_body, from_=from_whatsapp, to=to_whatsapp)
        return True, "Success"
    except Exception as e:
        return False, str(e)

# --- LOGO SECTION ---
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    
    # Display logo
    logo_displayed = display_logo()
    
    if not logo_displayed:
        # Fallback text logo with company colors (red from logo)
        st.markdown("""
            <div style="text-align: center; color: #c41e3a;">
                <h1 style="font-size: 3rem; margin: 0; font-weight: bold;">🏗️ Azaz AlBena</h1>
                <h2 style="font-size: 1.5rem; margin: 5px 0; color: #333;">مصنع عزاز البناء</h2>
                <p style="color: #666; font-size: 1rem;">للخرسانة الجاهزة | Ready Mix Concrete</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN HEADING ---
st.markdown("""
    <div class="header-title">
        <h2 style="color: #c41e3a; margin-bottom: 10px; font-family: 'Tajawal', sans-serif;">
            <span class="english-text">Customer Support System</span> | 
            <span class="arabic-text-inline">نظام دعم العملاء</span>
        </h2>
        <p style="color: #555; font-size: 1.1rem; font-family: 'Tajawal', sans-serif;">
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
                <span class="english-text">Full Name *</span>
                <span class="arabic-text-inline">الاسم الكامل *</span>
            </div>
        """, unsafe_allow_html=True)
        name = st.text_input("", key="name", placeholder="Mohammed Ahmed | محمد أحمد")
        
        # Mobile Number - Saudi Format
        st.markdown("""
            <div class="bilingual-label">
                <span class="english-text">Mobile Number *</span>
                <span class="arabic-text-inline">رقم الجوال *</span>
            </div>
        """, unsafe_allow_html=True)
        mobile = st.text_input("", key="mobile", placeholder="05xxxxxxxx | مثال: 0551234567")
        
        # Category - Bilingual options
        st.markdown("""
            <div class="bilingual-label">
                <span class="english-text">Request Type *</span>
                <span class="arabic-text-inline">نوع الطلب *</span>
            </div>
        """, unsafe_allow_html=True)
        
        category_options = {
            "Technical Support | دعم فني": "Support",
            "Complaint | شكوى": "Complaint", 
            "Inquiry | استفسار": "Query",
            "Order Request | طلب توريد": "Order",
            "Other | أخرى": "Other"
        }
        
        category_display = st.selectbox("", options=list(category_options.keys()))
        category = category_options[category_display]
        
        # Description
        st.markdown("""
            <div class="bilingual-label">
                <span class="english-text">Description *</span>
                <span class="arabic-text-inline">الوصف بالتفصيل *</span>
            </div>
        """, unsafe_allow_html=True)
        description = st.text_area("", key="desc", height=120, 
                                   placeholder="Describe your issue here... | اصف مشكلتك هنا بالتفصيل...")
        
        # Submit Button - Bilingual
        submit_button = st.form_submit_button("🚀 Submit Request | إرسال الطلب")
        
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
                        يرجى إدخال رقم جوال سعودي صحيح (مثال: 0551234567)
                    </div>
                """, unsafe_allow_html=True)
            else:
                with st.spinner("Sending... | جاري الإرسال..."):
                    success, result = send_whatsapp_notification(name, mobile, category, description)
                    if success:
                        st.markdown("""
                            <div class="success-message">
                                ✅ <strong>Submitted Successfully!</strong> | <strong>تم الإرسال بنجاح!</strong><br>
                                We will contact you soon on your mobile | سنتواصل معك قريباً على جوالك
                            </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                    else:
                        st.error(f"Error | خطأ: {result}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px; direction: rtl; font-family: 'Tajawal', sans-serif;">
        <p style="font-size: 1.1rem; color: #c41e3a; font-weight: bold;">
            🏗️ Azaz AlBena Ready Mix | مصنع عزاز البناء للخرسانة الجاهزة
        </p>
        <p style="font-size: 0.9rem; color: #555;">
            📍 Kingdom of Saudi Arabia | المملكة العربية السعودية<br>
            📞 Customer Service | خدمة العملاء: 9200XXXXX<br>
            © 2026 All Rights Reserved | جميع الحقوق محفوظة
        </p>
    </div>
""", unsafe_allow_html=True)
