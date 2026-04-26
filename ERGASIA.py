import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- CONFIG & SYSTEM MEMORY ---
st.set_page_config(page_title="Nexus Pro v8.0", layout="wide", page_icon="🌍")

if 'coaching_history' not in st.session_state:
    st.session_state['coaching_history'] = []

# --- MULTI-LANGUAGE DICTIONARY ---
lang_dict = {
    "Ελληνικά 🇬🇷": {
        "title": "💎 Nexus Pro: Σύστημα Διοίκησης & Coaching",
        "settings": "🏢 Ρυθμίσεις Συστήματος", "campaign": "Καμπάνια", "location": "Τοποθεσία", "work_model": "Μοντέλο Εργασίας",
        "time": "📅 Χρόνος & Ημερομηνίες", "date": "Ημερομηνία", "quarter": "Τρίμηνο", "month": "Μήνας", "year": "Έτος",
        "targets": "🎯 Στόχοι KPIs", "target_csat": "Στόχος CSAT %", "target_qa": "Στόχος QA %", "target_aht": "Στόχος AHT (sec)",
        "hierarchy": "👥 0. Διοικητική Ομάδα (Leadership)", "coach": "Όνομα Coach", "tl": "Όνομα Team Leader", "aom": "Όνομα AOM",
        "exp1": "👤 1. Προφίλ & Προσωπικότητα", "exp2": "🌟 2. Φιλοδοξίες & Κίνητρα", "exp3": "🎧 3. Αξιολόγηση Ποιότητας (QA)",
        "avatar": "Επιλογή Avatar", "male": "Άνδρας", "female": "Γυναίκα", "upload": "Ανέβασμα Φωτο",
        "agent_name": "Ονοματεπώνυμο Agent", "work_email": "Εταιρικό Email", "role": "Ρόλος / Θέση", "languages": "Γλώσσες Εργασίας",
        "primary_p": "Κύριος Τύπος", "secondary_p": "Δευτερεύων Τύπος",
        "p_red": "Κόκκινο (Δυναμικός)", "p_yellow": "Κίτρινο (Ενθουσιώδης)", "p_green": "Πράσινο (Υποστηρικτικός)", "p_blue": "Μπλε (Αναλυτικός)",
        "pers_asp": "Προσωπικές Φιλοδοξίες", "work_asp": "Επαγγελματικοί Στόχοι", "coop": "Επίπεδο Συνεργασίας",
        "qa_name": "Όνομα QA Coach", "qa_ticket": "Κωδικός Κλήσης (Ticket ID)", "qa_score": "Βαθμολογία QA (%)",
        "qa_str": "🌟 Δυνατά Σημεία", "qa_imp": "⚠️ Σημεία Βελτίωσης",
        "exec": "### 📋 Εκτέλεση Coaching",
        "tab1": "📊 Βαθμολογίες KPIs", "tab2": "🧠 5 Whys", "tab3": "🎯 Στόχοι SMART", "tab4": "⚠️ Πειθαρχικά", "tab5": "🗂️ Ιστορικό",
        "week": "Εβδομάδα", "issue": "Βασικό Πρόβλημα", "root": "Γιατί 5 (Ρίζα Προβλήματος)",
        "smart_s": "Συγκεκριμένος (S)", "smart_m": "Μετρήσιμος (M)", "smart_a": "Εφικτός (A)", "smart_r": "Σχετικός (R)", "smart_t": "Προθεσμία (T)",
        "outlier": "Ενεργοποίηση Πειθαρχικού", "action": "Ενέργεια", "notes": "Σχόλια Ηγεσίας",
        "save": "💾 ΑΠΟΘΗΚΕΥΣΗ & ΟΛΟΚΛΗΡΩΣΗ", "success": "Το Session αποθηκεύτηκε επιτυχώς!"
    },
    "English 🇬🇧": {
        "title": "💎 Nexus Pro: Management & Coaching OS",
        "settings": "🏢 System Settings", "campaign": "Campaign", "location": "Location", "work_model": "Work Model",
        "time": "📅 Time Management", "date": "Date", "quarter": "Quarter", "month": "Month", "year": "Year",
        "targets": "🎯 Global Targets (KPIs)", "target_csat": "Target CSAT %", "target_qa": "Target QA %", "target_aht": "Target AHT (sec)",
        "hierarchy": "👥 0. Leadership Hierarchy", "coach": "Coach Name", "tl": "Team Leader Name", "aom": "AOM Name",
        "exp1": "👤 1. Profile & Personality", "exp2": "🌟 2. Aspirations & Motivation", "exp3": "🎧 3. Quality Assurance (QA)",
        "avatar": "Avatar Source", "male": "Male", "female": "Female", "upload": "Upload Photo",
        "agent_name": "Agent Full Name", "work_email": "Work Email", "role": "Role", "languages": "Working Languages",
        "primary_p": "Primary Type", "secondary_p": "Secondary Type",
        "p_red": "Red (Director)", "p_yellow": "Yellow (Inspirer)", "p_green": "Green (Supporter)", "p_blue": "Blue (Analyst)",
        "pers_asp": "Personal Aspirations", "work_asp": "Work Aspirations", "coop": "Cooperativeness",
        "qa_name": "QA Coach Name", "qa_ticket": "Ticket ID", "qa_score": "QA Score (%)",
        "qa_str": "🌟 Strengths", "qa_imp": "⚠️ Areas of Improvement",
        "exec": "### 📋 Coaching Execution",
        "tab1": "📊 KPI Matrix", "tab2": "🧠 5 Whys", "tab3": "🎯 SMART Goals", "tab4": "⚠️ Disciplinary", "tab5": "🗂️ History",
        "week": "Week", "issue": "Main Issue", "root": "Why 5 (Root Cause)",
        "smart_s": "Specific (S)", "smart_m": "Measurable (M)", "smart_a": "Achievable (A)", "smart_r": "Relevant (R)", "smart_t": "Deadline (T)",
        "outlier": "Trigger Disciplinary Action", "action": "Action", "notes": "Manager Notes",
        "save": "💾 SAVE & FINALIZE", "success": "Session saved successfully!"
    },
    "Deutsch 🇩🇪": {
        "title": "💎 Nexus Pro: Management & Coaching System",
        "settings": "🏢 Systemeinstellungen", "campaign": "Kampagne", "location": "Standort", "work_model": "Arbeitsmodell",
        "time": "📅 Zeit & Datum", "date": "Datum", "quarter": "Quartal", "month": "Monat", "year": "Jahr",
        "targets": "🎯 Zielvorgaben (KPIs)", "target_csat": "Ziel CSAT %", "target_qa": "Ziel QA %", "target_aht": "Ziel AHT (Sek)",
        "hierarchy": "👥 0. Führungsebene", "coach": "Coach Name", "tl": "Team Leader Name", "aom": "AOM Name",
        "exp1": "👤 1. Profil & Persönlichkeit", "exp2": "🌟 2. Bestrebungen & Motivation", "exp3": "🎧 3. Qualitätsbewertung (QA)",
        "avatar": "Avatar Quelle", "male": "Mann", "female": "Frau", "upload": "Foto Hochladen",
        "agent_name": "Name des Agenten", "work_email": "Arbeits-E-Mail", "role": "Rolle", "languages": "Arbeitssprachen",
        "primary_p": "Haupttyp", "secondary_p": "Sekundärtyp",
        "p_red": "Rot (Direktor)", "p_yellow": "Gelb (Inspirator)", "p_green": "Grün (Unterstützer)", "p_blue": "Blau (Analyst)",
        "pers_asp": "Persönliche Ziele", "work_asp": "Berufliche Ziele", "coop": "Kooperationsbereitschaft",
        "qa_name": "QA Coach Name", "qa_ticket": "Ticket-ID", "qa_score": "QA-Bewertung (%)",
        "qa_str": "🌟 Stärken", "qa_imp": "⚠️ Verbesserungsbereiche",
        "exec": "### 📋 Coaching-Ausführung",
        "tab1": "📊 KPI-Werte", "tab2": "🧠 5 Whys", "tab3": "🎯 SMART-Ziele", "tab4": "⚠️ Disziplinarisch", "tab5": "🗂️ Verlauf",
        "week": "Woche", "issue": "Hauptproblem", "root": "Warum 5 (Ursache)",
        "smart_s": "Spezifisch (S)", "smart_m": "Messbar (M)", "smart_a": "Erreichbar (A)", "smart_r": "Relevant (R)", "smart_t": "Frist (T)",
        "outlier": "Disziplinarmaßnahme auslösen", "action": "Aktion", "notes": "Notizen",
        "save": "💾 SPEICHERN & ABSCHLIESSEN", "success": "Sitzung erfolgreich gespeichert!"
    },
    "Svenska 🇸🇪": {
        "title": "💎 Nexus Pro: Lednings- och Coachningssystem",
        "settings": "🏢 Systeminställningar", "campaign": "Kampanj", "location": "Plats", "work_model": "Arbetsmodell",
        "time": "📅 Tid & Datum", "date": "Datum", "quarter": "Kvartal", "month": "Månad", "year": "År",
        "targets": "🎯 Målvärden (KPI)", "target_csat": "Mål CSAT %", "target_qa": "Mål QA %", "target_aht": "Mål AHT (sek)",
        "hierarchy": "👥 0. Ledarskapshierarki", "coach": "Coach Namn", "tl": "Team Leader Namn", "aom": "AOM Namn",
        "exp1": "👤 1. Profil & Personlighet", "exp2": "🌟 2. Ambitioner & Motivation", "exp3": "🎧 3. Kvalitetsutvärdering (QA)",
        "avatar": "Avatar Källa", "male": "Man", "female": "Kvinna", "upload": "Ladda Upp",
        "agent_name": "Agentens Namn", "work_email": "Arbets-E-post", "role": "Roll", "languages": "Arbetsspråk",
        "primary_p": "Primär Typ", "secondary_p": "Sekundär Typ",
        "p_red": "Röd (Direktör)", "p_yellow": "Gul (Inspiratör)", "p_green": "Grön (Stödjare)", "p_blue": "Blå (Analytiker)",
        "pers_asp": "Personliga Mål", "work_asp": "Yrkesmål", "coop": "Samarbetsnivå",
        "qa_name": "QA Coach Namn", "qa_ticket": "Ticket ID", "qa_score": "QA-Poäng (%)",
        "qa_str": "🌟 Styrkor", "qa_imp": "⚠️ Förbättringsområden",
        "exec": "### 📋 Coaching Utförande",
        "tab1": "📊 KPI Värden", "tab2": "🧠 5 Whys", "tab3": "🎯 SMART Mål", "tab4": "⚠️ Disciplinär", "tab5": "🗂️ Historik",
        "week": "Vecka", "issue": "Huvudproblem", "root": "Varför 5 (Grundorsak)",
        "smart_s": "Specifikt (S)", "smart_m": "Mätbart (M)", "smart_a": "Uppnåeligt (A)", "smart_r": "Relevant (R)", "smart_t": "Deadline (T)",
        "outlier": "Utlösa Disciplinär Åtgärd", "action": "Åtgärd", "notes": "Anteckningar",
        "save": "💾 SPARA & AVSLUTA", "success": "Sessionen har sparats!"
    }
}

# --- SIDEBAR LANGUAGE SELECTOR ---
lang_choice = st.sidebar.radio("🌍 Language / Γλώσσα", ["Ελληνικά 🇬🇷", "English 🇬🇧", "Deutsch 🇩🇪", "Svenska 🇸🇪"], horizontal=True)
t = lang_dict[lang_choice]

st.sidebar.markdown("---")
st.sidebar.header(t["settings"])
project = st.sidebar.selectbox(t["campaign"], ["Booking.com", "Apple Support", "Google", "Netflix"])
site = st.sidebar.selectbox(t["location"], ["Thessaloniki", "Athens", "Cairo", "Lisbon", "Barcelona", "Berlin", "Stockholm"])
work_model = st.sidebar.selectbox(t["work_model"], ["On-Site", "WFH (Remote)", "Hybrid"])

st.sidebar.markdown("---")
st.sidebar.header(t["time"])
coaching_date = st.sidebar.date_input(t["date"], datetime.date.today())
quarter = st.sidebar.selectbox(t["quarter"], ["Q1", "Q2", "Q3", "Q4"])
month = st.sidebar.selectbox(t["month"], ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
year = st.sidebar.number_input(t["year"], value=2026, step=1)

st.sidebar.markdown("---")
st.sidebar.header(t["targets"])
t_csat = st.sidebar.slider(t["target_csat"], 70, 100, 85)
t_qa = st.sidebar.slider(t["target_qa"], 70, 100, 90)
t_aht = st.sidebar.number_input(t["target_aht"], value=280)

# --- HELPER FUNCTION FOR COLORS ---
def get_color(p_str):
    if any(x in p_str for x in ["Red", "Κόκκινο", "Rot", "Röd"]): return "#FF4B4B", "white"
    if any(x in p_str for x in ["Yellow", "Κίτρινο", "Gelb", "Gul"]): return "#FFEB3B", "black"
    if any(x in p_str for x in ["Green", "Πράσινο", "Grün"]): return "#4CAF50", "white"
    return "#0083B0", "white"

# --- MAIN UI ---
st.title(t["title"])

# --- 0. LEADERSHIP HIERARCHY ---
with st.expander(t["hierarchy"], expanded=True):
    h1, h2, h3 = st.columns(3)
    with h1: coach_name = st.text_input(t["coach"], "Ilias P.")
    with h2: tl_name = st.text_input(t["tl"], "")
    with h3: aom_name = st.text_input(t["aom"], "")

# --- 1. AGENT PROFILE ---
with st.expander(t["exp1"], expanded=True):
    col1, col2, col3 = st.columns([1, 2, 3])
    
    with col1:
        avatar_type = st.radio(t["avatar"], [t["male"], t["female"], t["upload"]], horizontal=True)
        if avatar_type == t["upload"]:
            photo = st.file_uploader("", type=['png', 'jpg'])
            if photo: st.image(photo, width=120)
        elif avatar_type == t["female"]:
            st.image("https://www.w3schools.com/howto/img_avatar2.png", width=120)
        else:
            st.image("https://www.w3schools.com/howto/img_avatar.png", width=120)
            
    with col2:
        agent_name = st.text_input(t["agent_name"], "Nick Kalas")
        work_email = st.text_input(t["work_email"], "agent@booking.com")
        agent_lang = st.multiselect(t["languages"], ["Greek", "English", "German", "Swedish", "French", "Spanish"], default=["English"])
        
    with col3:
        p_primary = st.selectbox(f"🌟 {t['primary_p']}", [t["p_red"], t["p_yellow"], t["p_green"], t["p_blue"]])
        p_secondary = st.selectbox(f"🌓 {t['secondary_p']}", [t["p_red"], t["p_yellow"], t["p_green"], t["p_blue"]], index=1)
        
        c_hex_p, font_c_p = get_color(p_primary)
        c_hex_s, font_c_s = get_color(p_secondary)
        
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between;'>
            <div style='width: 48%; padding:10px; border-radius:10px; background-color:{c_hex_p}; color:{font_c_p}; text-align:center;'><b>{t['primary_p']}:</b><br>{p_primary}</div>
            <div style='width: 48%; padding:10px; border-radius:10px; background-color:{c_hex_s}; color:{font_c_s}; text-align:center; opacity: 0.8;'><b>{t['secondary_p']}:</b><br>{p_secondary}</div>
        </div>
        """, unsafe_allow_html=True)

# --- 2. ASPIRATIONS ---
with st.expander(t["exp2"], expanded=False):
    asp1, asp2, asp3 = st.columns(3)
    with asp1: personal_asp = st.text_area(t["pers_asp"])
    with asp2: work_asp = st.text_area(t["work_asp"])
    with asp3: coop = st.select_slider(t["coop"], options=["1/4", "2/4", "3/4", "4/4 (Team Player)"])

# --- 3. QA FEEDBACK ---
with st.expander(t["exp3"], expanded=True):
    qa_col1, qa_col2, qa_col3 = st.columns(3)
    with qa_col1:
        qa_name = st.text_input(t["qa_name"], "Maria S.")
        qa_ticket = st.text_input(t["qa_ticket"], "BKG-98765")
        qa_score = st.number_input(t["qa_score"], value=82.0)
    with qa_col2: qa_strengths = st.text_area(t["qa_str"])
    with qa_col3: qa_improvements = st.text_area(t["qa_imp"])

# --- COACHING TABS ---
st.markdown(t["exec"])
tab1, tab2, tab3, tab4, tab5 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"], t["tab5"]])

# TAB 1: KPIs
with tab1:
    cols = st.columns(4)
    w_data = {}
    for i in range(1, 5):
        with cols[i-1]:
            st.markdown(f"**{t['week']} {i}**")
            c = st.number_input("CSAT", value=float(t_csat), key=f"c{i}")
            q = st.number_input("QA", value=float(t_qa), key=f"q{i}")
            a = st.number_input("AHT", value=float(t_aht), key=f"a{i}")
            w_data[f"W{i}"] = [c, q, a]
    df = pd.DataFrame(w_data, index=["CSAT", "QA", "AHT"])
    df['MTD'] = df.mean(axis=1)
    
    st.markdown("---")
    c_viz1, c_viz2 = st.columns(2)
    with c_viz1:
        radar_df = df[['MTD']].reset_index()
        fig1 = px.line_polar(radar_df, r='MTD', theta='index', line_close=True)
        fig1.update_traces(fill='toself')
        st.plotly_chart(fig1, use_container_width=True)

# TAB 2: 5 WHYS
with tab2:
    issue = st.text_input(t["issue"])
    w1, w2, w3, w4 = st.text_input("Why 1?"), st.text_input("Why 2?"), st.text_input("Why 3?"), st.text_input("Why 4?")
    root = st.text_input(t["root"])

# TAB 3: SMART GOALS
with tab3:
    s1, s2 = st.columns(2)
    with s1:
        spec = st.text_input(t["smart_s"])
        meas = st.text_input(t["smart_m"])
    with s2:
        achiev = st.text_input(t["smart_a"])
        relev = st.text_input(t["smart_r"])
        timel = st.date_input(t["smart_t"])

# TAB 4: DISCIPLINE
with tab4:
    is_outlier = st.toggle(t["outlier"])
    action_taken = "None"
    if is_outlier:
        action_taken = st.selectbox(t["action"], ["Verbal Warning", "Written Warning (1st)", "PIP"])
        st.text_area(t["notes"])

# --- SAVE ---
st.markdown("---")
if st.button(t["save"], use_container_width=True):
    session_data = {
        "Date": coaching_date, "Agent": agent_name, "Coach": coach_name, "TL": tl_name,
        "QA Score": f"{qa_score}%", "Root Cause": root if root else "N/A", "Disciplinary": action_taken
    }
    st.session_state['coaching_history'].append(session_data)
    st.balloons()
    st.success(f"{t['success']} ({agent_name})")

# TAB 5: HISTORY
with tab5:
    if len(st.session_state['coaching_history']) > 0:
        st.dataframe(pd.DataFrame(st.session_state['coaching_history']), use_container_width=True)