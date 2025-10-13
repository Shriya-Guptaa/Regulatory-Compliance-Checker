# auth_manager.py - Authentication System with Temp Session Support

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

VALID_USERS = {
    "admin@company.com": {
        "password": "admin123",
        "name": "Admin User",
        "role": "Administrator"
    },
    "user@company.com": {
        "password": "user123",
        "name": "Regular User",
        "role": "Analyst"
    }
}

ENV_USER = os.getenv("AUTH_USER")
ENV_PASSWORD = os.getenv("AUTH_PASSWORD")
ENV_NAME = os.getenv("AUTH_NAME", "Environment User")

if ENV_USER and ENV_PASSWORD:
    VALID_USERS[ENV_USER] = {
        "password": ENV_PASSWORD,
        "name": ENV_NAME,
        "role": "User"
    }


def initialize_auth_session():
    """Initialize authentication session state"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "temp_session" not in st.session_state:
        st.session_state.temp_session = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = None
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "login_time" not in st.session_state:
        st.session_state.login_time = None


def authenticate_user(email, password):
    """Authenticate user with email and password"""
    if email in VALID_USERS:
        if VALID_USERS[email]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.temp_session = False
            st.session_state.user_email = email
            st.session_state.user_name = VALID_USERS[email]["name"]
            st.session_state.user_role = VALID_USERS[email]["role"]
            st.session_state.login_time = datetime.now()
            return True, "Login successful!"
    return False, "Invalid email or password"


def create_temp_session(email):
    """Create temporary session for guest users"""
    st.session_state.authenticated = True
    st.session_state.temp_session = True
    st.session_state.user_email = email
    st.session_state.user_name = f"Guest ({email})"
    st.session_state.user_role = "Guest"
    st.session_state.login_time = datetime.now()
    return True


def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)


def is_temp_session():
    """Check if current session is temporary"""
    return st.session_state.get("temp_session", False)


def get_current_user():
    """Get current user information"""
    if not is_authenticated():
        return None
    
    return {
        "email": st.session_state.get("user_email"),
        "name": st.session_state.get("user_name"),
        "role": st.session_state.get("user_role"),
        "logged_in": not is_temp_session(),
        "is_temp": is_temp_session(),
        "login_time": st.session_state.get("login_time")
    }


def logout_user():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.temp_session = False
    st.session_state.user_email = None
    st.session_state.user_name = None
    st.session_state.user_role = None
    st.session_state.login_time = None


def show_login_form():
    """Display compact login form"""
    st.markdown("""
    <div style="text-align:center;padding:2rem 0;">
        <h1 style="color:#10b981;font-size:3rem;margin-bottom:0.5rem;">⚖️</h1>
        <h2 style="color:#fff;margin-bottom:0.5rem;">AI Compliance Dashboard</h2>
        <p style="color:#9ca3af;">Contract analysis with AI-powered risk assessment</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Login", "🚀 Quick Access"])
    
    with tab1:
        st.markdown("""
        <div style="background:#374151;padding:1.5rem;border-radius:10px;margin:1rem 0;">
            <h3 style="color:#10b981;margin-top:0;">Full Access</h3>
            <p style="color:#d1d5db;margin-bottom:0;">Login for all features including email notifications</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="user@company.com")
            password = st.text_input("🔑 Password", type="password")
            submit = st.form_submit_button("🔓 Login", use_container_width=True, type="primary")
            
            if submit:
                if not email or not password:
                    st.error("⚠️ Please enter email and password")
                else:
                    success, message = authenticate_user(email, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        with st.expander("🔍 Demo Credentials"):
            st.code("admin@company.com / admin123\nuser@company.com / user123")
    
    with tab2:
        st.markdown("""
        <div style="background:#374151;padding:1.5rem;border-radius:10px;margin:1rem 0;">
            <h3 style="color:#f59e0b;margin-top:0;">⚡ Temporary Session</h3>
            <p style="color:#d1d5db;margin-bottom:0;">Quick access (email disabled)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💡 Temporary sessions allow contract analysis but disable email notifications.")
        
        with st.form("temp_form"):
            temp_email = st.text_input("📧 Your Email", placeholder="guest@example.com")
            temp_submit = st.form_submit_button("🚀 Start Session", use_container_width=True)
            
            if temp_submit:
                if not temp_email or "@" not in temp_email:
                    st.error("⚠️ Please enter valid email")
                else:
                    create_temp_session(temp_email)
                    st.success(f"✅ Session created for {temp_email}")
                    st.rerun()


def show_user_info():
    """Display user info in sidebar"""
    if not is_authenticated():
        return
    
    user = get_current_user()
    
    st.sidebar.markdown("---")
    
    if user["is_temp"]:
        st.sidebar.markdown("""
        <div style="background:#92400e;padding:1rem;border-radius:8px;border:2px solid #f59e0b;">
            <h4 style="margin:0;color:#fbbf24;">⚡ Temp Session</h4>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div style="background:#065f46;padding:1rem;border-radius:8px;border:2px solid #10b981;">
            <h4 style="margin:0;color:#10b981;">✅ Authenticated</h4>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown(f"""
    <div style="padding:1rem 0;">
        <p style="margin:0.5rem 0;color:#9ca3af;font-size:0.875rem;">
            <strong>👤 Name:</strong><br>
            <span style="color:#fff;">{user['name']}</span>
        </p>
        <p style="margin:0.5rem 0;color:#9ca3af;font-size:0.875rem;">
            <strong>📧 Email:</strong><br>
            <span style="color:#fff;">{user['email']}</span>
        </p>
        <p style="margin:0.5rem 0;color:#9ca3af;font-size:0.875rem;">
            <strong>🎭 Role:</strong><br>
            <span style="color:#fff;">{user['role']}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if user["is_temp"]:
        st.sidebar.warning("⚠️ Email disabled in temp sessions")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        logout_user()
        st.rerun()


def require_auth(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            st.error("🔒 Authentication required")
            return None
        return func(*args, **kwargs)
    return wrapper


def require_full_auth(func):
    """Decorator to require full authentication (not temp)"""
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            st.error("🔒 Authentication required")
            return None
        if is_temp_session():
            st.error("🔒 Full authentication required")
            return None
        return func(*args, **kwargs)
    return wrapper