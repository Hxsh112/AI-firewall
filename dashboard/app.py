import streamlit as st
import requests
import pandas as pd
from src.feature_extractor import simulate_sample, FEATURE_COLUMNS

# ------------------------------------------
# DASHBOARD CONFIGURATION
# ------------------------------------------
st.set_page_config(
    page_title="AI Firewall Dashboard",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------
# HEADER SECTION
# ------------------------------------------
st.title("🛡️ AI Firewall — Intelligent Threat Detection")
st.caption("Real-time behavioral malware analysis using AI and ML models")

st.markdown("---")

# Sidebar setup
st.sidebar.header("⚙️ Configuration")
api_url = st.sidebar.text_input("API Endpoint", value="http://localhost:8000/detect")
sample_size = st.sidebar.slider("Generate synthetic samples", 1, 50, 5)

# ------------------------------------------
# DATA GENERATION SECTION
# ------------------------------------------
st.subheader("📡 Generate Traffic Samples")

df = simulate_sample(sample_size)
st.dataframe(df, use_container_width=True)

st.markdown("---")

# ------------------------------------------
# TEST SAMPLE SECTION
# ------------------------------------------
st.subheader("🚀 Run Detection")

col1, col2 = st.columns([3, 2])

with col1:
    st.write("Choose a sample index from generated data")
    sample_index = st.number_input("Sample Index", 0, sample_size - 1, 0)

    if st.button("Analyze Selected Sample", use_container_width=True):
        try:
            sample = df.iloc[sample_index].to_dict()
            response = requests.post(api_url, json=sample, timeout=5)
            result = response.json()["result"]

            st.success("Scan Completed Successfully")
            st.metric("Malicious", str(result["malicious"]))
            st.metric("Threat Score", f"{result['score']:.2f}")

        except Exception as e:
            st.error(f"API Error: {e}")

with col2:
    st.info("You can manually input feature values below for testing custom scenarios.")

# ------------------------------------------
# MANUAL INPUT SECTION
# ------------------------------------------
st.subheader("🧠 Manual Threat Simulation")

manual_input = {}
for feature in FEATURE_COLUMNS:
    manual_input[feature] = st.number_input(feature, value=0.0, step=1.0)

if st.button("Run Manual Detection", use_container_width=True):
    try:
        response = requests.post(api_url, json=manual_input, timeout=5)
        result = response.json()["result"]

        col1, col2 = st.columns(2)
        col1.metric("Detected as", "Malicious" if result["malicious"] else "Safe")
        col2.metric("AI Confidence", f"{result['score']*100:.2f}%")
        if result["malicious"]:
            st.error("⚠️ Potential Threat Detected — Block Recommended")
        else:
            st.success("✅ No malicious activity detected")
    except Exception as e:
        st.error(f"API Error: {e}")

st.markdown("---")

# ------------------------------------------
# FOOTER SECTION
# ------------------------------------------
st.caption("Developed by Harsh Kumar | AI Firewall Prototype | Streamlit + FastAPI + Scikit-learn")
