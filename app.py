import streamlit as st
from twilio.rest import Client
from datetime import datetime

# --- CONFIGURATION & WHATSAPP LOGIC ---
def send_whatsapp_notification(name, mobile, category, description):
    # SAHI TARIKA: Yahan hum "Variable Names" use kar rahe hain, direct keys nahi.
    # Ye values aapke Streamlit Cloud ke 'Secrets' section se uthayi jayengi.
    try:
        account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
        auth_token = st.secrets["TWILIO_AUTH_TOKEN"]
        from_whatsapp = st.secrets["TWILIO_WHATSAPP_FROM"]
        to_whatsapp = st.secrets["MY_WHATSAPP_NUMBER"]

        client = Client(account_sid, auth_token)
        
        # Format the message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_body = (
            f"🚨 *New Support Ticket*\n\n"
            f"*Name:* {name}\n"
            f"*Mobile:* {mobile}\n"
            f"*Type:* {category}\n"
            f"*Description:* {description}\n\n"
            f"*Time:* {timestamp}"
        )

        message = client.messages.create(
            body=message_body,
            from_=from_whatsapp,
            to=to_whatsapp
        )
        return True, message.sid
    except Exception as e:
        return False, str(e)

# --- STREAMLIT UI ---
st.set_page_config(page_title="Support Portal", page_icon="🎫")

st.title("📩 Support & Complaint System")
st.markdown("Please fill out the form below. We will receive your request instantly via WhatsApp.")

with st.form("complaint_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name*")
    with col2:
        mobile = st.text_input("Mobile Number*")
        
    category = st.selectbox(
        "Complaint Type*",
        ["Support", "Complaint", "Query", "Other"]
    )
    
    description = st.text_area("Detailed Description*", help="Provide as much detail as possible.")
    
    submit_button = st.form_submit_button("Submit Ticket")

    if submit_button:
        if not name or not mobile or not description:
            st.error("Please fill in all required fields.")
        else:
            with st.spinner("Processing..."):
                success, result = send_whatsapp_notification(name, mobile, category, description)
                
                if success:
                    st.success(f"Ticket submitted successfully!")
                    st.balloons()
                else:
                    # Agar error aata hai toh yahan dikhayega
                    st.error(f"Error: {result}")
