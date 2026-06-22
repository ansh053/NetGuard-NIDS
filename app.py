import streamlit as st
import pandas as pd
import joblib
import numpy as np
import time

# --- UI Configuration ---
st.set_page_config(
    page_title="AI-NIDS Console", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ System Status")
    st.success("Detection Engine: Online")
    st.info("Model: Custom NSL-KDD")
    st.markdown("---")
    st.write("Use the main dashboard to evaluate incoming network package parameters manually.")

# --- Main Header ---
st.title("🛡️ Enterprise SOC Dashboard")
st.markdown("Evaluate incoming network package parameters against our custom NSL-KDD detection engine to identify malicious anomalies.")
st.divider()

@st.cache_resource
def load_assets():
    model = joblib.load("nids_model.pkl")
    features = joblib.load("model_features.pkl")
    return model, features

try:
    model, feature_names = load_assets()
    
    st.subheader("📥 Telemetry Metric Entry")
    
    # Grouping inputs logically using containers and columns
    col_route, col_payload, col_freq = st.columns(3)
    
    with col_route:
        st.markdown("**Network & Routing**")
        protocol = st.selectbox("Protocol Layer", ["tcp", "udp", "icmp"])
        service = st.selectbox("Target Core Port Service", ["http", "smtp", "private", "ftp_data", "domain", "other"])
        flag = st.selectbox("Connection State Flag", ["SF", "S0", "REJ", "RSTO", "RSTR"])
        
    with col_payload:
        st.markdown("**Payload & Session**")
        duration = st.number_input("Duration (sec)", min_value=0.0, value=0.0, step=0.1)
        src_bytes = st.number_input("Source Payload (Bytes)", min_value=0, value=0, step=100)
        dst_bytes = st.number_input("Destination Payload (Bytes)", min_value=0, value=0, step=100)
        
    with col_freq:
        st.markdown("**Frequency & Auth (Past 2s)**")
        count = st.number_input("Connections to same host", min_value=0, value=1)
        srv_count = st.number_input("Connections to same service", min_value=0, value=1)
        logged_in = st.selectbox("Successful Auth?", ["No", "Yes"])

    # --- DataFrame Construction ---
    input_df = pd.DataFrame(np.zeros((1, len(feature_names))), columns=feature_names)
    
    if 'duration' in input_df.columns: input_df['duration'] = duration
    if 'src_bytes' in input_df.columns: input_df['src_bytes'] = src_bytes
    if 'dst_bytes' in input_df.columns: input_df['dst_bytes'] = dst_bytes
    if 'count' in input_df.columns: input_df['count'] = count
    if 'srv_count' in input_df.columns: input_df['srv_count'] = srv_count
    if 'logged_in' in input_df.columns: input_df['logged_in'] = 1 if logged_in == "Yes" else 0
    
    proto_col = f"protocol_type_{protocol}"
    flag_col = f"flag_{flag}"
    service_col = f"service_{service}"
    
    if proto_col in input_df.columns: input_df[proto_col] = 1
    if flag_col in input_df.columns: input_df[flag_col] = 1
    if service_col in input_df.columns: input_df[service_col] = 1

    if flag == "S0":
        for col in ['serror_rate', 'srv_serror_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate']:
            if col in input_df.columns:
                input_df[col] = 1.0
                
    if flag in ["REJ", "RSTO", "RSTR"]:
        for col in ['rerror_rate', 'srv_rerror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate']:
            if col in input_df.columns:
                input_df[col] = 1.0

    if 'dst_host_count' in input_df.columns: input_df['dst_host_count'] = max(255, count)
    if 'dst_host_srv_count' in input_df.columns: input_df['dst_host_srv_count'] = srv_count

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Execution Block
    col_btn, col_empty = st.columns([1, 3])
    with col_btn:
        execute = st.button("🚀 Execute Forensic Inspection", use_container_width=True, type="primary")

    if execute:
        with st.spinner('Analyzing network traffic signatures...'):
            # Simulating a slight delay for realism/UX
            time.sleep(0.5) 
            prediction = model.predict(input_df)[0]
            confidence = model.predict_proba(input_df)[0]
            
        st.divider()
        st.subheader("📊 Inspection Results")
        
        res_col1, res_col2 = st.columns([2, 1])
        
        with res_col1:
            if prediction == 1:
                st.error("🚨 **CRITICAL ALERT: Malicious Anomaly Intercepted!**")
                st.warning("Anomaly profile resembles typical Probe/DoS signature behaviors. Applying network level isolation protocols.")
            else:
                st.success("✅ **Clean Signal Verification: Normal Connection.**")
                st.info("Packet behaviors align safely with standard operating limits.")
                
        with res_col2:
            conf_val = confidence[1]*100 if prediction == 1 else confidence[0]*100
            st.metric(label="Model Confidence", value=f"{conf_val:.2f}%")
            st.progress(int(conf_val))

    with st.expander("🔍 View Raw Telemetry Data Payload"):
        st.dataframe(input_df)

except FileNotFoundError:
    st.error("❌ **Model configurations missing.** Run `python train.py` from your workspace environment terminal first.")
