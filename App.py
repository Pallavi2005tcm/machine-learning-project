import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="SpamGuard Pro",
    page_icon="📧",
    layout="centered"
)

# ---------------- NLTK (SAFE) ----------------
@st.cache_resource
def load_stopwords():
    nltk.download("stopwords")
    return set(stopwords.words("english"))

STOP_WORDS = load_stopwords()
ps = PorterStemmer()

# ---------------- MODEL ----------------
BASE_DIR = os.path.dirname(__file__)
tfidf = pickle.load(open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb"))
model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))

# ---------------- LOGIC ----------------
def transform_text(text):
    text = text.lower().split()

    clean_words = []
    for word in text:
        if word.isalnum() and word not in STOP_WORDS:
            clean_words.append(ps.stem(word))

    return " ".join(clean_words)

# ---------------- CSS ----------------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
    }
    .main-box {
        background: white;
        padding: 40px;
        border-radius: 24px;
        max-width: 900px;
        margin: auto;
        box-shadow: 0 25px 50px rgba(102,126,234,0.15);
        border: 3px solid #667eea;
    }
    .title {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    .stButton button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        height: 60px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- UI ----------------
st.markdown(
    """
    <div class="main-box">
        <div class="title">📧 SpamGuard Pro</div>
        <div class="subtitle">
            AI-powered spam detection for emails and SMS messages
        </div>
    """,
    unsafe_allow_html=True
)

input_sms = st.text_area(
    "✉️ Enter your message",
    height=180,
    placeholder="Congratulations! You won ₹10,00,000. Click here now!"
)

if st.button("🚀 Analyze for Spam", use_container_width=True):
    if input_sms.strip() == "":
        st.warning("Please enter a message")
    else:
        with st.spinner("Analyzing message..."):
            transformed_sms = transform_text(input_sms)
            vector_input = tfidf.transform([transformed_sms])
            result = model.predict(vector_input)[0]

        if result == 1:
            st.error("🚨 **SPAM DETECTED**\n\nThis message looks suspicious. Be careful.")
        else:
            st.success("✅ **SAFE MESSAGE**\n\nNo spam indicators found.")

st.markdown("</div>", unsafe_allow_html=True)

