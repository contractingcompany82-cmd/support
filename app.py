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

def send_whatsapp_ultramsg(phone_number, message, instance_id, token):
    """
    UltraMsg API - 100 messages/day free
    Sign up: https://ultramsg.com
    """
    try:
        url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
        payload = {
            "token": token,
            "to": phone_number,
            "body": message,
            "priority": 1,
            "referenceId": ""
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, data=payload, headers=headers)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def format_whatsapp_message(ticket_data, message_type="new"):
    """Format message for WhatsApp"""
    if message_type == "new":
        return f"""🚨 *NEW SUPPORT TICKET*

👤 *Name:* {ticket_data['name']}
📱 *Phone:* {ticket_data['phone']}
📧 *Email:* {ticket_data.get('email', 'N/A')}
📋 *Issue:* {ticket_data['issue_type']}
📝 *Message:* {ticket_data['message']}
⏰ *Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Reply to chat: {ticket_data['phone']}"""
    
    elif message_type == "reply":
        return f"""💬 *New Message from {ticket_data['name']}*

📝 {ticket_data['last_message']}

_View full conversation in dashboard_"""

# ==================== UI COMPONENTS ====================

def init_database():
    """Initialize in-memory database (replace with Firebase/SQLite for production)"""
    if 'db' not in st.session_state:
        st.session_state.db = {}

def create_ticket(name, phone, email, issue_type, message):
    """Create new support ticket"""
    ticket_id = f"TKT{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    ticket_data = {
        'id': ticket_id,
        'name': name,
        'phone': phone,
        'email': email,
        'issue_type': issue_type,
        'message': message,
        'status': 'open',
        'created_at': datetime.now(),
        'messages': [
            {
                'sender': 'user',
                'text': message,
                'timestamp': datetime.now(),
                'read': False
            }
        ],
        'unread': True
    }
    
    st.session_state.tickets[ticket_id] = ticket_data
    
    # Send WhatsApp Notification
    admin_phone = os.getenv('ADMIN_WHATSAPP_NUMBER', '919876543210')
    api_key = os.getenv('CALLMEBOT_API_KEY', '')
    
    whatsapp_msg = format_whatsapp_message(ticket_data, "new")
    
    # Try CallMeBot first (free)
    if api_key:
        success = send_whatsapp_callmebot(admin_phone, whatsapp_msg, api_key)
        if success:
            st.success("✅ Notification sent to admin via WhatsApp!")
        else:
            st.warning("⚠️ WhatsApp notification failed, but ticket created")
    else:
        st.info("ℹ️ WhatsApp API not configured. Ticket saved locally.")
        # Show manual WhatsApp link
        wa_link = f"https://wa.me/{admin_phone}?text={requests.utils.quote(whatsapp_msg)}"
        st.markdown(f"[📱 Click to send WhatsApp manually]({wa_link})")
    
    return ticket_id

def render_chat_interface():
    """Render chat interface for users"""
    st.markdown('<h1 class="main-header">💬 Live Support Chat</h1>', unsafe_allow_html=True)
    
    # Check if already has ticket
    if 'user_ticket' in st.session_state:
        show_active_chat(st.session_state.user_ticket)
        return
    
    # New Ticket Form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 1rem; margin-bottom: 2rem;">
            <h2>How can we help you today?</h2>
            <p>Fill in your details and we'll connect you with our support team instantly.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("support_form"):
            name = st.text_input("👤 Your Name", placeholder="John Doe")
            phone = st.text_input("📱 WhatsApp Number", placeholder="919876543210", 
                                help="Include country code without +")
            email = st.text_input("📧 Email (Optional)", placeholder="john@example.com")
            
            issue_type = st.selectbox(
                "📋 Issue Category",
                ["General Inquiry", "Technical Support", "Billing Issue", "Feature Request", "Urgent 🚨"]
            )
            
            message = st.text_area("📝 Describe your issue", placeholder="Tell us what you need help with...")
            
            submitted = st.form_submit_button("🚀 Start Chat", use_container_width=True)
            
            if submitted:
                if not name or not phone or not message:
                    st.error("Please fill all required fields!")
                else:
                    ticket_id = create_ticket(name, phone, email, issue_type, message)
                    st.session_state.user_ticket = ticket_id
                    st.balloons()
                    st.rerun()

