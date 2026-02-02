"""
FAQ Chatbot - Streamlit Dashboard
Professional blue and yellow theme with side-by-side layout
"""

import streamlit as st
import os
from init_db import create_database, populate_faqs, get_all_faqs, get_faq_count
from faq_matcher import FAQMatcher

# Page configuration
st.set_page_config(
    page_title="Fashion FAQ Chatbot",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: #1E3A8A;
    }
    
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    /* Left section */
    .left-content {
        background: linear-gradient(rgba(30, 58, 138, 0.85), rgba(30, 58, 138, 0.85)), 
                    url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1200') center/cover;
        min-height: 100vh;
        padding: 3rem;
        color: white;
    }
    
    .left-content h1 {
        font-size: 3rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 1.5rem;
        color: white;
    }
    
    .left-content p {
        font-size: 1.1rem;
        line-height: 1.6;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 3rem;
    }
    
    .info-block {
        margin-bottom: 2rem;
    }
    
    .info-block h3 {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .info-block p {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.5;
        margin-bottom: 0;
    }
    
    /* Right section */
    .right-content {
        background: #F8FAFC;
        min-height: 100vh;
        padding: 2.5rem;
    }
    
    .right-content h2 {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    
    .right-content .subheader {
        font-size: 0.95rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    
    /* Stats */
    .stat-box {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border: 1px solid #E2E8F0;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    
    .stat-label {
        color: #64748B;
        font-size: 0.85rem;
        margin-top: 4px;
        font-weight: 500;
    }
    
    /* Chat */
    .chat-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        max-height: 450px;
        overflow-y: auto;
        border: 1px solid #E2E8F0;
    }
    
    .user-message {
        background: #FCD34D;
        color: #1E3A8A;
        padding: 12px 16px;
        border-radius: 12px 12px 2px 12px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    .bot-answer {
        background: #EFF6FF;
        color: #1E293B;
        padding: 16px;
        border-radius: 12px;
        margin: 10px 0;
        border-left: 4px solid #1E3A8A;
    }
    
    .bot-answer strong {
        color: #1E3A8A;
        display: block;
        margin-bottom: 8px;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .bot-message {
        background: #FEF3C7;
        color: #92400E;
        padding: 14px;
        border-radius: 12px;
        margin: 10px 0;
        border-left: 4px solid #FCD34D;
        font-size: 0.9rem;
    }
    
    .info-box {
        background: #DBEAFE;
        padding: 14px 16px;
        border-radius: 12px;
        margin: 10px 0;
        color: #1E40AF;
        font-weight: 500;
        border-left: 4px solid #3B82F6;
        font-size: 0.9rem;
    }
    
    .category-badge {
        display: inline-block;
        background: #1E3A8A;
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 4px 4px 4px 0;
    }
    
    .similarity-score {
        background: #FCD34D;
        color: #1E3A8A;
        padding: 6px 14px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 8px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* Input */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #CBD5E1;
        padding: 12px 16px;
        font-size: 0.95rem;
        background: white;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1E3A8A;
        box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1);
        outline: none;
    }
    
    /* Button */
    .stButton > button {
        background: #FCD34D;
        color: #1E3A8A;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        border: none;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #FBBF24;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Scrollbar */
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #F1F5F9;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #CBD5E1;
        border-radius: 10px;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    [data-testid="column"] {
        padding: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize
@st.cache_resource
def initialize_system():
    if not os.path.exists("faqs.db"):
        create_database()
        populate_faqs()
    faqs = get_all_faqs()
    matcher = FAQMatcher(faqs)
    return matcher, faqs

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

matcher, faqs = initialize_system()

# Layout
col1, col2 = st.columns([1, 1])

# LEFT COLUMN
with col1:
    st.markdown("""
    <div class="left-content">
        <h1>You Have Questions,<br>We Have Answers</h1>
        <p>Discover our premium clothing collection designed with care. Get instant answers to all your questions about sizing, shipping, returns, and more.</p>
        
        <div style="margin-top: 4rem;">
            <div class="info-block">
                <h3>📍 About Us</h3>
                <p>Premium Fashion Boutique<br>Delivering quality since 2020<br>Worldwide shipping available</p>
            </div>
            
            <div class="info-block">
                <h3>📧 Contact</h3>
                <p>Email: support@clothingbrand.com<br>Phone: +1 (555) 123-4567<br>Hours: Mon-Sun | 9:00 AM - 10:00 PM</p>
            </div>
            
            <div class="info-block">
                <h3>🌐 Follow Us</h3>
                <p>Instagram | Facebook | Twitter<br>@fashionboutique</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# RIGHT COLUMN
with col2:
    st.markdown('<div class="right-content">', unsafe_allow_html=True)
    st.markdown('<h2>FAQ Assistant</h2>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Our team is ready to assist you with every detail, big or small.</p>', unsafe_allow_html=True)
    
    # Stats
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{get_faq_count()}</div><div class="stat-label">FAQs</div></div>', unsafe_allow_html=True)
    with s2:
        categories = matcher.get_all_categories()
        st.markdown(f'<div class="stat-box"><div class="stat-number">{len(categories)}</div><div class="stat-label">Categories</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{len(st.session_state.chat_history)}</div><div class="stat-label">Asked</div></div>', unsafe_allow_html=True)
    
    # Chat
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            st.markdown(f'<div class="user-message">❓ {chat["question"]}</div>', unsafe_allow_html=True)
            
            if chat['match']:
                st.markdown(f'''
                    <div class="bot-answer">
                        <strong>📌 {chat['match']['question']}</strong>
                        {chat['match']['answer']}
                        <br><br>
                        <span class="category-badge">{chat['match']['category']}</span>
                        <span class="similarity-score">🎯 {chat['match']['similarity_score']}% Match</span>
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown('<div class="bot-message">😕 I couldn\'t find a good match. Please try rephrasing or contact support@clothingbrand.com</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">💡 <strong>Try asking:</strong> "What sizes do you offer?", "How long does shipping take?", "What is your return policy?"</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input
    i1, i2 = st.columns([4, 1])
    with i1:
        user_question = st.text_input("Your Question", placeholder="Type your question here...", label_visibility="collapsed", key="user_input")
    with i2:
        ask_button = st.button("Ask 🚀", use_container_width=True)
    
    if ask_button and user_question:
        match = matcher.find_best_match(user_question)
        st.session_state.chat_history.append({'question': user_question, 'match': match})
        st.rerun()
    
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Categories
    st.markdown('<br><p style="font-size: 0.9rem; font-weight: 600; color: #1E3A8A; margin-bottom: 0.5rem;">📂 Categories</p>', unsafe_allow_html=True)
    for category in categories:
        st.markdown(f'<span class="category-badge">{category}</span>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
