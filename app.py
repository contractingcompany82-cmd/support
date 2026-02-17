
import streamlit as st
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="WhatsApp Support System",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #25D366, #128C7E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #dcf8c6;
        margin-left: 20%;
        border-bottom-right-radius: 0.2rem;
    }
    .admin-message {
        background-color: #ffffff;
        margin-right: 20%;
        border: 1px solid #e0e0e0;
        border-bottom-left-radius: 0.2rem;
    }
    .timestamp {
        font-size: 0.7rem;
        color: #666;
        margin-top: 0.2rem;
    }
    .status-online {
        color: #25D366;
        font-weight: bold;
    }
    .ticket-card {
        background: #f0f2f5;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #25D366;
        cursor: pointer;
        transition: all 0.3s;
    }
    .ticket-card:hover {
        transform: translateX(5px);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .unread {
        border-left-color: #ff3366;
        background: #fff5f5;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'tickets' not in st.session_state:
    st.session_state.tickets = {}
if 'current_ticket' not in st.session_state:
    st.session_state.current_ticket = None
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

# ==================== WHATSAPP API FUNCTIONS ====================

def send_whatsapp_callmebot(phone_number, message, api_key):
    """
    Free WhatsApp API using CallMeBot
    Get API Key: Message "I allow callmebot to send me messages" to +34 644 52 53 02
    """
    try:
        url = f"https://api.callmebot.com/whatsapp.php"
        params = {
            'phone': phone_number,
            'text': message,
            'apikey': api_key
        }
        response = requests.get(url, params=params, timeout=10)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error sending WhatsApp: {e}")
        return False

def send_whatsapp_ultramsg(phone_number, message,
