import streamlit as st
import pandas as pd
import time

# Page configs
st.set_page_config(page_title="Classroom Intelligence System", layout="wide")

st.title("📊 Multimodal Attendance & Engagement Agent Dashboard")
st.caption("AI-Powered, Privacy-Preserving Classroom Analytics (Running 100% Offline)")

# Sidebar Session Management
st.sidebar.header("Session Settings")
class_id = st.sidebar.selectbox("Select Class Section", ["CS-401: Senior Capstone", "CS-302: Operating Systems"])
start_btn = st.sidebar.button("Start Intelligent Tracking Session", type="primary")

# Create layout cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Verified Attendance Count", value="1 / 1", delta="100% Present")
with col2:
    st.metric(label="Real-time Engagement Score", value="65.0%", delta="-15.0% Drop", delta_color="inverse")
with col3:
    st.metric(label="Audio Environment Status", value="Ambient / Lecture", delta="Stable Noise Floor")

st.markdown("---")

# Analytics and Recommendations Engine View
st.subheader("🤖 Agent Context-Aware Suggestions")

if start_btn:
    with st.spinner("Analyzing current multimodal metrics feed..."):
        time.sleep(1)
        st.info("**AI Assistant Recommendation:** Attention drop detected during the passive lecturing window. "
                "Action item: Consider introducing a brief peer-to-peer breakout discussion or launch an interactive poll to restabilize focus.")
else:
    st.warning("Click 'Start Intelligent Tracking Session' in the sidebar to stream real-time insights.")

st.markdown("---")
st.subheader("📉 Session Telemetry Timeline")

# Fixed structural chart data using a clean pandas DataFrame format
chart_data = pd.DataFrame({
    "Minutes into Lecture": [0, 10, 20, 30, 40, 50, 60, 70],
    "Engagement Index (%)": [80, 85, 70, 65, 78, 82, 60, 65]
})


st.line_chart(data=chart_data, x="Minutes into Lecture", y="Engagement Index (%)")
