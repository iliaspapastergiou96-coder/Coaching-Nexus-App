import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- CONFIG & SYSTEM MEMORY ---
st.set_page_config(page_title="Nexus Pro v13 Ultimate", layout="wide", page_icon="💎")

if 'coaching_history' not in st.session_state: st.session_state['coaching_history'] = []
if 'custom_roots' not in st.session_state: 
    st.session_state['custom_roots'] = [
        "Product Knowledge (Έλλειψη Γνώσης)", "System Latency (Αργά Εργαλεία)", 
        "Burnout / Mental Fatigue", "Process Confusion", "AHT Pressure (Πίεση Χρόνου)", 
        "Lack of Empathy", "Missed Security Verification (Fatal QA)", "Distractions at Home (WFH)"
    ]
if 'custom_actions' not in st.session_state: 
    st.session_state['custom_actions'] = [
        "Side-by-Side Shadowing", "Roleplay Scenario", "Review Knowledge Base", 
        "Listen to 'Golden Calls'", "Daily 10-min Sync", "Assign Peer Mentor", 
        "Soft Skills Workshop"
    ]

# --- 4-LANGUAGE DICTIONARY ---
lang_dict = {
    "Ελληνικά 🇬🇷": {
        "title": "💎 Nexus Pro: Σύστημα Διοίκησης & Coaching",
        "settings": "🏢 Ρυθμίσεις & Τοποθεσία", "time": "📅 Χρόνος", "targets": "🎯 Στόχοι",
        "hierarchy": "👥 0. Διοικητική Ομάδα (Leadership)", "exp1": "👤 1. Προφίλ, Εμπειρία & Ψυχολογία",
        "exp2": "🌟 2. Φιλοδοξίες & Κίνητρα", "exp3": "🎧 3. Αξιολόγηση Ποιότητας (QA)",
        "tab1": "📊 Βαθμολογίες & Γραφήματα", "tab2": "🧠 Root Causes (5 Whys)", "tab3": "🎯 Στόχοι SMART", 
        "tab4": "⚠️ Πειθαρχικά", "tab5": "🗂️ Ιστορικό & Εξαγωγή", "save": "💾 ΑΠΟΘΗΚΕΥΣΗ & ΟΛΟΚΛΗΡΩΣΗ"
    },
    "English 🇬🇧": {
        "title": "💎 Nexus Pro: Management & Coaching OS",
        "settings": "🏢 Settings & Location", "time": "📅 Time", "targets": "🎯 Targets",
        "hierarchy": "👥 0. Leadership Hierarchy", "exp1": "👤 1. Profile, Tenure & Psychology",
        "exp2": "🌟 2. Aspirations & Motivation", "exp3": "🎧 3. Quality Assurance (QA)",
        "tab1": "📊 Charts & KPIs", "tab2": "🧠 Root Causes", "tab3": "🎯 SMART Goals", 
        "tab4": "⚠️ Disciplinary", "tab5": "🗂️ History & Export", "save": "💾 SAVE & FINALIZE"
    },
    "Deutsch 🇩🇪": {
        "title": "💎 Nexus Pro: Management System",
        "settings": "🏢 Einstellungen", "time": "📅 Zeit", "targets": "🎯 Ziele",
        "hierarchy": "👥 0. Führungsebene", "exp1": "👤 1. Profil & Psychologie",
        "exp2": "🌟 2. Motivation", "exp3": "🎧 3. Qualitätsbewertung (QA)",
        "tab1": "📊 KPI-Werte", "tab2": "🧠 Ursachen", "tab3": "🎯 SMART-Ziele", 
        "tab4": "⚠️ Disziplinarisch", "tab5": "🗂️ Verlauf & Export", "save": "💾 SPEICHERN"
    },
    "Svenska 🇸🇪": {
        "title": "💎 Nexus Pro: Ledningssystem",
        "settings": "🏢 Inställningar", "time": "📅 Tid", "targets": "🎯 Mål",
        "hierarchy": "👥 0. Ledarskap", "exp1": "👤 1. Profil & Personlighet",
        "exp2": "🌟 2. Ambitioner", "exp3": "🎧 3. Kvalitetsutvärdering (QA)",
        "tab1": "📊 KPI Värden", "tab2": "🧠 Grundorsaker", "tab3": "🎯 SMART Mål", 
        "tab4": "⚠️ Disciplinär", "tab5": "🗂️ Historik & Export", "save": "💾 SPARA"
    }
}

# --- SIDEBAR ---
lang_choice = st.sidebar.radio("🌍 UI Language", ["Ελληνικά 🇬🇷", "English 🇬🇧", "Deutsch 🇩🇪", "Svenska 🇸🇪"], horizontal=True)
t = lang_dict[lang_choice]

st.sidebar.markdown("---")
st.sidebar.header(t["settings"])
project = st.sidebar.selectbox("Campaign", ["Booking.com", "Apple Support", "Google", "Netflix"])
site = st.sidebar.selectbox("Location", ["Thessaloniki", "Athens", "Cairo", "Lisbon", "Barcelona", "Berlin", "Stockholm"])
work_model = st.sidebar.selectbox("Work Model", ["On-Site", "WFH (Remote)", "Hybrid"])

st.sidebar.markdown("---")
st.sidebar.header(t["time"])
coaching_date = st.sidebar.date_input("Date", datetime.date.today())
quarter = st.sidebar.selectbox("Quarter", ["Q1", "Q2", "Q3", "Q4"])
month = st.sidebar.selectbox("Month", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

st.sidebar.markdown("---")
st.sidebar.header(t["targets"])
t_csat = st.sidebar.slider("Target CSAT %", 70, 100, 85)
t_qa = st.sidebar.slider("Target QA %", 70, 100, 90)
t_aht = st.sidebar.number_input("Target AHT (sec)", value=280)

def get_color(p_str):
    if "Red" in p_str: return "#FF4B4B", "white"
    if "Yellow" in p_str: return "#FFEB3B", "black"
    if "Green" in p_str: return "#4CAF50", "white"
    return "#0083B0", "white"

# --- MAIN UI ---
st.title(t["title"])
st.markdown("##### *AI-Powered Performance Management & Behavioral Coaching*")

# --- 0. LEADERSHIP ---
with st.expander(t["hierarchy"], expanded=False):
    h1, h2, h3 = st.columns(3)
    with h1: coach_name = st.text_input("Coach Name", "Ilias P.")
    with h2: tl_name = st.text_input("Team Leader Name", "")
    with h3: aom_name = st.text_input("AOM Name", "")

# --- 1. AGENT PROFILE & AI MATRIX ---
with st.expander(t["exp1"], expanded=True):
    col1, col2, col3 = st.columns([1, 2, 3])
    with col1: 
        avatar_type = st.radio("Avatar", ["Male", "Female", "Upload"], horizontal=True)
        if avatar_type == "Upload":
            photo = st.file_uploader("", type=['png', 'jpg'])
            if photo: st.image(photo, width=120)
        elif avatar_type == "Female": st.image("https://www.w3schools.com/howto/img_avatar2.png", width=120)
        else: st.image("https://www.w3schools.com/howto/img_avatar.png", width=120)
        
    with col2:
        agent_name = st.text_input("Agent Name", "Nick Kalas")
        tenure = st.select_slider("Agent Tenure (Εμπειρία)", options=["Rookie (0-6m)", "Developing (6-12m)", "Experienced (1-3y)", "Veteran (3y+)"], value="Developing (6-12m)")
        agent_langs = ["Greek", "English", "German", "French", "Spanish", "Italian", "Dutch", "Portuguese", "Swedish", "Norwegian", "Danish", "Polish", "Turkish", "Arabic", "Mandarin", "Japanese", "Russian"]
        agent_lang = st.multiselect("Spoken Languages", agent_langs, default=["Greek", "English"])
        
    with col3:
        p_primary = st.selectbox("🌟 Primary Personality", ["Red (Director)", "Yellow (Inspirer)", "Green (Supporter)", "Blue (Analyst)"])
        p_secondary = st.selectbox("🌓 Secondary Personality", ["Red (Director)", "Yellow (Inspirer)", "Green (Supporter)", "Blue (Analyst)"], index=1)
        
        c_hex_p, font_c_p = get_color(p_primary)
        c_hex_s, font_c_s = get_color(p_secondary)
        
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between;'>
            <div style='width: 48%; padding:10px; border-radius:10px; background-color:{c_hex_p}; color:{font_c_p}; text-align:center;'><b>Primary:</b><br>{p_primary}</div>
            <div style='width: 48%; padding:10px; border-radius:10px; background-color:{c_hex_s}; color:{font_c_s}; text-align:center; opacity: 0.8;'><b>Secondary:</b><br>{p_secondary}</div>
        </div>
        """, unsafe_allow_html=True)

        # AI MATRIX: Χρώμα + Μοντέλο + Εμπειρία!
        fit_msg = ""
        if c_hex_p == "#FF4B4B": fit_msg = f"🔥 [WFH/HYBRID]: Γρήγορα KPIs, πρόσεχε την ποιότητα. Ως {tenure.split()[0]}, δώστου ευθύνες αλλά έλεγχε τα νούμερα." if "WFH" in work_model else f"🔥 [ON-SITE]: Θέλει να ηγείται. Ως {tenure.split()[0]}, πρόσεχε μην φανεί αυταρχικός στους νέους."
        elif c_hex_p == "#FFEB3B": fit_msg = f"⚠️ [WFH]: ΚΙΝΔΥΝΟΣ ΑΠΟΜΟΝΩΣΗΣ. Ως {tenure.split()[0]}, χρειάζεται daily checks με κάμερα." if "WFH" in work_model else f"⭐ [ON-SITE]: Η ψυχή της ομάδας. Ως {tenure.split()[0]}, χρησιμοποίησέ τον για καλό κλίμα αλλά πρόσεχε το AHT."
        elif c_hex_p == "#4CAF50": fit_msg = f"🤝 [WFH]: Silent Burnout risk. Ως {tenure.split()[0]}, δεν θα ζητήσει βοήθεια. Κάνε εσύ την κίνηση." if "WFH" in work_model else f"🤝 [ON-SITE]: Λατρεύει τη σταθερότητα. Ως {tenure.split()[0]}, είναι ο ιδανικός Peer Mentor."
        else: fit_msg = f"❄️ [WFH]: ΤΟ ΑΠΟΛΥΤΟ MATCH. Ως {tenure.split()[0]}, αποδίδει τέλεια στην ησυχία." if "WFH" in work_model else f"❄️ [ON-SITE]: Ενοχλείται από τη φασαρία. Δώσε γραπτό feedback, ειδικά αφού είναι {tenure.split()[0]}."
        st.info(f"🧠 **AI Advanced Matrix (Tenure x Model x Psy):** {fit_msg}")

# --- 2. ASPIRATIONS & 3. QA ---
with st.expander(t["exp2"], expanded=False):
    asp1, asp2, asp3 = st.columns(3)
    with asp1: personal_asp = st.text_area("Personal Aspirations", placeholder="Family, Hobbies, Work-Life balance")
    with asp2: work_asp = st.text_area("Career Aspirations", placeholder="Promotions, Skill development")
    with asp3: coop = st.select_slider("Cooperativeness Level", options=["1/4", "2/4", "3/4", "4/4 (Team Player)"])

with st.expander(t["exp3"], expanded=False):
    qa_col1, qa_col2, qa_col3 = st.columns(3)
    with qa_col1:
        qa_name = st.text_input("QA Coach Name", "Maria S.")
        qa_ticket = st.text_input("Ticket/Call ID", "BKG-98765")
        qa_score = st.number_input("QA Evaluation Score (%)", value=82.0)
    with qa_col2: qa_strengths = st.text_area("🌟 Strengths (What went well)")
    with qa_col3: qa_improvements = st.text_area("⚠️ Areas of Improvement (Fatal / Non-Fatal)")

# --- COACHING TABS ---
st.markdown("### 📋 Coaching Session Execution")
tab1, tab2, tab3, tab4, tab5 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"], t["tab5"]])

# TAB 1: KPIs & CHARTS
with tab1:
    cols = st.columns(4)
    w_data = {}
    for i in range(1, 5):
        with cols[i-1]:
            st.markdown(f"**Week {i}**")
            c = st.number_input(f"CSAT", value=float(t_csat), key=f"c{i}")
            q = st.number_input(f"QA", value=float(t_qa), key=f"q{i}")
            a = st.number_input(f"AHT", value=280.0, key=f"a{i}")
            w_data[f"W{i}"] = [c, q, a]
            
    df = pd.DataFrame(w_data, index=["CSAT", "QA", "AHT"])
    df['MTD'] = df.mean(axis=1)
    
    st.markdown("---")
    c_viz1, c_viz2 = st.columns([1, 2])
    with c_viz1:
        st.markdown("**Target Progress**")
        st.metric("CSAT MTD", f"{df.loc['CSAT', 'MTD']:.1f}%")
        st.progress(min(int(df.loc['CSAT', 'MTD']), 100))
        st.metric("QA MTD", f"{df.loc['QA', 'MTD']:.1f}%")
        st.progress(min(int(df.loc['QA', 'MTD']), 100))
        
    with c_viz2:
        chart_type = st.radio("🎨 Select Chart:", ["Radar (DNA)", "Bar Chart", "Line Chart"], horizontal=True)
        if "Radar" in chart_type:
            fig = px.line_polar(df[['MTD']].reset_index(), r='MTD', theta='index', line_close=True)
            fig.update_traces(fill='toself')
        elif "Bar" in chart_type: fig = px.bar(df.drop(columns='MTD').T, barmode='group')
        else: fig = px.line(df.drop(columns='MTD').T, markers=True)
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: ROOT CAUSES
with tab2:
    issue = st.text_input("Main Issue / Problem Identified")
    w1, w2, w3, w4 = st.text_input("Why 1?"), st.text_input("Why 2?"), st.text_input("Why 3?"), st.text_input("Why 4?")
    st.markdown("---")
    selected_root = st.selectbox("📌 Select Final Root Cause:", ["-- Add New --"] + st.session_state['custom_roots'])
    final_root = st.text_input("Type New Root Cause:") if selected_root == "-- Add New --" else selected_root

# TAB 3: SMART GOALS
with tab3:
    s1, s2 = st.columns(2)
    with s1:
        spec = st.text_input("Specific (What exactly?)")
        meas = st.text_input("Measurable (Which KPI?)")
        selected_action = st.selectbox("🛠️ Select Action Strategy:", ["-- Add New --"] + st.session_state['custom_actions'])
        final_action = st.text_input("Type New Action:") if selected_action == "-- Add New --" else selected_action
    with s2:
        achiev = st.text_input("Achievable (How?)")
        relev = st.text_input("Relevant (Why does it matter?)")
        timel = st.date_input("Deadline / Follow-up Date", datetime.date.today() + datetime.timedelta(days=7))

# TAB 4: DISCIPLINE
with tab4:
    is_outlier = st.toggle("Trigger Disciplinary/Outlier Process")
    action_taken = st.selectbox("Action Required", ["None", "Verbal Warning", "Written Warning (1st)", "Written Warning (Final)", "PIP"]) if is_outlier else "None"
    if is_outlier: st.text_area("HR / Management Notes Justification")

# --- SAVE ---
st.markdown("---")
if st.button(t["save"], use_container_width=True):
    if final_root and final_root != "-- Add New --" and final_root not in st.session_state['custom_roots']: st.session_state['custom_roots'].append(final_root)
    if final_action and final_action != "-- Add New --" and final_action not in st.session_state['custom_actions']: st.session_state['custom_actions'].append(final_action)

    session_data = {
        "Date": coaching_date, "Agent": agent_name, "Coach": coach_name, "Model": work_model, "Tenure": tenure,
        "QA Score": f"{qa_score}%", "CSAT": round(df.loc['CSAT', 'MTD'],1), "Root Cause": final_root, "Action": final_action, "Discipline": action_taken
    }
    st.session_state['coaching_history'].append(session_data)
    st.balloons()
    st.success("Έγινε επιτυχής καταχώρηση στη Βάση Δεδομένων! Το Ιστορικό ανανεώθηκε.")

# TAB 5: HISTORY & EXPORT
with tab5:
    if len(st.session_state['coaching_history']) > 0:
        history_df = pd.DataFrame(st.session_state['coaching_history'])
        st.dataframe(history_df, use_container_width=True)
        
        # EXPORT ΜΕ ΥΠΟΣΤΗΡΙΞΗ ΕΛΛΗΝΙΚΩΝ (utf-8-sig)
        csv = history_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Export Data to Excel (CSV)",
            data=csv,
            file_name=f"Nexus_Coaching_Export_{datetime.date.today()}.csv",
            mime="text/csv",
        )
    else:
        st.info("Δεν υπάρχουν δεδομένα. Κάνε μια αποθήκευση για να εμφανιστεί ο πίνακας και το κουμπί εξαγωγής.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>Developed by Ilias Papastergiou | Nexus Pro Enterprise OS v13.0 Ultimate</p>", unsafe_allow_html=True)