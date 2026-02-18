import streamlit as st
from twilio.rest import Client
from datetime import datetime

# --- CONFIGURATION & WHATSAPP LOGIC ---
def send_whatsapp_notification(name, mobile, category, description):
    # Fetch credentials from Streamlit Secrets
    account_sid = st.secrets["ACed69b33546757121abd0fe5d9f9455b5"]
    auth_token = st.secrets["854aac2c8b57dbf945babd600c885bf8"]
    from_whatsapp = st.secrets["whatsapp:+14155238886"]  # e.g., 'whatsapp:+14155238886'
    to_whatsapp = st.secrets["whatsapp:+966544221519"]      # e.g., 'whatsapp:+911234567890'

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

    try:
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
        # --- VALIDATION ---
        if not name or not mobile or not description:
            st.error("Please fill in all required fields.")
        elif len(mobile) < 10:
            st.error("Please enter a valid mobile number.")
        else:
            with st.spinner("Sending ticket to support team..."):
                success, result = send_whatsapp_notification(name, mobile, category, description)
                
                if success:
                    st.success(f"Thank you, {name}! Your ticket has been submitted and sent to our team.")
                    st.balloons()
                else:
                    st.error(f"Error sending WhatsApp notification: {result}")
