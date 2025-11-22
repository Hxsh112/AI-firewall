import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import requests
import pandas as pd
from src.feature_extractor import simulate_sample, FEATURE_COLUMNS
from time import sleep

# PAGE CONFIG

st.set_page_config(
    page_title="AI Firewall Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# CUSTOM CSS STYLING
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #e0e0e0;
}
.stApp {
    background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
}
h1, h2, h3, h4 {
    color: #00c8ff !important;
    font-weight: 700;
}
.metric-card {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin-top: 10px;
    transition: all 0.3s ease;
}
.metric-card:hover {
    background: rgba(0,200,255,0.15);
    transform: scale(1.02);
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# HEADER

st.title("🛡️ AI Firewall Dashboard")
st.caption("AI-powered behavioral malware detection prototype")

# Sidebar
st.sidebar.header("⚙️ Settings")
api_url = st.sidebar.text_input("API Endpoint", "http://localhost:8000/detect")
sample_size = st.sidebar.slider("Sample Size", 1, 50, 5)
st.sidebar.markdown("---")
st.sidebar.info("Ensure FastAPI backend is running before detection (`uvicorn api.main:app --port 8000`).")

# SECTION: GENERATE DATA
st.subheader("📡 Simulate Network Activity")
df = simulate_sample(sample_size)
st.dataframe(df, use_container_width=True)

# SECTION: DETECTION
st.markdown("---")
st.subheader("🚀 Threat Detection Panel")

col1, col2 = st.columns([3, 2])

with col1:
    idx = st.number_input("Select Sample Index", 0, sample_size - 1, 0)
    if st.button("Run Detection", use_container_width=True, type="primary"):
        with st.spinner("Analyzing traffic sample..."):
            try:
                payload = df.iloc[idx].to_dict()
                response = requests.post(api_url, json=payload, timeout=5)
                result = response.json()["result"]
                score = round(result["score"] * 100, 2)
                st.markdown("### ✅ Scan Result")
                if result["malicious"]:
                    st.markdown(
                        f"<div class='metric-card' style='border-left:5px solid #ff4d4d;'>"
                        f"<h3>🚨 MALICIOUS TRAFFIC DETECTED</h3>"
                        f"<p>Threat Score: <b>{score}%</b></p>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<div class='metric-card' style='border-left:5px solid #00ff88;'>"
                        f"<h3>✅ SAFE TRAFFIC</h3>"
                        f"<p>Threat Score: <b>{score}%</b></p>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            except Exception as e:
                st.error(f"⚠️ API call failed: {e}")

with col2:
    st.info("ℹ️ You can also input custom values manually below to simulate specific conditions.")

# SECTION: MANUAL INPUT

st.markdown("---")
st.subheader("🧠 Manual Threat Simulation")

with st.expander("Enter feature values manually"):
    manual = {}
    for f in FEATURE_COLUMNS:
        manual[f] = st.number_input(f, 0.0, 100000.0, 0.0)

    if st.button("Run Manual Detection", use_container_width=True):
        with st.spinner("Running manual analysis..."):
            try:
                response = requests.post(api_url, json=manual, timeout=5)
                result = response.json()["result"]
                score = round(result["score"] * 100, 2)
                st.markdown("### 🧩 Manual Detection Result")
                if result["malicious"]:
                    st.error(f"🚨 Potential Threat — Confidence {score}%")
                else:
                    st.success(f"✅ Clean Sample — Confidence {score}%")
            except Exception as e:
                st.error(f"Error: {e}")
                
# SECTION: FOOTER

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Developed by Harsh Jain • AI Firewall Prototype • Streamlit + FastAPI</p>",
    unsafe_allow_html=True,
)
