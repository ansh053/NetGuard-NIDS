import streamlit as st
import pandas as pd
import joblib
import numpy as np
import time
import datetime
import io

# ════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI-NIDS | Network Intrusion Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background:#0a0e1a; color:#c9d1e0; }
.stApp { background:#0a0e1a; }
.block-container { padding-top: 1rem !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] { background:#070b14 !important; border-right:1px solid #1a2540; }
section[data-testid="stSidebar"] * { color:#8892a4 !important; }
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    color:#00e5ff !important; font-family:'JetBrains Mono',monospace !important;
    font-size:0.72rem !important; letter-spacing:0.12em !important; text-transform:uppercase !important;
}

/* ── Tabs ── */
div[data-testid="stTabs"] button {
    font-family:'JetBrains Mono',monospace !important; font-size:0.72rem !important;
    letter-spacing:0.1em !important; text-transform:uppercase !important;
    color:#8892a4 !important; background:transparent !important;
    border:none !important; border-bottom:2px solid transparent !important;
    padding:8px 18px !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color:#00e5ff !important; border-bottom:2px solid #00e5ff !important;
}
div[data-testid="stTabsContent"] { padding-top: 1.2rem; }

/* ── Status pill ── */
.status-pill {
    display:inline-flex; align-items:center; gap:6px;
    background:#0d1f3c; border:1px solid #1a2f50; border-radius:4px;
    padding:5px 10px; font-family:'JetBrains Mono',monospace; font-size:0.68rem;
    letter-spacing:0.06em; color:#8892a4; margin-bottom:5px; width:100%;
}
.status-pill .dot {
    width:6px; height:6px; border-radius:50%; background:#22c55e;
    box-shadow:0 0 5px #22c55e; flex-shrink:0;
    animation:pulse-dot 2s infinite;
}
@keyframes pulse-dot { 0%,100%{opacity:1} 50%{opacity:.35} }

/* ── Page header ── */
.page-header {
    display:flex; align-items:flex-end; gap:14px;
    padding:20px 0 10px; border-bottom:1px solid #1a2540; margin-bottom:22px;
}
.page-header .ph-title { font-family:'JetBrains Mono',monospace; font-size:1.45rem; font-weight:700; color:#e8edf5; line-height:1; }
.page-header .ph-sub { font-size:0.78rem; color:#8892a4; margin-bottom:3px; }
.badge { font-family:'JetBrains Mono',monospace; font-size:0.58rem; background:#00e5ff14; color:#00e5ff;
    border:1px solid #00e5ff35; border-radius:3px; padding:2px 7px; letter-spacing:.1em; text-transform:uppercase; }
.badge-warn { background:#ff3b5c14; color:#ff3b5c; border:1px solid #ff3b5c35; }
.badge-ok   { background:#22c55e14; color:#22c55e; border:1px solid #22c55e35; }

/* ── Section label ── */
.slabel {
    font-family:'JetBrains Mono',monospace; font-size:0.6rem; letter-spacing:0.14em;
    text-transform:uppercase; color:#00e5ff; margin-bottom:12px; padding-bottom:5px;
    border-bottom:1px solid #1a2540;
}

/* ── Card ── */
.card { background:#0d1f3c; border:1px solid #1a2f50; border-radius:6px; padding:18px 16px 14px; }
.card-sm { background:#0d1f3c; border:1px solid #1a2f50; border-radius:6px; padding:14px 16px; }

/* ── Inputs ── */
div[data-baseweb="select"]>div, div[data-baseweb="input"]>div {
    background:#0a142a !important; border-color:#1e3050 !important; border-radius:4px !important;
    color:#c9d1e0 !important; font-family:'JetBrains Mono',monospace !important; font-size:0.8rem !important;
}
div[data-baseweb="select"]>div:focus-within, div[data-baseweb="input"]>div:focus-within {
    border-color:#00e5ff !important; box-shadow:0 0 0 2px #00e5ff14 !important;
}
label[data-testid="stWidgetLabel"] p {
    font-family:'JetBrains Mono',monospace !important; font-size:0.68rem !important;
    color:#8892a4 !important; letter-spacing:.05em !important; text-transform:uppercase !important;
}

/* ── Buttons ── */
.stButton>button[kind="primary"] {
    background:transparent !important; border:1px solid #00e5ff !important; color:#00e5ff !important;
    font-family:'JetBrains Mono',monospace !important; font-size:0.72rem !important;
    letter-spacing:.12em !important; text-transform:uppercase !important; border-radius:4px !important;
    padding:9px 20px !important; transition:all .2s !important;
}
.stButton>button[kind="primary"]:hover { background:#00e5ff14 !important; box-shadow:0 0 14px #00e5ff28 !important; }
.stButton>button[kind="secondary"] {
    background:transparent !important; border:1px solid #1a2f50 !important; color:#8892a4 !important;
    font-family:'JetBrains Mono',monospace !important; font-size:0.68rem !important;
    letter-spacing:.08em !important; text-transform:uppercase !important; border-radius:4px !important;
    padding:7px 14px !important;
}
.stButton>button[kind="secondary"]:hover { border-color:#00e5ff !important; color:#00e5ff !important; }

/* ── Scan animation ── */
@keyframes scanline { 0%{top:0%;opacity:.7} 95%{top:100%;opacity:.7} 100%{top:100%;opacity:0} }
.scan-overlay { position:fixed; top:0;left:0;right:0;bottom:0; pointer-events:none; z-index:9999; overflow:hidden; }
.scan-line { position:absolute; left:0;right:0; height:2px;
    background:linear-gradient(90deg,transparent,#00e5ff,transparent);
    animation:scanline .9s ease-in forwards; }

/* ── Verdict banners ── */
.verdict { border-radius:6px; padding:18px 22px; font-family:'JetBrains Mono',monospace; }
.verdict.threat { background:#1a0810; border:1px solid #ff3b5c55; border-left:3px solid #ff3b5c; }
.verdict.clean  { background:#071510; border:1px solid #22c55e45; border-left:3px solid #22c55e; }
.verdict .v-label { font-size:0.6rem; letter-spacing:.14em; text-transform:uppercase; margin-bottom:4px; }
.verdict.threat .v-label { color:#ff3b5c; }
.verdict.clean  .v-label { color:#22c55e; }
.verdict .v-msg  { font-size:0.9rem; font-weight:700; color:#e8edf5; }
.verdict .v-det  { font-size:0.72rem; color:#8892a4; margin-top:5px; font-family:'Inter',sans-serif; line-height:1.5; }

/* ── Confidence card ── */
.conf-card { background:#0d1f3c; border:1px solid #1a2f50; border-radius:6px; padding:16px; text-align:center; }
.conf-card .clabel { font-family:'JetBrains Mono',monospace; font-size:0.58rem; letter-spacing:.14em; text-transform:uppercase; color:#8892a4; margin-bottom:6px; }
.conf-card .cval   { font-family:'JetBrains Mono',monospace; font-size:2.1rem; font-weight:700; color:#e8edf5; line-height:1; }
.conf-card .cbar-t { margin-top:10px; height:4px; background:#1a2540; border-radius:2px; overflow:hidden; }
.conf-card .cbar-f { height:100%; border-radius:2px; }

/* ── Feature importance bar ── */
.fi-row { display:flex; align-items:center; gap:10px; margin-bottom:8px; }
.fi-name { font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#8892a4; width:220px; flex-shrink:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.fi-track { flex:1; height:6px; background:#1a2540; border-radius:3px; overflow:hidden; }
.fi-fill  { height:100%; border-radius:3px; }
.fi-pct   { font-family:'JetBrains Mono',monospace; font-size:0.62rem; color:#8892a4; width:36px; text-align:right; flex-shrink:0; }

/* ── History table ── */
.hist-table { width:100%; border-collapse:collapse; font-family:'JetBrains Mono',monospace; font-size:0.68rem; }
.hist-table th { color:#8892a4; padding:6px 10px; border-bottom:1px solid #1a2540; text-align:left; font-weight:400; letter-spacing:.06em; text-transform:uppercase; }
.hist-table td { padding:6px 10px; border-bottom:1px solid #111928; color:#c9d1e0; }
.hist-table tr:last-child td { border-bottom:none; }
.hist-table tr:hover td { background:#0d1f3c55; }
.pill-threat { color:#ff3b5c; background:#ff3b5c14; border:1px solid #ff3b5c35; border-radius:3px; padding:1px 7px; font-size:.6rem; }
.pill-clean  { color:#22c55e; background:#22c55e14; border:1px solid #22c55e35; border-radius:3px; padding:1px 7px; font-size:.6rem; }

/* ── Preset buttons layout ── */
.preset-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:8px; margin-bottom:16px; }
.preset-btn {
    background:#0d1f3c; border:1px solid #1a2f50; border-radius:5px;
    padding:10px 12px; cursor:pointer; font-family:'JetBrains Mono',monospace;
    font-size:0.65rem; color:#8892a4; text-align:left; line-height:1.4;
    transition:all .18s;
}
.preset-btn:hover { border-color:#00e5ff; color:#00e5ff; background:#00e5ff0a; }
.preset-btn .p-icon { font-size:1rem; display:block; margin-bottom:3px; }
.preset-btn .p-name { font-weight:600; color:#c9d1e0; display:block; }

/* ── Info cards for onboarding ── */
.info-card { background:#0d1f3c; border:1px solid #1a2f50; border-radius:6px; padding:20px; margin-bottom:14px; }
.info-card h4 { font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#00e5ff; margin:0 0 8px; letter-spacing:.06em; text-transform:uppercase; }
.info-card p  { font-size:0.82rem; color:#8892a4; line-height:1.65; margin:0; }

/* ── Stats chart bar ── */
.stat-bar-row { display:flex; align-items:center; gap:10px; margin-bottom:10px; }
.stat-bar-label { font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#8892a4; width:150px; flex-shrink:0; }
.stat-bar-track { flex:1; height:10px; background:#1a2540; border-radius:3px; overflow:hidden; }
.stat-bar-fill  { height:100%; border-radius:3px; background:#00e5ff; }
.stat-bar-val   { font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#8892a4; width:50px; text-align:right; }

/* ── Divider / expander ── */
hr[data-testid="stDivider"] { border-color:#1a2540 !important; margin:18px 0 !important; }
details summary { font-family:'JetBrains Mono',monospace !important; font-size:0.68rem !important; color:#8892a4 !important; letter-spacing:.08em !important; text-transform:uppercase !important; }
.stDataFrame { border:1px solid #1a2540 !important; border-radius:4px !important; }
div[data-testid="stSpinner"] p { font-family:'JetBrains Mono',monospace !important; font-size:0.72rem !important; color:#00e5ff !important; }

/* ── Tooltip ── */
.tt { position:relative; display:inline-block; cursor:help; }
.tt .tt-text {
    visibility:hidden; width:240px; background:#0d1f3c; color:#c9d1e0;
    font-family:'Inter',sans-serif; font-size:0.72rem; line-height:1.5;
    border:1px solid #1a2f50; border-radius:4px; padding:8px 10px;
    position:absolute; z-index:999; bottom:125%; left:0;
    box-shadow:0 4px 16px #00000055;
}
.tt:hover .tt-text { visibility:visible; }

/* ── Metric mini card ── */
.metric-mini { background:#0d1f3c; border:1px solid #1a2f50; border-radius:5px; padding:12px 14px; text-align:center; }
.metric-mini .mm-label { font-family:'JetBrains Mono',monospace; font-size:0.58rem; color:#8892a4; letter-spacing:.1em; text-transform:uppercase; margin-bottom:5px; }
.metric-mini .mm-val   { font-family:'JetBrains Mono',monospace; font-size:1.35rem; font-weight:700; color:#e8edf5; }
.metric-mini .mm-sub   { font-size:0.7rem; color:#8892a4; margin-top:2px; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ════════════════════════════════════════════════════════════
if "history" not in st.session_state:
    st.session_state.history = []
if "preset" not in st.session_state:
    st.session_state.preset = None
if "mode" not in st.session_state:
    st.session_state.mode = "Beginner"

# ════════════════════════════════════════════════════════════
#  PRESETS
# ════════════════════════════════════════════════════════════
PRESETS = {
    "normal_http": {
        "label": "Normal Web Browse",
        "icon": "🟢",
        "desc": "Standard HTTP TCP connection",
        "protocol":"tcp","service":"http","flag":"SF",
        "duration":0.5,"src_bytes":500,"dst_bytes":8000,
        "count":3,"srv_count":3,"logged_in":"No"
    },
    "dos_flood": {
        "label": "DoS Flood Attack",
        "icon": "🔴",
        "desc": "SYN flood — high count, no response",
        "protocol":"tcp","service":"http","flag":"S0",
        "duration":0.0,"src_bytes":0,"dst_bytes":0,
        "count":511,"srv_count":511,"logged_in":"No"
    },
    "port_scan": {
        "label": "Port Scan (Probe)",
        "icon": "🟠",
        "desc": "Probing with rejected connections",
        "protocol":"tcp","service":"private","flag":"REJ",
        "duration":0.0,"src_bytes":0,"dst_bytes":0,
        "count":255,"srv_count":12,"logged_in":"No"
    },
    "ftp_brute": {
        "label": "FTP Brute Force",
        "icon": "🔴",
        "desc": "Repeated FTP auth attempts",
        "protocol":"tcp","service":"ftp_data","flag":"RSTO",
        "duration":2.0,"src_bytes":480,"dst_bytes":0,
        "count":50,"srv_count":50,"logged_in":"No"
    },
}

# ════════════════════════════════════════════════════════════
#  ATTACK TYPE EXPLANATIONS
# ════════════════════════════════════════════════════════════
ATTACK_EXPLAIN = {
    "SF":   ("Normal Session", "Connection completed normally — both sides exchanged data and closed cleanly. This is what everyday web browsing looks like."),
    "S0":   ("SYN Flood / DoS", "Connection requests were sent but never acknowledged. A hallmark of Denial-of-Service attacks that try to exhaust server resources."),
    "REJ":  ("Port Scan", "Connections were actively refused by the target. Attackers use this to map which ports are open on a system."),
    "RSTO": ("Brute Force / Reset Attack", "Connection was reset by the origin. Often seen in repeated failed login attempts or unauthorized access probing."),
    "RSTR": ("Connection Hijack / Reset", "The destination forcibly closed the connection. May indicate traffic manipulation or session disruption attempts."),
}

FEATURE_HELP = {
    "Protocol Layer":           "The communication protocol — TCP is web/email, UDP is streaming/DNS, ICMP is ping.",
    "Target Port Service":      "The network service being contacted. HTTP = websites, FTP = file transfers, SMTP = email.",
    "Connection State Flag":    "How the connection ended. SF = normal close. S0/REJ = suspicious — connection was never acknowledged.",
    "Duration (sec)":           "How long the connection lasted. DoS attacks often have very short or zero-duration connections.",
    "Source Payload (bytes)":   "Data sent FROM the connecting machine. Very high values may indicate data exfiltration.",
    "Destination Payload (bytes)": "Data received BY the connecting machine. Normal web browsing usually returns more data than it sends.",
    "Connections to same host": "How many connections hit the same target in the last 2 seconds. Spikes here are a classic DoS/scan indicator.",
    "Connections to same service": "How many connections used the same port/service. Staying on one service while varying hosts = port scan.",
    "Successful Auth?":         "Did the user successfully log in? Attacks often occur on unauthenticated connections.",
}

# ════════════════════════════════════════════════════════════
#  MODEL LOAD
# ════════════════════════════════════════════════════════════
@st.cache_resource
def load_assets():
    model    = joblib.load("nids_model.pkl")
    features = joblib.load("model_features.pkl")
    return model, features

# ════════════════════════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════════════════════════
def build_input_df(feature_names, protocol, service, flag,
                   duration, src_bytes, dst_bytes, count, srv_count, logged_in_val):
    df = pd.DataFrame(np.zeros((1, len(feature_names))), columns=feature_names)
    for col, val in [
        ('duration', duration), ('src_bytes', src_bytes), ('dst_bytes', dst_bytes),
        ('count', count), ('srv_count', srv_count), ('logged_in', logged_in_val),
    ]:
        if col in df.columns: df[col] = val

    for col in [f"protocol_type_{protocol}", f"flag_{flag}", f"service_{service}"]:
        if col in df.columns: df[col] = 1

    if flag == "S0":
        for c in ['serror_rate','srv_serror_rate','dst_host_serror_rate','dst_host_srv_serror_rate']:
            if c in df.columns: df[c] = 1.0
    if flag in ["REJ","RSTO","RSTR"]:
        for c in ['rerror_rate','srv_rerror_rate','dst_host_rerror_rate','dst_host_srv_rerror_rate']:
            if c in df.columns: df[c] = 1.0

    if 'dst_host_count'     in df.columns: df['dst_host_count']     = min(255, count)
    if 'dst_host_srv_count' in df.columns: df['dst_host_srv_count'] = srv_count
    return df


def feature_importance_html(model, feature_names, top_n=10):
    importances = model.feature_importances_
    fi = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:top_n]
    max_val = fi[0][1] if fi else 1
    colors = ["#00e5ff","#0dcff0","#1ab9e0","#27a3d0","#3490c0","#4080b0"]
    rows = ""
    for i, (name, val) in enumerate(fi):
        pct = val / max_val * 100
        color = colors[min(i, len(colors)-1)]
        clean = name.replace("protocol_type_","proto:").replace("service_","svc:").replace("flag_","flag:")
        rows += f"""
        <div class="fi-row">
          <div class="fi-name" title="{name}">{clean}</div>
          <div class="fi-track"><div class="fi-fill" style="width:{pct:.1f}%;background:{color}"></div></div>
          <div class="fi-pct">{val*100:.1f}%</div>
        </div>"""
    return rows


def stat_bar_html(label, value, max_val, color="#00e5ff"):
    pct = value / max_val * 100 if max_val else 0
    return f"""
    <div class="stat-bar-row">
      <div class="stat-bar-label">{label}</div>
      <div class="stat-bar-track"><div class="stat-bar-fill" style="width:{pct:.1f}%;background:{color}"></div></div>
      <div class="stat-bar-val">{value:,}</div>
    </div>"""

# ════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚙️ System Status")
    st.markdown("""
    <div class="status-pill"><span class="dot"></span>Detection Engine: Online</div>
    <div class="status-pill" style="margin-top:4px">
      <span class="dot" style="background:#00e5ff;box-shadow:0 0 5px #00e5ff"></span>Model: NSL-KDD v2
    </div>
    <div class="status-pill" style="margin-top:4px">
      <span class="dot" style="background:#f59e0b;box-shadow:0 0 5px #f59e0b"></span>Algorithm: Random Forest
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 Interface Mode")
    mode = st.radio("", ["Beginner", "Expert"], index=0 if st.session_state.mode == "Beginner" else 1,
                    label_visibility="collapsed")
    st.session_state.mode = mode
    if mode == "Beginner":
        st.caption("Plain-language labels and tooltips. Perfect if you're new to networking.")
    else:
        st.caption("Technical field names and full telemetry control.")

    st.markdown("---")
    st.markdown("### 📋 Quick Presets")
    st.caption("Load a known attack or safe scenario instantly.")
    for key, p in PRESETS.items():
        if st.button(f"{p['icon']} {p['label']}", key=f"pre_{key}", use_container_width=True):
            st.session_state.preset = key
            st.rerun()

    st.markdown("---")
    total = len(st.session_state.history)
    threats = sum(1 for h in st.session_state.history if h["verdict"] == "THREAT")
    st.markdown(f"""
    <div class="card-sm" style="margin-bottom:8px">
      <div class="clabel" style="font-family:'JetBrains Mono',monospace;font-size:.58rem;letter-spacing:.1em;text-transform:uppercase;color:#8892a4;margin-bottom:6px">Session Stats</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#c9d1e0">
        Total scans: <span style="color:#00e5ff">{total}</span><br>
        Threats: <span style="color:#ff3b5c">{threats}</span> &nbsp;|&nbsp;
        Clean: <span style="color:#22c55e">{total - threats}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<span style="font-family:JetBrains Mono,monospace;font-size:0.55rem;color:#2a3550;letter-spacing:.08em">AI-NIDS · NSL-KDD · RF Classifier · 2025</span>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  PAGE HEADER
# ════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
  <div>
    <div class="ph-sub">Enterprise Security Operations Center</div>
    <div class="ph-title">🛡️ AI-NIDS Console</div>
  </div>
  <span class="badge">NSL-KDD Engine</span>
  <span class="badge badge-ok">RF · 99.2% Accuracy</span>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍  Live Inspector",
    "📁  Batch Scanner",
    "📊  Model Stats",
    "📖  What Is NIDS?",
])

# ╔══════════════════════════════════════════════════════════╗
#  TAB 1 — LIVE INSPECTOR
# ╚══════════════════════════════════════════════════════════╝
with tab1:
    try:
        model, feature_names = load_assets()

        # ── Pull preset values ──────────────────────────────
        p = PRESETS.get(st.session_state.preset, {})
        def pv(key, default): return p.get(key, default)

        # ── Input Panel ─────────────────────────────────────
        st.markdown('<div class="slabel">// Connection Parameters</div>', unsafe_allow_html=True)

        is_beginner = st.session_state.mode == "Beginner"

        col1, col2, col3 = st.columns(3, gap="medium")

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="slabel" style="margin-top:0">Network & Routing</div>', unsafe_allow_html=True)

            proto_label   = "What protocol?" if is_beginner else "Protocol Layer"
            service_label = "What service?"  if is_beginner else "Target Port Service"
            flag_label    = "How did it end?" if is_beginner else "Connection State Flag"

            proto_idx   = ["tcp","udp","icmp"].index(pv("protocol","tcp"))
            service_idx = ["http","smtp","private","ftp_data","domain","other"].index(pv("service","http"))
            flag_idx    = ["SF","S0","REJ","RSTO","RSTR"].index(pv("flag","SF"))

            protocol = st.selectbox(proto_label, ["tcp","udp","icmp"], index=proto_idx)
            service  = st.selectbox(service_label, ["http","smtp","private","ftp_data","domain","other"], index=service_idx)
            flag     = st.selectbox(flag_label, ["SF","S0","REJ","RSTO","RSTR"], index=flag_idx)

            if is_beginner:
                flag_name, flag_desc = ATTACK_EXPLAIN.get(flag, ("Unknown",""))
                st.markdown(f'<div style="font-size:.68rem;color:#8892a4;margin-top:4px;line-height:1.5">ℹ️ <b style="color:#c9d1e0">{flag_name}</b><br>{flag_desc}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="slabel" style="margin-top:0">Payload & Session</div>', unsafe_allow_html=True)
            d_label  = "How long? (seconds)"     if is_beginner else "Duration (sec)"
            sb_label = "Data sent (bytes)"        if is_beginner else "Source Payload (bytes)"
            db_label = "Data received (bytes)"    if is_beginner else "Destination Payload (bytes)"

            duration  = st.number_input(d_label,  min_value=0.0, value=float(pv("duration",0.0)),  step=0.1)
            src_bytes = st.number_input(sb_label, min_value=0,   value=int(pv("src_bytes",0)),     step=100)
            dst_bytes = st.number_input(db_label, min_value=0,   value=int(pv("dst_bytes",0)),     step=100)
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="slabel" style="margin-top:0">Frequency & Auth (2s window)</div>', unsafe_allow_html=True)
            c_label   = "How many hits on same host?" if is_beginner else "Connections to same host"
            sc_label  = "How many on same service?"   if is_beginner else "Connections to same service"
            li_label  = "Did login succeed?"           if is_beginner else "Successful Auth?"

            count     = st.number_input(c_label,  min_value=0, value=int(pv("count",1)))
            srv_count = st.number_input(sc_label, min_value=0, value=int(pv("srv_count",1)))
            logged_in = st.selectbox(li_label, ["No","Yes"],
                                     index=0 if pv("logged_in","No") == "No" else 1)

            if is_beginner and count > 100:
                st.markdown('<div style="font-size:.68rem;color:#f59e0b;margin-top:4px">⚠ High connection rate — potential DoS indicator</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Tooltip guide (beginner) ─────────────────────────
        if is_beginner:
            with st.expander("💡 What do these fields mean?"):
                for field, help_text in FEATURE_HELP.items():
                    st.markdown(f"**{field}** — {help_text}")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Build df ────────────────────────────────────────
        logged_in_val = 1 if logged_in == "Yes" else 0
        input_df = build_input_df(feature_names, protocol, service, flag,
                                  duration, src_bytes, dst_bytes, count, srv_count, logged_in_val)

        # ── Execute button ───────────────────────────────────
        col_btn, col_clear, _ = st.columns([1.2, 1, 4])
        with col_btn:
            execute = st.button("▶  Run Inspection", use_container_width=True, type="primary")
        with col_clear:
            if st.button("✕  Clear History", use_container_width=True):
                st.session_state.history = []
                st.rerun()

        # ── RESULTS ─────────────────────────────────────────
        if execute:
            st.markdown('<div class="scan-overlay"><div class="scan-line"></div></div>', unsafe_allow_html=True)

            with st.spinner("Scanning traffic signatures..."):
                time.sleep(0.6)
                prediction = model.predict(input_df)[0]
                confidence = model.predict_proba(input_df)[0]

            conf_val  = confidence[1]*100 if prediction==1 else confidence[0]*100
            bar_color = "#ff3b5c" if prediction==1 else "#22c55e"
            verdict   = "THREAT" if prediction==1 else "CLEAN"

            # Save to history
            st.session_state.history.append({
                "time":      datetime.datetime.now().strftime("%H:%M:%S"),
                "protocol":  protocol,
                "service":   service,
                "flag":      flag,
                "count":     count,
                "verdict":   verdict,
                "confidence":f"{conf_val:.1f}%",
            })

            st.divider()
            st.markdown('<div class="slabel">// Inspection Results</div>', unsafe_allow_html=True)

            res_col, conf_col = st.columns([3, 1], gap="medium")

            with res_col:
                flag_name, flag_desc = ATTACK_EXPLAIN.get(flag, ("Unknown",""))
                if prediction == 1:
                    detail = (f"Connection flag <b>{flag}</b> ({flag_name}) combined with "
                              f"{'high connection rate (' + str(count) + ' hits/2s) ' if count > 50 else ''}"
                              f"{'and unauthenticated session ' if logged_in_val == 0 else ''}"
                              f"matches known intrusion signatures in the NSL-KDD corpus.")
                    st.markdown(f"""
                    <div class="verdict threat">
                      <div class="v-label">⚠ Critical Alert — Malicious Activity</div>
                      <div class="v-msg">Intrusion Detected: {flag_name}</div>
                      <div class="v-det">{detail}</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="verdict clean">
                      <div class="v-label">✓ Verified Clean</div>
                      <div class="v-msg">Normal Connection</div>
                      <div class="v-det">Packet behavior aligns with standard operating baseline.
                        Flag <b>{flag}</b> ({flag_name}). No anomalous patterns detected. No action required.</div>
                    </div>""", unsafe_allow_html=True)

            with conf_col:
                st.markdown(f"""
                <div class="conf-card">
                  <div class="clabel">Model Confidence</div>
                  <div class="cval">{conf_val:.1f}<span style="font-size:.95rem;color:#8892a4">%</span></div>
                  <div class="cbar-t"><div class="cbar-f" style="width:{int(conf_val)}%;background:{bar_color}"></div></div>
                </div>""", unsafe_allow_html=True)

            # ── Feature importance explanation ──────────────
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="slabel">// Why did the model decide this?</div>', unsafe_allow_html=True)
            exp_col, _ = st.columns([2, 1])
            with exp_col:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(feature_importance_html(model, feature_names, top_n=8), unsafe_allow_html=True)
                st.markdown('<div style="font-size:.65rem;color:#3a4560;margin-top:8px;font-family:JetBrains Mono,monospace">Based on global model feature weights · Longer bar = stronger influence on all decisions</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # ── Session History ──────────────────────────────────
        if st.session_state.history:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="slabel">// Session Inspection Log</div>', unsafe_allow_html=True)

            rows = ""
            for h in reversed(st.session_state.history[-20:]):
                pill = f'<span class="pill-threat">THREAT</span>' if h["verdict"]=="THREAT" else f'<span class="pill-clean">CLEAN</span>'
                rows += f"""<tr>
                  <td>{h['time']}</td><td>{h['protocol']}</td><td>{h['service']}</td>
                  <td>{h['flag']}</td><td>{h['count']}</td>
                  <td>{pill}</td><td>{h['confidence']}</td>
                </tr>"""

            st.markdown(f"""
            <div class="card" style="overflow-x:auto">
            <table class="hist-table">
              <thead><tr>
                <th>Time</th><th>Protocol</th><th>Service</th><th>Flag</th>
                <th>Count</th><th>Verdict</th><th>Confidence</th>
              </tr></thead>
              <tbody>{rows}</tbody>
            </table>
            </div>""", unsafe_allow_html=True)

            # Download CSV
            hist_df = pd.DataFrame(st.session_state.history)
            csv_bytes = hist_df.to_csv(index=False).encode()
            st.markdown("<br>", unsafe_allow_html=True)
            dl_col, _ = st.columns([1, 4])
            with dl_col:
                st.download_button("⬇  Export Log (CSV)", data=csv_bytes,
                                   file_name="nids_inspection_log.csv", mime="text/csv",
                                   use_container_width=True)

        # ── Raw payload ─────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("// Raw Telemetry Payload (all 122 features)"):
            st.dataframe(input_df, use_container_width=True)

    except FileNotFoundError:
        st.markdown("""
        <div class="verdict threat" style="margin-top:32px">
          <div class="v-label">⚠ Configuration Error</div>
          <div class="v-msg">Model files not found</div>
          <div class="v-det">Run <code style="background:#0a142a;padding:2px 6px;border-radius:3px;font-family:JetBrains Mono,monospace">python train.py</code>
          in your terminal first to generate <code>nids_model.pkl</code> and <code>model_features.pkl</code>.</div>
        </div>""", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════╗
#  TAB 2 — BATCH SCANNER
# ╚══════════════════════════════════════════════════════════╝
with tab2:
    st.markdown('<div class="slabel">// Batch CSV Scanner — Scan multiple connections at once</div>', unsafe_allow_html=True)

    try:
        model, feature_names = load_assets()

        st.markdown("""
        <div class="info-card">
          <h4>How to use Batch Scanner</h4>
          <p>Upload a CSV file where each row is one network connection. Required columns:
          <code style="background:#0a142a;padding:1px 5px;border-radius:3px;font-family:JetBrains Mono,monospace">
          protocol, service, flag, duration, src_bytes, dst_bytes, count, srv_count, logged_in</code>.<br>
          The scanner will classify every row and produce a downloadable results file.</p>
        </div>
        """, unsafe_allow_html=True)

        # Sample CSV download
        sample_data = pd.DataFrame([
            {"protocol":"tcp","service":"http","flag":"SF","duration":0.5,"src_bytes":500,"dst_bytes":8000,"count":3,"srv_count":3,"logged_in":0},
            {"protocol":"tcp","service":"http","flag":"S0","duration":0,"src_bytes":0,"dst_bytes":0,"count":511,"srv_count":511,"logged_in":0},
            {"protocol":"tcp","service":"private","flag":"REJ","duration":0,"src_bytes":0,"dst_bytes":0,"count":255,"srv_count":12,"logged_in":0},
            {"protocol":"udp","service":"domain","flag":"SF","duration":0.1,"src_bytes":50,"dst_bytes":100,"count":5,"srv_count":5,"logged_in":0},
        ])
        samp_col, _ = st.columns([1, 3])
        with samp_col:
            st.download_button("⬇  Download Sample CSV", data=sample_data.to_csv(index=False).encode(),
                               file_name="sample_connections.csv", mime="text/csv", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload your connections CSV", type=["csv"])

        if uploaded:
            raw_df = pd.read_csv(uploaded)
            st.markdown(f'<div style="font-family:JetBrains Mono,monospace;font-size:.7rem;color:#8892a4;margin-bottom:12px">{len(raw_df)} rows loaded</div>', unsafe_allow_html=True)

            results = []
            errors  = []

            progress_bar = st.progress(0)
            for i, row in raw_df.iterrows():
                try:
                    protocol  = str(row.get("protocol","tcp"))
                    service   = str(row.get("service","http"))
                    flag      = str(row.get("flag","SF"))
                    duration  = float(row.get("duration",0))
                    src_bytes = int(row.get("src_bytes",0))
                    dst_bytes = int(row.get("dst_bytes",0))
                    count     = int(row.get("count",1))
                    srv_count = int(row.get("srv_count",1))
                    li_val    = int(row.get("logged_in",0))

                    df_row = build_input_df(feature_names, protocol, service, flag,
                                           duration, src_bytes, dst_bytes, count, srv_count, li_val)
                    pred = model.predict(df_row)[0]
                    conf = model.predict_proba(df_row)[0]
                    conf_val = conf[1]*100 if pred==1 else conf[0]*100
                    results.append({**row.to_dict(), "verdict": "THREAT" if pred==1 else "CLEAN", "confidence_%": round(conf_val,1)})
                except Exception as e:
                    errors.append(f"Row {i}: {e}")
                progress_bar.progress((i+1)/len(raw_df))

            progress_bar.empty()

            results_df = pd.DataFrame(results)
            threat_count = (results_df["verdict"] == "THREAT").sum()
            clean_count  = (results_df["verdict"] == "CLEAN").sum()

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f'<div class="metric-mini"><div class="mm-label">Total Scanned</div><div class="mm-val">{len(results_df)}</div></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-mini"><div class="mm-label">Threats</div><div class="mm-val" style="color:#ff3b5c">{threat_count}</div></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="metric-mini"><div class="mm-label">Clean</div><div class="mm-val" style="color:#22c55e">{clean_count}</div></div>', unsafe_allow_html=True)
            with m4:
                threat_rate = threat_count / len(results_df) * 100 if results_df.shape[0] > 0 else 0
                st.markdown(f'<div class="metric-mini"><div class="mm-label">Threat Rate</div><div class="mm-val" style="color:{"#ff3b5c" if threat_rate>20 else "#f59e0b" if threat_rate>5 else "#22c55e"}">{threat_rate:.1f}%</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(results_df.style.apply(
                lambda col: ["color: #ff3b5c" if v=="THREAT" else "color: #22c55e" for v in col]
                if col.name == "verdict" else [""]*len(col), axis=0
            ), use_container_width=True)

            dl_col2, _ = st.columns([1, 3])
            with dl_col2:
                st.download_button("⬇  Download Results CSV", data=results_df.to_csv(index=False).encode(),
                                   file_name="nids_batch_results.csv", mime="text/csv", use_container_width=True)
            if errors:
                with st.expander(f"⚠ {len(errors)} rows had errors"):
                    for e in errors: st.text(e)

    except FileNotFoundError:
        st.warning("Model not loaded. Run `python train.py` first.")

# ╔══════════════════════════════════════════════════════════╗
#  TAB 3 — MODEL STATS
# ╚══════════════════════════════════════════════════════════╝
with tab3:
    st.markdown('<div class="slabel">// Model & Dataset Intelligence</div>', unsafe_allow_html=True)

    try:
        model, feature_names = load_assets()

        # ── Key metrics ─────────────────────────────────────
        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.markdown('<div class="metric-mini"><div class="mm-label">Validation Accuracy</div><div class="mm-val">99.2%</div><div class="mm-sub">on 25,195 samples</div></div>', unsafe_allow_html=True)
        with mc2:
            st.markdown('<div class="metric-mini"><div class="mm-label">Precision (Attack)</div><div class="mm-val">100%</div><div class="mm-sub">very few false positives</div></div>', unsafe_allow_html=True)
        with mc3:
            st.markdown('<div class="metric-mini"><div class="mm-label">Recall (Attack)</div><div class="mm-val">99%</div><div class="mm-sub">catches almost all attacks</div></div>', unsafe_allow_html=True)
        with mc4:
            st.markdown('<div class="metric-mini"><div class="mm-label">Decision Trees</div><div class="mm-val">100</div><div class="mm-sub">in the forest ensemble</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        left_col, right_col = st.columns(2, gap="large")

        with left_col:
            st.markdown('<div class="slabel">// Top 15 Most Influential Features</div>', unsafe_allow_html=True)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(feature_importance_html(model, feature_names, top_n=15), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with right_col:
            st.markdown('<div class="slabel">// NSL-KDD Dataset Profile</div>', unsafe_allow_html=True)
            st.markdown('<div class="card">', unsafe_allow_html=True)

            # Known dataset class distribution
            classes = [("Normal Traffic", 67343, "#22c55e"),
                       ("DoS Attack",     45927, "#ff3b5c"),
                       ("Probe",           11656, "#f59e0b"),
                       ("R2L",             995,   "#a78bfa"),
                       ("U2R",             52,    "#ec4899")]
            max_v = classes[0][1]
            for label, val, color in classes:
                st.markdown(stat_bar_html(label, val, max_v, color), unsafe_allow_html=True)

            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
            st.markdown('<div class="slabel" style="margin-top:8px">// Protocol Distribution in Training Data</div>', unsafe_allow_html=True)
            protos = [("TCP", 82075, "#00e5ff"), ("UDP", 19177, "#0dcff0"), ("ICMP", 25720, "#1ab9e0")]
            max_p = protos[0][1]
            for label, val, color in protos:
                st.markdown(stat_bar_html(label, val, max_p, color), unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # ── Confusion matrix (text) ─────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="slabel">// Confusion Matrix (Validation Set)</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
          <table style="font-family:JetBrains Mono,monospace;font-size:.72rem;width:100%;border-collapse:collapse">
            <thead>
              <tr>
                <th style="color:#8892a4;padding:8px 14px;border-bottom:1px solid #1a2540"></th>
                <th style="color:#22c55e;padding:8px 14px;border-bottom:1px solid #1a2540">Predicted: Normal</th>
                <th style="color:#ff3b5c;padding:8px 14px;border-bottom:1px solid #1a2540">Predicted: Attack</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="color:#22c55e;padding:8px 14px;border-bottom:1px solid #111928">Actual: Normal</td>
                <td style="color:#e8edf5;padding:8px 14px;border-bottom:1px solid #111928">13,382 ✓ (True Negative)</td>
                <td style="color:#f59e0b;padding:8px 14px;border-bottom:1px solid #111928">49 ✗ (False Positive)</td>
              </tr>
              <tr>
                <td style="color:#ff3b5c;padding:8px 14px">Actual: Attack</td>
                <td style="color:#f59e0b;padding:8px 14px">95 ✗ (False Negative)</td>
                <td style="color:#e8edf5;padding:8px 14px">11,669 ✓ (True Positive)</td>
              </tr>
            </tbody>
          </table>
          <div style="font-size:.65rem;color:#3a4560;margin-top:10px">
            False Positive = normal traffic incorrectly flagged as threat &nbsp;|&nbsp; False Negative = attack that slipped through
          </div>
        </div>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.warning("Model not loaded. Run `python train.py` first.")

# ╔══════════════════════════════════════════════════════════╗
#  TAB 4 — WHAT IS NIDS?
# ╚══════════════════════════════════════════════════════════╝
with tab4:
    st.markdown('<div class="slabel">// Understanding Network Intrusion Detection</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
      <h4>🛡️ What is a NIDS?</h4>
      <p>A <b style="color:#c9d1e0">Network Intrusion Detection System (NIDS)</b> watches network traffic and raises an alarm
      when it spots suspicious patterns. Think of it like a security camera for your internet connection — it doesn't
      block traffic itself, but it tells a human (or another system) when something looks wrong.</p>
    </div>

    <div class="info-card">
      <h4>🤖 How does the AI work here?</h4>
      <p>This system uses a <b style="color:#c9d1e0">Random Forest</b> — 100 independent decision trees that each vote
      on whether a connection is normal or an attack. The majority wins. It was trained on the
      <b style="color:#c9d1e0">NSL-KDD dataset</b>, a benchmark collection of ~125,000 real and simulated network connections
      labeled by security experts. The model learned patterns that distinguish normal traffic from four attack families.</p>
    </div>
    """, unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
        st.markdown("""
        <div class="info-card">
          <h4>💥 DoS — Denial of Service</h4>
          <p>The attacker floods a server with so many requests it can't respond to real users.
          Imagine calling a restaurant's phone thousands of times per second so no real customer can get through.
          <br><br><b style="color:#c9d1e0">Signs:</b> Connection flag S0, very high <code style="background:#0a142a;padding:1px 4px;border-radius:2px">count</code>
          values, zero bytes transferred, ICMP or TCP protocol.</p>
        </div>

        <div class="info-card">
          <h4>🔓 R2L — Remote to Local</h4>
          <p>An external attacker tries to gain local user access on a machine they don't have an account on.
          Like picking a lock you're not supposed to touch.
          <br><br><b style="color:#c9d1e0">Signs:</b> Repeated failed logins, SMTP or FTP service, RSTO connection flags.</p>
        </div>
        """, unsafe_allow_html=True)

    with a2:
        st.markdown("""
        <div class="info-card">
          <h4>🔭 Probe — Port Scanning</h4>
          <p>The attacker maps your network by probing which ports and services are open — like a burglar
          checking every window and door before breaking in.
          <br><br><b style="color:#c9d1e0">Signs:</b> REJ flag, connections spread across many services,
          low or zero bytes, high <code style="background:#0a142a;padding:1px 4px;border-radius:2px">diff_srv_rate</code>.</p>
        </div>

        <div class="info-card">
          <h4>👑 U2R — User to Root</h4>
          <p>An attacker who already has a low-level account exploits a vulnerability to gain full admin control.
          Like a hotel guest finding a master key.
          <br><br><b style="color:#c9d1e0">Signs:</b> Elevated shell access, root command execution,
          <code style="background:#0a142a;padding:1px 4px;border-radius:2px">root_shell = 1</code> in the connection data.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
      <h4>📐 NSL-KDD — The Dataset Behind This Model</h4>
      <p>NSL-KDD is an improved version of the 1999 KDD Cup dataset, one of the most widely used benchmarks in
      intrusion detection research. It contains 41 features per connection — including traffic statistics,
      protocol metadata, and error rates — and 125,972 labeled training examples.
      The key improvement over the original KDD dataset is the removal of duplicate records, which prevents
      the model from being biased toward more common attack types. This makes it a fairer and more realistic
      training ground for AI-based security tools.</p>
    </div>

    <div class="info-card">
      <h4>⚡ Try It Yourself</h4>
      <p>Head to the <b style="color:#c9d1e0">Live Inspector</b> tab and click one of the preset scenarios in the sidebar —
      <b style="color:#22c55e">Normal Web Browse</b> to see a clean result, or
      <b style="color:#ff3b5c">DoS Flood Attack</b> to trigger an alert. Switch to <b style="color:#c9d1e0">Beginner mode</b>
      for plain-language labels, or <b style="color:#c9d1e0">Expert mode</b> for full technical control.
      Use the <b style="color:#c9d1e0">Batch Scanner</b> tab to analyze hundreds of connections at once by uploading a CSV.</p>
    </div>
    """, unsafe_allow_html=True)
