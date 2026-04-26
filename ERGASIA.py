import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- SETTINGS & PRO LOOK ---
st.set_page_config(page_title="AI Coaching Nexus v3.0", layout="wide", page_icon="💎")

st.title("💎 AI Coaching Nexus: The Manager's OS")
st.markdown("Σύστημα Τεχνητής Νοημοσύνης για την Ανάπτυξη Ανθρώπινου Δυναμικού & Ανάλυση KPIs.")

# --- SIDEBAR: ENTERPRISE FLEET MANAGEMENT ---
st.sidebar.header("🚀 Enterprise Fleet")
account = st.sidebar.selectbox("Global Account", ["Apple Support", "Google Ads", "Amazon Logistics", "Netflix CS", "Airbnb Experiences"])
site = st.sidebar.radio("Site Location", ["Thessaloniki, Greece", "Athens, Greece", "Lisbon, Portugal", "Cairo, Egypt", "Remote / Cloud"], horizontal=False)

# Δυναμική επιλογή έτους χωρίς όριο
current_year = datetime.date.today().year
year_range = list(range(current_year - 5, current_year + 20))
sel_year = st.sidebar.selectbox("Fiscal Year", year_range, index=5)
sel_month = st.sidebar.selectbox("Fiscal Month", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

st.sidebar.markdown("---")
st.sidebar.header("🎯 Target Overrides")
target_csat = st.sidebar.slider("Target CSAT", 70, 100, 88)
target_qa = st.sidebar.slider("Target QA Score", 80, 100, 92)
target_aht = st.sidebar.number_input("AHT Threshold (s)", value=280)

# --- AGENT COMMAND CENTER ---
st.header("🏁 Agent Command Center")
c1, c2, c3 = st.columns([1, 2, 2])

with c1:
    photo = st.file_uploader("Agent Image", type=['png', 'jpg'])
    if photo: st.image(photo, width=160)
    else: st.warning("👤 Avatar Missing")

with c2:
    a_name = st.text_input("Agent Identity", "Nick Kalas")
    contract = st.selectbox("Contract Type", ["Permanent Full-Time", "Fixed Term", "Freelance B2B", "Part-Time Scholar"])
    mood = st.select_slider("Agent Sentiment (Vibe)", options=["🔴 Frustrated", "🟠 Bored", "🟡 Neutral", "🟢 Motivated", "🔥 Rockstar"])

with c3:
    skills = st.multiselect("Active Skillsets", ["Voice", "Chat", "Email", "Social Media", "Backoffice", "Escalations"], default=["Voice", "Chat"])
    performance_tag = st.select_slider("Performance Tier", options=["Underperformer", "Consistent", "High Flyer", "Potential SME"])

st.markdown("---")

# --- CORE FUNCTIONALITY TABS ---
t1, t2, t3, t4, t5 = st.tabs(["📊 KPI Matrix", "📈 Insight Dashboard", "🧠 Root Cause (5 Whys)", "🎯 SMART Strategy", "📋 Export & Summary"])

# TAB 1: KPI MATRIX
with t1:
    st.subheader("Weekly Performance Injection")
    weeks = ["W1", "W2", "W3", "W4"]
    w_data = {}
    cols = st.columns(4)
    for i, w in enumerate(weeks):
        with cols[i]:
            st.info(f"📅 **{w} Metrics**")
            csat = st.number_input(f"CSAT", key=f"c{i}", value=85.0)
            qa = st.number_input(f"QA", key=f"q{i}", value=90.0)
            aht = st.number_input(f"AHT", key=f"a{i}", value=290.0)
            adh = st.number_input(f"Adherence", key=f"ad{i}", value=96.0)
            w_data[w] = [csat, qa, aht, adh]
    
    df = pd.DataFrame(w_data, index=["CSAT", "QA", "AHT", "Adherence"])
    df['MTD Avg'] = df.mean(axis=1)

# TAB 2: INSIGHTS
with t2:
    st.subheader("Visual Analytics")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("CSAT MTD", f"{df.loc['CSAT', 'MTD Avg']:.1f}%", f"{df.loc['CSAT', 'MTD Avg']-target_csat:.1f}%")
    col_m2.metric("QA MTD", f"{df.loc['QA', 'MTD Avg']:.1f}%", f"{df.loc['QA', 'MTD Avg']-target_qa:.1f}%")
    col_m3.metric("AHT MTD", f"{df.loc['AHT', 'MTD Avg']:.0f}s", f"{target_aht-df.loc['AHT', 'MTD Avg']:.0f}s", delta_color="inverse")
    col_m4.metric("Adherence", f"{df.loc['Adherence', 'MTD Avg']:.1f}%", "Target: 95%")

    viz_type = st.radio("Analytics View", ["Trend Analysis", "KPI Distribution (Radar)", "Weekly Breakdown (Bar)"], horizontal=True)
    
    if viz_type == "Trend Analysis":
        fig = px.line(df.drop(columns='MTD Avg').T, title="Performance Over Time", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    elif viz_type == "KPI Distribution (Radar)":
        radar_df = df[['MTD Avg']].reset_index()
        fig = px.line_polar(radar_df, r='MTD Avg', theta='index', line_close=True, title="Skill DNA Chart")
        fig.update_traces(fill='toself')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.bar(df.drop(columns='MTD Avg').T, barmode='group', title="Weekly KPI Comparison")
        st.plotly_chart(fig, use_container_width=True)

# TAB 3: COMPLEX ROOT CAUSE
with t3:
    st.subheader("🧠 Deep Psychology: Root Cause Analysis")
    
    cause_col1, cause_col2 = st.columns(2)
    with cause_col1:
        st.markdown("**1. Psychological & Skill Gaps**")
        category = st.selectbox("Issue Category", ["Motivation / Disengagement", "Process Complexity", "Tool/System Latency", "External/Personal Factors"])
        
        causes = {
            "Motivation / Disengagement": ["Lack of Recognition", "Repetitive Tasks (Boredom)", "Toxic Peer Interaction", "Quiet Quitting Vibe", "Career Stagnation"],
            "Process Complexity": ["Recent Policy Change", "Complex Refund Rules", "Bilingual Switching Stress", "Knowledge Base (KB) Confusion"],
            "Tool/System Latency": ["Slow VPN (WFH)", "CRM Freezing", "Too many open tabs", "Headset Issues"],
            "External/Personal Factors": ["Home Distractions", "Financial Stress", "Health/Fatigue", "Schedule Conflict"]
        }
        specific = st.selectbox("Deep Cause", causes[category])

    with cause_col2:
        st.markdown("**2. The 5 Whys (BPO Standard)**")
        y1 = st.text_input("Why #1", placeholder="High AHT in W2")
        y2 = st.text_input("Why #2", placeholder="Agent spending too long on KB")
        y3 = st.text_input("Why #3", placeholder="Agent can't find the new promo article")
        y4 = st.text_input("Why #4", placeholder="Agent forgot the keywords for the search")
        y5 = st.error(f"**Root Cause Found:** {st.text_input('Why #5 (The Root)', placeholder='Lack of recurring training on KB search filters')}")

# TAB 4: SMART STRATEGY
with t4:
    st.subheader("🎯 SMART Goal Architecture")
    sg1, sg2 = st.columns(2)
    with sg1:
        spec = st.text_input("Specific Goal", "Increase QA by focusing on Verification steps")
        meas = st.text_input("Measurement (KPI)", "QA Score > 93%")
        ach = st.text_input("Achievable Steps", "Daily 10min review of 'Verification Article'")
    with sg2:
        rel = st.text_input("Relevance", "Crucial for Data Security compliance")
        dead = st.date_input("Review Deadline", datetime.date.today() + datetime.timedelta(days=14))
    
    if st.button("🏗️ Build SMART Strategy"):
        st.success(f"Strategy Locked: {a_name} will achieve {spec} by {dead}.")

# TAB 5: EXPORT & SUMMARY
with t5:
    st.subheader("📋 Session Summary for PowerPoint")
    st.markdown(f"**Manager Summary Report**")
    st.write(f"* **Agent:** {a_name} ({account})")
    st.write(f"* **Site:** {site}")
    st.write(f"* **Month:** {sel_month} {sel_year}")
    st.write(f"* **Main Issue:** {category} - {specific}")
    st.write(f"* **Coaching Recommendation:** {spec}")
    
    if st.button("✅ Sign & Export to CSV"):
        st.balloons()
        st.success("Session Data Ready for Presentation!")