def show_active_chat(ticket_id):
    """Show active chat for existing ticket"""
    ticket = st.session_state.tickets.get(ticket_id)
    if not ticket:
        del st.session_state.user_ticket
        st.rerun()
        return
    
    # Header
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(f"""
        <div style="background: #25D366; color: white; padding: 1rem; border-radius: 1rem; text-align: center;">
            <h3 style="margin: 0;">🎫 Ticket #{ticket_id}</h3>
            <p style="margin: 0; opacity: 0.9;">Status: <span class="status-online">● Online</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat Container
    chat_container = st.container()
    
    with chat_container:
        for msg in ticket['messages']:
            if msg['sender'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <b>You</b>
                    <p>{msg['text']}</p>
                    <span class="timestamp">{msg['timestamp'].strftime('%H:%M')}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message admin-message">
                    <b>🤖 Support Agent</b>
                    <p>{msg['text']}</p>
                    <span class="timestamp">{msg['timestamp'].strftime('%H:%M')}</span>
                </div>
                """, unsafe_allow_html=True)
    
    # Input Area
    st.markdown("---")
    col1, col2 = st.columns([4, 1])
    
    with col1:
        new_message = st.text_input("Type your message...", key="chat_input", 
                                   placeholder="Type here and press Enter...")
    
    with col2:
        if st.button("Send 📤", use_container_width=True):
            if new_message:
                # Add message
                ticket['messages'].append({
                    'sender': 'user',
                    'text': new_message,
                    'timestamp': datetime.now(),
                    'read': False
                })
                ticket['unread'] = True
                
                # Send WhatsApp notification for reply
                admin_phone = os.getenv('ADMIN_WHATSAPP_NUMBER', '919876543210')
                api_key = os.getenv('CALLMEBOT_API_KEY', '')
                
                notif_data = {
                    'name': ticket['name'],
                    'last_message': new_message,
                    'phone': ticket['phone']
                }
                
                if api_key:
                    send_whatsapp_callmebot(
                        admin_phone, 
                        format_whatsapp_message(notif_data, "reply"),
                        api_key
                    )
                
                st.rerun()

