import streamlit as st
import requests
import json
from src.feature_extractor import simulate_sample, FEATURE_COLUMNS
import pandas as pd

st.title("AI Firewall — Demo Dashboard")
st.write("Generate a sample, inspect features, and run local detection.")

col1, col2 = st.columns(2)
with col1:
    n = st.number_input("Generate samples", min_value=1, max_value=50, value=1)
    df = simulate_sample(n)
    st.dataframe(df)

with col2:
    st.write("Detection controls")
    api_url = st.text_input("API URL", value="http://localhost:8000/detect")
    idx = st.number_input("Sample index to test", min_value=0, max_value=max(0, len(df)-1), value=0)

if st.button("Run detection on sample"):
    sample = df.iloc[idx].to_dict()
    st.write("Input features:")
    st.json(sample)
    try:
        resp = requests.post(api_url, json=sample, timeout=5)
        st.write("API response:")
        st.json(resp.json())
    except Exception as e:
        st.error(f"API call failed: {e}")

st.markdown("---")
st.write("Manual input")
manual = {k: st.text_input(k, value=str(0)) for k in FEATURE_COLUMNS}
if st.button("Test manual"):
    # coerce types
    payload = {
        "src_port": int(manual['src_port'] or 0),
        "dst_port": int(manual['dst_port'] or 0),
        "pkt_count": int(manual['pkt_count'] or 0),
        "byte_count": int(manual['byte_count'] or 0),
        "duration": float(manual['duration'] or 0.0),
        "entropy": float(manual['entropy'] or 0.0),
        "uncommon_dst_ip": int(manual['uncommon_dst_ip'] or 0),
        "process_spawn_count": int(manual['process_spawn_count'] or 0),
    }
    try:
        resp = requests.post(api_url, json=payload, timeout=5)
        st.json(resp.json())
    except Exception as e:
        st.error(f"API call failed: {e}")
