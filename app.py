import streamlit as st
from twilio.rest import Client
from datetime import datetime

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
            f"🚨 *طلب دعم جديد من عزاز البنا للخرسانة الجاهزة*\n\n"
            f"*الاسم:* {name}\n"
            f"*الجوال:* {mobile}\n"
            f"*النوع:* {category}\n"
            f"*الوصف:* {description}\n\n"
            f"*الوقت:* {timestamp}"
        )

        message = client.messages.create(
            body=message_body,
            from_=from_whatsapp,
            to=to_whatsapp
        )
        return True, message.sid
    except Exception as e:
        return False, str(e)

# --- STREAMLIT UI (ARABIC & RTL SUPPORT with Branding) ---
st.set_page_config(page_title="نظام الدعم الفني - عزاز البنا", page_icon="🏗️")

# Custom CSS for RTL, Saudi Green Theme, and Fonts
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Cairo', sans-serif;
    }
    
    .reportview-container .main .block-container {
        direction: RTL;
        text-align: right;
        max-width: 750px; # Adjust as needed
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    input, textarea, select, .stTextInput, .stTextArea, .stSelectbox {
        direction: RTL !important;
        text-align: right !important;
        border-color: #004F2D; /* Saudi Green border */
    }
    label {
        color: #004F2D; /* Saudi Green labels */
        text-align: right;
        width: 100%;
    }
    .stButton > button {
        background-color: #004F2D; /* Saudi Green button */
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        direction: RTL;
        text-align: center;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #006F3D; /* Darker Green on hover */
        color: #FFFFFF;
    }
    .stSuccess, .stError, .stWarning {
        direction: RTL;
        text-align: right;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #004F2D; /* Headings in Saudi Green */
        text-align: right;
    }
    .css-1faytmc { /* Streamlit header div for alignment */
        flex-direction: row-reverse;
        justify-content: flex-start;
    }
    .stMarkdown p {
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Branding and Company Name ---
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Flag_of_Saudi_Arabia.svg/1200px-Flag_of_Saudi_Arabia.svg.png", width=100) # Saudi Flag for theme
st.title("🌟 نظام الدعم والشكاوى لـ *عزاز البنا للخرسانة الجاهزة*")
st.markdown("---")
st.subheader("نتواجد لخدمتكم، يرجى ملء النموذج أدناه.")

with st.form("complaint_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("الاسم الكامل*")
    with col2:
        mobile = st.text_input("رقم الجوال* (مثال: 05xxxxxxx)", placeholder="05xxxxxxxx")
        
    category = st.selectbox(
        "نوع الطلب*",
        ["دعم فني (Support)", "شكوى (Complaint)", "استفسار (Query)", "أخرى (Other)"]
    )
    
    description = st.text_area("وصف المشكلة بالتفصيل*", help="يرجى تقديم أكبر قدر ممكن من التفاصيل لخدمتكم بشكل أفضل.")
    
    submit_button = st.form_submit_button("إرسال الطلب")

    if submit_button:
        if not name or not mobile or not description:
            st.error("❌ يرجى تعبئة جميع الحقول المطلوبة.")
        elif not (mobile.startswith(('05')) and len(mobile) == 10) and not (mobile.startswith(('+9665')) and len(mobile) == 13):
            st.warning("⚠️ يرجى التأكد من صحة رقم الجوال السعودي (مثال: 05xxxxxxx أو +9665xxxxxxx).")
        else:
            with st.spinner("⏳ جاري إرسال طلبكم، يرجى الانتظار..."):
                success, result = send_whatsapp_notification(name, mobile, category, description)
                
                if success:
                    st.success(f"✅ تم إرسال طلبكم بنجاح، {name} ! شكرًا لتواصلكم مع عزاز البنا.")
                    st.balloons()
                else:
                    st.error(f"🚫 خطأ في الإرسال: {result}. يرجى المحاولة لاحقاً أو التواصل معنا مباشرةً.")

st.markdown("---")
# Saudi Vision 2030 reference
st.caption("✨ متوافق مع رؤية المملكة 2030 - عزاز البنا للخرسانة الجاهزة ©")