def render_admin_panel():
    """Render admin dashboard"""
    st.markdown('<h1 class="main-header">🎛️ Admin Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar Stats
    st.sidebar.markdown("### 📊 Quick Stats")
    total_tickets = len(st.session_state.tickets)
    open_tickets = sum(1 for t in st.session_state.tickets.values() if t['status'] == 'open')
    unread_tickets = sum(1 for t in st.session_state.tickets.values() if t['unread'])
    
    st.sidebar.metric("Total Tickets", total_tickets)
    st.sidebar.metric("Open", open_tickets)
    st.sidebar.metric("Unread", unread_tickets, delta=unread_tickets if unread_tickets > 0 else None)
    
    # Main Content
    tab1, tab2, tab3 = st.tabs(["🎫 All Tickets", "💬 Live Chat", "⚙️ Settings"])
    
    with tab1:
        st.subheader("Support Tickets")
        
        if not st.session_state.tickets:
            st.info("No tickets yet. Waiting for customers...")
        else:
            for ticket_id, ticket in sorted(st.session_state.tickets.items(), 
                                          key=lambda x: x[1]['created_at'], reverse=True):
                unread_class = "unread" if ticket['unread'] else ""
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="ticket-card {unread_class}" onclick="alert('Clicked')">
                        <h4>🎫 {ticket_id} - {ticket['name']}</h4>
                        <p>📱 {ticket['phone']} | 📋 {ticket['issue_type']}</p>
                        <p style="color: #666; font-size: 0.9rem;">📝 {ticket['message'][:100]}...</p>
                        <small>⏰ {ticket['created_at'].strftime('%Y-%m-%d %H:%M')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if ticket['unread']:
                        st.markdown("🔴 **New**")
                    status_color = "green" if ticket['status'] == 'open' else "gray"
                    st.markdown(f"<span style='color: {status_color};'>● {ticket['status'].upper()}</span>", 
                              unsafe_allow_html=True)
                
                with col3:
                    if st.button("Open Chat", key=f"open_{ticket_id}"):
                        st.session_state.current_ticket = ticket_id
                        ticket['unread'] = False
                        st.rerun()
                
                st.markdown("---")
    
    with tab2:
        if st.session_state.current_ticket:
            ticket = st.session_state.tickets[st.session_state.current_ticket]
            
            st.subheader(f"Chat with {ticket['name']}")
            
            # Chat display
            chat_box = st.container()
            with chat_box:
                for msg in ticket['messages']:
                    align = "right" if msg['sender'] == 'user' else "left"
                    bg_color = "#dcf8c6" if msg['sender'] == 'user' else "white"
                    sender = ticket['name'] if msg['sender'] == 'user' else "You (Admin)"
                    
                    st.markdown(f"""
                    <div style="text-align: {align}; margin: 10px 0;">
                        <div style="background: {bg_color}; display: inline-block; padding: 10px; border-radius: 10px; max-width: 70%; text-align: left;">
                            <small><b>{sender}</b></small><br>
                            {msg['text']}
                            <br><small style="opacity: 0.6;">{msg['timestamp'].strftime('%H:%M')}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Reply box
            reply = st.text_input("Reply to customer...", key="admin_reply")
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Send ✅"):
                    if reply:
                        ticket['messages'].append({
                            'sender': 'admin',
                            'text': reply,
                            'timestamp': datetime.now(),
                            'read': False
                        })
                        
                        # Send WhatsApp to customer
                        customer_phone = ticket['phone']
                        api_key = os.getenv('CALLMEBOT_API_KEY', '')
                        
                        msg = f"""📩 *Support Reply*

Hello {ticket['name']},

{reply}

_Reply to this chat to continue..."""
                        
                        if api_key:
                            send_whatsapp_callmebot(customer_phone, msg, api_key)
                        
                        st.success("Reply sent!")
                        st.rerun()
            
            with col2:
                if st.button("🔙 Back to Tickets"):
                    st.session_state.current_ticket = None
                    st.rerun()
        else:
            st.info("Select a ticket from the 'All Tickets' tab to start chatting")
    
    with tab3:
        st.subheader("⚙️ WhatsApp API Settings")
        
        st.markdown("""
        ### 🔧 Configuration
        
        **Option 1: CallMeBot (Free)**
        1. Save this number: +34 644 52 53 02
        2. Send message: `I allow callmebot to send me messages`
        3. Get your API key in reply
        4. Enter below:
        """)
        
        api_key = st.text_input("CallMeBot API Key", value=os.getenv('CALLMEBOT_API_KEY', ''), type="password")
        admin_phone = st.text_input("Your WhatsApp Number (with country code)", 
                                   value=os.getenv('ADMIN_WHATSAPP_NUMBER', ''))
        
        if st.button("Save Settings"):
            # In production, save to database
            st.success("Settings saved! (In demo mode)")
        
        st.markdown("---")
        
        st.markdown("""
        ### 📱 Test WhatsApp
        Send a test message to verify setup:
        """)
        
        test_phone = st.text_input("Test Phone Number", placeholder="919876543210")
        test_msg = st.text_input("Test Message", value="🧪 Test message from Support System")
        
        if st.button("Send Test"):
            if api_key and test_phone:
                success = send_whatsapp_callmebot(test_phone, test_msg, api_key)
                if success:
                    st.success("Test message sent! Check your WhatsApp.")
                else:
                    st.error("Failed to send. Check API key.")
            else:
                st.error("Please enter API key and phone number")

def main():
    init_database()
    
    # Sidebar Navigation
    st.sidebar.title("🚀 Navigation")
    
    if st.session_state.admin_logged_in:
        page = st.sidebar.radio("Go to", ["Admin Panel", "Logout"])
        
        if page == "Logout":
            st.session_state.admin_logged_in = False
            st.rerun()
        else:
            render_admin_panel()
    else:
        page = st.sidebar.radio("Go to", ["Customer Support", "Admin Login"])
        
        if page == "Customer Support":
            render_chat_interface()
        else:
            st.sidebar.markdown("---")
            st.sidebar.subheader("🔐 Admin Login")
            password = st.sidebar.text_input("Password", type="password")
            
            if st.sidebar.button("Login"):
                if password == os.getenv('ADMIN_PASSWORD', 'admin123'):
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.sidebar.error("Wrong password!")

if __name__ == "__main__":
    main()
