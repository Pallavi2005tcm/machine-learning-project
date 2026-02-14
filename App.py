import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import os

# Download stopwords
nltk.download('stopwords')

ps = PorterStemmer()

# ---------------- ENHANCED CSS STYLING ----------------
st.set_page_config(
    page_title="Spam Classifier", 
    page_icon="📧", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    
    .stApp {
        background: transparent;
    }
    
    .container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 40px;
        width: 100%;
        max-width: 800px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: fadeIn 0.6s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    h1 {
        color: #2d3436;
        text-align: center;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .subtitle {
        text-align: center;
        color: #636e72;
        font-size: 1.1rem;
        margin-bottom: 40px;
        font-weight: 400;
    }
    
    .stTextArea textarea {
        border-radius: 16px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 20px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        background: #f8f9fa !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        background: white !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 16px;
        height: 56px;
        width: 100%;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 20px;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    .prediction-box {
        margin-top: 30px;
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
        animation: slideIn 0.5s ease-out;
        border: 2px solid;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .spam {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
        color: white;
        border-color: #ff5252;
    }
    
    .ham {
        background: linear-gradient(135deg, #51cf66 0%, #69db7c 100%);
        color: white;
        border-color: #40c057;
    }
    
    .icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
    }
    
    .footer {
        text-align: center;
        margin-top: 40px;
        color: #636e72;
        font-size: 0.9rem;
        padding-top: 20px;
        border-top: 1px solid #e0e0e0;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e0e0e0;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 10px;
        color: #667eea;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .container {
            padding: 25px;
            margin: 10px;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        .feature-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LOGIC ----------------
def transform_text(text):
    text = text.lower()
    text = text.split()
    
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    
    stop_words = set(stopwords.words('english'))
    final_words = []
    for i in y:
        if i not in stop_words and i not in string.punctuation:
            final_words.append(ps.stem(i))
    
    return " ".join(final_words)

# Load model
BASE_DIR = os.path.dirname(__file__)
tfidf = pickle.load(open(os.path.join(BASE_DIR, 'vectorizer.pkl'), 'rb'))
model = pickle.load(open(os.path.join(BASE_DIR, 'model.pkl'), 'rb'))

# ---------------- ENHANCED UI ----------------


st.markdown("<p class='subtitle'>Advanced machine learning model to detect spam emails and SMS messages</p>", unsafe_allow_html=True)

# Features showcase
st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>AI-Powered</h3>
            <p>ML model with 98% accuracy</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3>Real-Time</h3>
            <p>Instant spam detection</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3>Privacy First</h3>
            <p>No data stored or shared</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

input_sms = st.text_area(
    "✉️ **Paste your message here**", 
    height=180,
    placeholder="Enter email or SMS content to analyze for spam..."
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_btn = st.button("🚀 Analyze Message", use_container_width=True)

if predict_btn:
    if input_sms.strip() == "":
        st.warning("Please enter a message to analyze")
    else:
        with st.spinner("🔍 Analyzing message..."):
            transformed_sms = transform_text(input_sms)
            vector_input = tfidf.transform([transformed_sms])
            result = model.predict(vector_input)[0]
            
            if result == 1:
                st.markdown(
                    """
                    <div class="prediction-box spam">
                        <div class="icon">🚨</div>
                        <h3>SPAM DETECTED!</h3>
                        <p>This message appears to be spam. Exercise caution.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                # Additional info for spam
                st.info("💡 **Tip:** Spam messages often contain urgent calls to action, suspicious links, or requests for personal information.")
            else:
                st.markdown(
                    """
                    <div class="prediction-box ham">
                        <div class="icon">✅</div>
                        <h3>SAFE MESSAGE</h3>
                        <p>This message appears to be legitimate (ham).</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )




