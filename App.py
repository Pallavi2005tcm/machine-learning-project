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

# ---------------- CSS STYLING ----------------
st.set_page_config(page_title="Spam Classifier", page_icon="💌", layout="centered")

st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #ff9a9e, #fad0c4);
    }
    .main {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.15);
    }
    h1 {
        color: #e91e63;
        text-align: center;
    }
    textarea {
        border-radius: 12px !important;
    }
    .stButton>button {
        background-color: #e91e63;
        color: white;
        border-radius: 12px;
        height: 3em;
        width: 100%;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #c2185b;
        color: white;
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

# ---------------- UI ----------------
st.markdown("<h1>💌 Email / SMS Spam Classifier</h1>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center;color:#555;'>Paste a message below to check if it is spam</p>",
    unsafe_allow_html=True
)

input_sms = st.text_area("✉️ Enter your message", height=150)

if st.button("🔍 Predict"):
    if input_sms.strip() == "":
        st.warning("Please enter a message")
    else:
        transformed_sms = transform_text(input_sms)
        vector_input = tfidf.transform([transformed_sms])
        result = model.predict(vector_input)[0]

        if result == 1:
            st.error("🚨 This message is SPAM")
        else:
            st.success("✅ This message is NOT spam")
