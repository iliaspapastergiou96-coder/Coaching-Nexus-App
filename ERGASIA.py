import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import urllib.parse
import streamlit.components.v1 as components

# --- CONFIG & SYSTEM MEMORY ---
st.set_page_config(page_title="Nexus Pro | Management OS", layout="wide")

if 'coaching_history' not in st.session_state: st.session_state['coaching_history'] = []
if 'custom_roots' not in st.session_state: st.session_state['custom_roots'] = []
if 'custom_actions' not in st.session_state: st.session_state['custom_actions'] = []
if 'my_team' not in st.session_state: st.session_state['my_team'] = ["Nick Kalas", "Maria S."]
if 'num_whys' not in st.session_state: st.session_state['num_whys'] = 1

# AI MAPPING: Root Causes -> Προτεινόμενα Action Plans
rc_action_map = {
    "Product Knowledge / Skill Gap": ["Review Knowledge Base (KB) Article", "Complete Training Module", "Roleplay Scenario"],
    "System Latency / Tech Issues": ["Raise IT Helpdesk Ticket", "Teach Keyboard Shortcuts", "Clear Cache/Cookies Workflow"],
    "Burnout / Mental Fatigue": ["Schedule Wellbeing Check-in", "Review PTO / Vacation Accrual", "Workload Rebalance"],
    "Process Confusion": ["Side-by-Side Shadowing", "Review Standard Operating Procedure (SOP)"],
    "AHT Pressure (Handling Time)": ["Call Control Coaching", "Shadow High Performer", "Hold-time Best Practices"],
    "Missed QA Verification (Fatal)": ["Compliance & Security Refresher", "Sticky Note Reminder on Monitor"],
    "Lack of Empathy / Tone of Voice": ["Soft Skills Workshop", "Empathy Phrasing Practice", "Listen to 'Golden Calls'"]
}

# --- 4-LANGUAGE DICTIONARY (100% FULL UI TRANSLATION + TOOLTIPS) ---
lang_dict = {
    "Ελληνικά 🇬🇷": {
        "title": "Nexus Pro | Performance & Coaching OS", "subtitle": "Σύστημα Διαχείρισης Απόδοσης & Ανάπτυξης Προσωπικού",
        "team_mgmt": "👥 Η Ομάδα Μου (My Team)", "add_agent": "Προσθήκη Agent", "add_btn": "➕ Προσθήκη", "sel_agent": "👤 Ενεργός Agent", "rem_btn": "❌ Διαγραφή",
        "settings": "🏢 Ρυθμίσεις Συστήματος", "proj": "Project / Καμπάνια", "model": "Μοντέλο Εργασίας", "loc": "Τοποθεσία", "date": "Ημερομηνία", "duration": "Διάρκεια",
        "targets": "🎯 Στόχοι Εταιρείας (KPIs)", "timer": "Χρονόμετρο Συνεδρίας", "start": "▶ Έναρξη", "stop": "⏹ Παύση",
        "hierarchy": "1. Διοικητική Ομάδα", "coach": "Coach / Team Leader", "qa_eval": "QA Evaluator",
        "exp1": "2. Προφίλ & Αναλυτικά Στοιχεία Agent", "avatar": "Εικόνα Προφίλ", "male": "Άνδρας", "female": "Γυναίκα", "upload": "Ανέβασμα",
        "name": "Ονοματεπώνυμο Agent", "email": "Εταιρικό Email", "tenure": "Εμπειρία (Tenure)", "langs": "Γλώσσες Εργασίας",
        "behavior": "Behavioral Profile (Ψυχολογία)", "prim_p": "Κύριος Τύπος", "sec_p": "Δευτερεύων Τύπος", "ai_insight": "🧠 AI Οδηγία", "flight": "Πρόβλεψη Ρίσκου Παραίτησης",
        "exp2": "3. Αξιολόγηση Ποιότητας (QA)", "qa_score": "Σκορ QA (%)", "qa_notes": "Σχόλια QA / Στόχοι",
        "tab1": "Μετρικές (KPIs)", "tab2": "Ανάλυση Αιτιών (5 Whys)", "tab3": "S.M.A.R.T. & Action Plan", "tab4": "Αναγνώριση & Συμμόρφωση", "tab5": "Ιστορικό & Email",
        "week": "Εβδομάδα", "mtd_vs_tgt": "MTD vs Στόχος", "chart_type": "Είδος Γραφήματος",
        "rc_ident": "Αναγνώριση Αιτίας (Root Cause)", "add_why": "Προσθήκη Why", "pri_rc": "Κύρια Αιτία (Primary):", "sec_rc": "Δευτερεύουσα Αιτία (Secondary):", "def_rc": "Γράψε Νέα Αιτία:",
        "smart_title": "📝 Στοχοθεσία S.M.A.R.T.", "s_s": "Specific (Συγκεκριμένος)", "s_m": "Measurable (Μετρήσιμος)", "s_a": "Achievable (Εφικτός)", "s_r": "Relevant (Σχετικός)", "s_t": "Time-bound (Χρόνος)",
        "ap_title": "🛠️ Πλάνο Δράσης (Action Plan)", "strat_ap": "Στρατηγική Ενέργεια:", "def_ap": "Γράψε Νέα Ενέργεια:", "deadline": "Προθεσμία:",
        "kudos_title": "🏆 Αναγνώριση (Kudos)", "kudos_btn": "Δημιουργία Μηνύματος", "comp_title": "⚠️ Συμμόρφωση & Πειθαρχικά", "flag_out": "Ενεργοποίηση Πειθαρχικού", "comp_action": "Ενέργεια Συμμόρφωσης",
        "sign_title": "📝 Έλεγχος & Ψηφιακή Υπογραφή", "sign_text": "Ο/Η Agent κατανοεί και συμφωνεί με το Action Plan.", "initials": "Αρχικά Agent",
        "save_btn": "📥 ΑΠΟΘΗΚΕΥΣΗ SESSION", "err_sign": "❌ Απαιτείται υπογραφή και συγκατάθεση για αποθήκευση.", "succ_save": "✅ Η συνεδρία αποθηκεύτηκε επιτυχώς!",
        "hist_ag": "👤 Ιστορικό Coaching για:", "db_team": "🏢 Πλήρης Βάση Δεδομένων", "export_btn": "📥 Εξαγωγή Ολικής Βάσης", "db_mgmt": "🗑️ Διαχείριση Βάσης", "del_all": "🚨 Διαγραφή Όλου του Ιστορικού", "del_sel": "❌ Διαγραφή Επιλεγμένου", "sel_del": "Επίλεξε συνεδρία για διαγραφή:",
        "email_gen": "✉️ Δημιουργία Επίσημου Email", "sel_sess": "Επίλεξε Συνεδρία προς Αποστολή:", "prev_email": "👀 Προεπισκόπηση Αναφοράς", "send_btn": "✉️ Αποστολή μέσω Outlook / Gmail",
        "tt_red": "Αποφασιστικός, γρήγορος, εστιάζει στο αποτέλεσμα. Απεχθάνεται το micromanagement.", "tt_yellow": "Κοινωνικός, ενθουσιώδης. Θέλει αναγνώριση. Προσοχή στο AHT.", "tt_green": "Ήρεμος, υπομονετικός. Απεχθάνεται την πίεση. Κίνδυνος burnout.", "tt_blue": "Αναλυτικός, ακριβής. Απαιτεί δεδομένα. Τον ενοχλεί η φασαρία.",
        "email_subject": "Επίσημη Ανασκόπηση Coaching - {}",
        "email_body": "Αγαπητέ/ή {},\n\nΣε ευχαριστώ πολύ για τη σημερινή μας συνεδρία.\n\n[1. ΑΠΟΔΟΣΗ & ΜΕΤΡΙΚΕΣ]\n- Στόχος CSAT: {}% | Τρέχον: {}%\n- Στόχος QA: {}% | Τρέχον: {}\n\n[2. ΑΝΑΛΥΣΗ ΑΙΤΙΩΝ]\n- Κύρια Αιτία: {}\n- Δευτερεύουσα Αιτία: {}\n\n[3. S.M.A.R.T. ΣΤΟΧΟΙ & ACTION PLAN]\n- Specific: {}\n- Measurable: {}\n- Achievable: {}\n- Relevant: {}\n- Time-bound: {}\n- Επίσημο Action Plan: {}\n\nΠαρακαλώ όπως απαντήσεις επιβεβαιώνοντας ότι αποδέχεσαι το πλάνο.\n\nΜε εκτίμηση,\n{}"
    },
    "English 🇬🇧": {
        "title": "Nexus Pro | Performance & Coaching OS", "subtitle": "Enterprise Performance Management & Staff Development",
        "team_mgmt": "👥 My Team Management", "add_agent": "Add New Agent", "add_btn": "➕ Add", "sel_agent": "👤 Select Active Agent", "rem_btn": "❌ Remove",
        "settings": "🏢 System Settings", "proj": "Project / Campaign", "model": "Work Model", "loc": "Location", "date": "Session Date", "duration": "Duration",
        "targets": "🎯 Corporate Targets (KPIs)", "timer": "Live Session Timer", "start": "▶ Start", "stop": "⏹ Stop",
        "hierarchy": "1. Leadership & Management", "coach": "Coach / Team Leader", "qa_eval": "QA Evaluator",
        "exp1": "2. Agent Profile & Behavioral Analytics", "avatar": "Profile Image", "male": "Male", "female": "Female", "upload": "Upload",
        "name": "Agent Full Name", "email": "Corporate Email", "tenure": "Tenure Level", "langs": "Working Languages",
        "behavior": "Behavioral Profile", "prim_p": "Primary Personality", "sec_p": "Secondary Personality", "ai_insight": "🧠 AI Management Insight", "flight": "Retention AI Forecast",
        "exp2": "3. Career Development & QA", "qa_score": "Overall QA Score (%)", "qa_notes": "QA Feedback / Goals",
        "tab1": "Metrics (KPIs)", "tab2": "Root Causes & 5 Whys", "tab3": "S.M.A.R.T. & Action Plan", "tab4": "Recognition & Compliance", "tab5": "History & Email",
        "week": "Week", "mtd_vs_tgt": "MTD vs Target", "chart_type": "Visualization",
        "rc_ident": "Root Cause Identification", "add_why": "Add Why", "pri_rc": "Primary Root Cause:", "sec_rc": "Secondary Root Cause:", "def_rc": "Define Custom Cause:",
        "smart_title": "📝 S.M.A.R.T. Target Setting", "s_s": "Specific", "s_m": "Measurable", "s_a": "Achievable", "s_r": "Relevant", "s_t": "Time-bound",
        "ap_title": "🛠️ Action Plan Assignment", "strat_ap": "Strategic Action Plan:", "def_ap": "Define Custom Action:", "deadline": "Target Deadline:",
        "kudos_title": "🏆 Recognition (Kudos)", "kudos_btn": "Generate Recognition Note", "comp_title": "⚠️ Compliance & Discipline", "flag_out": "Flag for Disciplinary Review", "comp_action": "Compliance Action",
        "sign_title": "📝 Manager Review & Digital Sign-off", "sign_text": "Agent acknowledges and agrees to this action plan.", "initials": "Agent Initials",
        "save_btn": "📥 SAVE SESSION TO DATABASE", "err_sign": "❌ Action Required: Agent must agree and provide initials.", "succ_save": "✅ Record successfully logged!",
        "hist_ag": "👤 Coaching History for:", "db_team": "🏢 Full Team Database", "export_btn": "📥 Export Full DB", "db_mgmt": "🗑️ Database Management", "del_all": "🚨 Clear All History", "del_sel": "❌ Delete Selected", "sel_del": "Select record to delete:",
        "email_gen": "✉️ Generate Official Coaching Log", "sel_sess": "Select Session Date to Email:", "prev_email": "👀 Email Preview", "send_btn": "✉️ Send via Outlook / Gmail",
        "tt_red": "Results-oriented, decisive, fast-paced. Dislikes micromanagement.", "tt_yellow": "Sociable, enthusiastic. Needs recognition. Monitor AHT.", "tt_green": "Calm, patient. Dislikes pressure. Risk of burnout.", "tt_blue": "Analytical, precise. Requires data. Dislikes noise.",
        "email_subject": "Official Coaching Session Log - {}",
        "email_body": "Dear {},\n\nThank you for your time during our coaching session.\n\n[1. PERFORMANCE METRICS]\n- Target CSAT: {}% | Actual: {}%\n- Target QA: {}% | Actual: {}\n\n[2. ROOT CAUSE ANALYSIS]\n- Primary Root Cause: {}\n- Secondary Root Cause: {}\n\n[3. S.M.A.R.T. TARGETS & ACTION PLAN]\n- Specific: {}\n- Measurable: {}\n- Achievable: {}\n- Relevant: {}\n- Time-bound: {}\n- Official Action Plan: {}\n\nPlease reply to this email to acknowledge that you understand and agree with the action plan outlined above.\n\nBest regards,\n{}"
    },
    "Deutsch 🇩🇪": {
        "title": "Nexus Pro | Performance & Coaching OS", "subtitle": "Leistungsmanagement & Personalentwicklung",
        "team_mgmt": "👥 Meine Teamverwaltung", "add_agent": "Agenten hinzufügen", "add_btn": "➕ Hinzufügen", "sel_agent": "👤 Agenten auswählen", "rem_btn": "❌ Entfernen",
        "settings": "🏢 Systemeinstellungen", "proj": "Projekt", "model": "Arbeitsmodell", "loc": "Standort", "date": "Datum", "duration": "Dauer",
        "targets": "🎯 Unternehmensziele (KPIs)", "timer": "Sitzungs-Timer", "start": "▶ Start", "stop": "⏹ Stopp",
        "hierarchy": "1. Führung & Management", "coach": "Coach / Team Leader", "qa_eval": "QA Bewerter",
        "exp1": "2. Agentenprofil & Verhaltensanalytik", "avatar": "Profilbild", "male": "Mann", "female": "Frau", "upload": "Hochladen",
        "name": "Name des Agenten", "email": "E-Mail", "tenure": "Erfahrung", "langs": "Sprachen",
        "behavior": "Verhaltensprofil", "prim_p": "Primärer Typ", "sec_p": "Sekundärer Typ", "ai_insight": "🧠 AI Coaching-Tipp", "flight": "Kündigungsrisiko",
        "exp2": "3. Qualitätsbewertung (QA)", "qa_score": "QA-Ergebnis (%)", "qa_notes": "QA Notizen",
        "tab1": "KPI-Werte", "tab2": "Ursachenanalyse", "tab3": "S.M.A.R.T. & Aktionsplan", "tab4": "Anerkennung & Compliance", "tab5": "Verlauf & E-Mail",
        "week": "Woche", "mtd_vs_tgt": "MTD vs Ziel", "chart_type": "Diagrammtyp",
        "rc_ident": "Ursachenidentifikation", "add_why": "Warum hinzufügen", "pri_rc": "Hauptursache:", "sec_rc": "Sekundäre Ursache:", "def_rc": "Eigene Ursache definieren:",
        "smart_title": "📝 S.M.A.R.T. Ziele", "s_s": "Spezifisch", "s_m": "Messbar", "s_a": "Erreichbar", "s_r": "Relevant", "s_t": "Terminiert",
        "ap_title": "🛠️ Aktionsplan", "strat_ap": "Strategische Aktion:", "def_ap": "Eigene Aktion:", "deadline": "Frist:",
        "kudos_title": "🏆 Anerkennung", "kudos_btn": "Lob generieren", "comp_title": "⚠️ Disziplinarmaßnahmen", "flag_out": "Disziplinarisch markieren", "comp_action": "Maßnahme",
        "sign_title": "📝 Digitale Unterschrift", "sign_text": "Der Agent stimmt diesem Aktionsplan zu.", "initials": "Initialen",
        "save_btn": "📥 SESSION SPEICHERN", "err_sign": "❌ Agent muss zustimmen und Initialen angeben.", "succ_save": "✅ Erfolgreich gespeichert!",
        "hist_ag": "👤 Coaching-Verlauf für:", "db_team": "🏢 Gesamte Datenbank", "export_btn": "📥 CSV Exportieren", "db_mgmt": "🗑️ Datenbankverwaltung", "del_all": "🚨 Gesamten Verlauf löschen", "del_sel": "❌ Ausgewählte löschen", "sel_del": "Zu löschenden Datensatz wählen:",
        "email_gen": "✉️ Offizielle E-Mail generieren", "sel_sess": "Sitzung für E-Mail auswählen:", "prev_email": "👀 Vorschau", "send_btn": "✉️ Senden via Outlook",
        "tt_red": "Ergebnisorientiert, entscheidungsfreudig. Mag kein Mikromanagement.", "tt_yellow": "Kontaktfreudig, enthusiastisch. Braucht Anerkennung. AHT im Auge behalten.", "tt_green": "Ruhig, geduldig. Mag keinen Druck. Burnout-Risiko.", "tt_blue": "Analytisch, präzise. Benötigt Daten. Mag keinen Lärm.",
        "email_subject": "Offizielles Coaching-Protokoll - {}",
        "email_body": "Hallo {},\n\nvielen Dank für deine Zeit.\n\n[1. LEISTUNGSKENNZAHLEN]\n- Ziel CSAT: {}% | Aktuell: {}%\n- Ziel QA: {}% | Aktuell: {}\n\n[2. URSACHENANALYSE]\n- Hauptursache: {}\n- Sekundäre Ursache: {}\n\n[3. S.M.A.R.T. & AKTIONSPLAN]\n- Spezifisch: {}\n- Messbar: {}\n- Erreichbar: {}\n- Relevant: {}\n- Terminiert: {}\n- Aktionsplan: {}\n\nBitte antworte auf diese E-Mail, um den Plan zu bestätigen.\n\nBeste Grüße,\n{}"
    },
    "Svenska 🇸🇪": {
        "title": "Nexus Pro | Performance & Coaching OS", "subtitle": "Verksamhetsstyrning & Personalutveckling",
        "team_mgmt": "👥 Min Teamhantering", "add_agent": "Lägg till Agent", "add_btn": "➕ Lägg till", "sel_agent": "👤 Välj Agent", "rem_btn": "❌ Ta bort",
        "settings": "🏢 Systeminställningar", "proj": "Projekt", "model": "Arbetsmodell", "loc": "Plats", "date": "Datum", "duration": "Varaktighet",
        "targets": "🎯 Företagets Mål (KPI)", "timer": "Session Timer", "start": "▶ Start", "stop": "⏹ Stopp",
        "hierarchy": "1. Ledarskap & Chefer", "coach": "Coach / Team Leader", "qa_eval": "QA Utvärderare",
        "exp1": "2. Agentprofil & Beteendeanalys", "avatar": "Profilbild", "male": "Man", "female": "Kvinna", "upload": "Ladda upp",
        "name": "Agentens Namn", "email": "E-post", "tenure": "Erfarenhet", "langs": "Språk",
        "behavior": "Beteendeprofil", "prim_p": "Primär Personlighet", "sec_p": "Sekundär Personlighet", "ai_insight": "🧠 AI Coaching-tips", "flight": "Risk för uppsägning",
        "exp2": "3. Kvalitetsutvärdering (QA)", "qa_score": "QA Resultat (%)", "qa_notes": "QA Anteckningar",
        "tab1": "Prestationsmått", "tab2": "Grundorsaker", "tab3": "S.M.A.R.T. & Handlingsplan", "tab4": "Erkännande & Disciplin", "tab5": "Historik & E-post",
        "week": "Vecka", "mtd_vs_tgt": "MTD vs Mål", "chart_type": "Diagramtyp",
        "rc_ident": "Grundorsaksanalys", "add_why": "Lägg till Varför", "pri_rc": "Huvudorsak:", "sec_rc": "Sekundär orsak:", "def_rc": "Definiera Egen Orsak:",
        "smart_title": "📝 S.M.A.R.T. Målsättning", "s_s": "Specifikt", "s_m": "Mätbart", "s_a": "Uppnåeligt", "s_r": "Relevant", "s_t": "Tidsbunden",
        "ap_title": "🛠️ Handlingsplan", "strat_ap": "Strategisk Åtgärd:", "def_ap": "Egen Åtgärd:", "deadline": "Deadline:",
        "kudos_title": "🏆 Erkännande", "kudos_btn": "Generera Beröm", "comp_title": "⚠️ Disciplinära åtgärder", "flag_out": "Markera för åtgärd", "comp_action": "Åtgärd",
        "sign_title": "📝 Digital Signatur", "sign_text": "Agenten godkänner denna handlingsplan.", "initials": "Initialer",
        "save_btn": "📥 SPARA SESSION", "err_sign": "❌ Agenten måste godkänna.", "succ_save": "✅ Sparad framgångsrikt!",
        "hist_ag": "👤 Coachinghistorik för:", "db_team": "🏢 Hela Databasen", "export_btn": "📥 Exportera (CSV)", "db_mgmt": "🗑️ Databashantering", "del_all": "🚨 Rensa all historik", "del_sel": "❌ Ta bort vald", "sel_del": "Välj post att ta bort:",
        "email_gen": "✉️ Skapa Officiellt E-post", "sel_sess": "Välj session för e-post:", "prev_email": "👀 Förhandsgranska", "send_btn": "✉️ Skicka via Outlook",
        "tt_red": "Resultatinriktad, beslutsam, snabb. Ogillar detaljstyrning.", "tt_yellow": "Sällskaplig, entusiastisk. Behöver bekräftelse. Övervaka AHT.", "tt_green": "Lugn, tålmodig. Ogillar press. Risk för utbrändhet.", "tt_blue": "Analytisk, exakt. Kräver data. Ogillar oljud.",
        "email_subject": "Officiell Coaching Logg - {}",
        "email_body": "Hej {},\n\nTack för din tid idag.\n\n[1. PRESTATIONSMÅTT]\n- Mål CSAT: {}% | Aktuell: {}%\n- Mål QA: {}% | Aktuell: {}\n\n[2. GRUNDORSAK]\n- Huvudorsak: {}\n- Sekundär orsak: {}\n\n[3. S.M.A.R.T. & HANDLINGSPLAN]\n- Specifikt: {}\n- Mätbart: {}\n- Uppnåeligt: {}\n- Relevant: {}\n- Tidsbunden: {}\n- Åtgärd: {}\n\nVänligen svara på detta mejl för att bekräfta planen.\n\nVänliga hälsningar,\n{}"
    }
}

# --- UI LANGUAGE SELECTION ---
lang_choice = st.sidebar.selectbox("🌍 Language", ["English 🇬🇧", "Ελληνικά 🇬🇷", "Deutsch 🇩🇪", "Svenska 🇸🇪"])
t = lang_dict[lang_choice]
tt_text = f"🔴 Red: {t['tt_red']}\n\n🟡 Yellow: {t['tt_yellow']}\n\n🟢 Green: {t['tt_green']}\n\n🔵 Blue: {t['tt_blue']}"

# --- SIDEBAR CONFIGURATION & MY TEAM ---
st.sidebar.markdown("---")
st.sidebar.subheader(t["team_mgmt"])

new_member = st.sidebar.text_input(t["add_agent"], placeholder="...")
if st.sidebar.button(t["add_btn"]):
    if new_member and new_member not in st.session_state['my_team']:
        st.session_state['my_team'].append(new_member)
        st.sidebar.success("OK!")

active_agent = ""
if st.session_state['my_team']:
    active_agent = st.sidebar.selectbox(t["sel_agent"], st.session_state['my_team'])
    if st.sidebar.button(t["rem_btn"]):
        st.session_state['my_team'].remove(active_agent)
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader(t["settings"])
project = st.sidebar.selectbox(t["proj"], ["Booking.com", "Apple Support", "Google", "Netflix", "Customer Care"])
work_model = st.sidebar.selectbox(t["model"], ["On-Site", "WFH (Remote)", "Hybrid"])
site = st.sidebar.selectbox(t["loc"], ["Thessaloniki", "Athens", "Cairo", "Lisbon", "Barcelona", "Stockholm", "Berlin"])
coaching_date = st.sidebar.date_input(t["date"], datetime.date.today())
session_duration = st.sidebar.selectbox(t["duration"], ["15 mins", "30 mins", "45 mins", "60+ mins"])

# --- MAIN UI ---
st.title(t["title"])
st.markdown(f"**{t['subtitle']}**")

# --- CENTRAL TARGETS & LIVE TIMER (ME START & STOP) ---
st.markdown(f"### 🎯 {t['targets']}")
with st.container(border=True):
    ct1, ct2, ct3, ct4 = st.columns(4)
    with ct1: t_csat = st.number_input("Target CSAT %", 70.0, 100.0, 85.0)
    with ct2: t_qa = st.number_input("Target QA %", 70.0, 100.0, 90.0)
    with ct3: t_aht = st.number_input("Target AHT (sec)", value=280.0)
    with ct4:
        st.markdown(f"**{t['timer']}**")
        components.html(f"""
            <div style="font-family: Arial; font-size: 24px; font-weight: bold; color: #0083B0; text-align: center; border: 2px solid #0083B0; border-radius: 5px; padding: 5px;">
                <span id="time">00:00</span>
            </div>
            <div style="display: flex; gap: 5px; margin-top: 5px;">
                <button onclick="startTimer()" style="width: 50%; background-color: #4CAF50; color: white; border: none; padding: 5px; cursor: pointer; border-radius: 3px;">{t['start']}</button>
                <button onclick="stopTimer()" style="width: 50%; background-color: #FF4B4B; color: white; border: none; padding: 5px; cursor: pointer; border-radius: 3px;">{t['stop']}</button>
            </div>
            <script>
                let timerInterval; 
                let seconds = 0;
                function startTimer() {{
                    clearInterval(timerInterval); // Αποτρέπει το διπλό interval αν πατηθεί 2 φορές
                    timerInterval = setInterval(() => {{
                        seconds++;
                        let m = Math.floor(seconds / 60).toString().padStart(2, '0');
                        let s = (seconds % 60).toString().padStart(2, '0');
                        document.getElementById("time").innerText = m + ":" + s;
                    }}, 1000);
                }}
                function stopTimer() {{
                    clearInterval(timerInterval); // Σταματάει τον χρόνο χωρίς να τον μηδενίζει
                }}
            </script>
        """, height=100)

st.divider()

if active_agent:
    agent_past = [s for s in st.session_state['coaching_history'] if s['Agent'] == active_agent]
    if agent_past:
        last_action = agent_past[-1].get('Action Plan', '')
        last_date = agent_past[-1].get('Date', '')
        st.warning(f"🔄 **Follow-up:** ({last_date}) Action Plan: **'{last_action}'**.")

# --- 1. LEADERSHIP ---
st.subheader(t["hierarchy"])
col_l1, col_l2 = st.columns(2)
with col_l1: coach_name = st.text_input(t["coach"], "Ilias P.")
with col_l2: qa_evaluator = st.text_input(t["qa_eval"], "Maria S.")

# --- 2. AGENT PROFILE & AI MATRIX ---
st.subheader(t["exp1"])
c1, c2, c3 = st.columns([1, 2, 2])
with c1: 
    avatar = st.radio(t["avatar"], [t["male"], t["female"], t["upload"]], horizontal=True)
    if avatar == t["female"]: st.image("https://www.w3schools.com/howto/img_avatar2.png", width=120)
    elif avatar == t["upload"]:
        img = st.file_uploader("", type=['png', 'jpg'])
        if img: st.image(img, width=120)
    else: st.image("https://www.w3schools.com/howto/img_avatar.png", width=120)
    
with c2:
    agent_name = st.text_input(t["name"], value=active_agent)
    work_email = st.text_input(t["email"], f"{agent_name.replace(' ', '.').lower()}@booking.com" if agent_name else "agent@booking.com")
    tenure = st.selectbox(t["tenure"], ["0-6 Months (Rookie)", "6-12 Months (Developing)", "1-3 Years (Experienced)", "3+ Years (Veteran)"])
    agent_lang = st.multiselect(t["langs"], ["Greek", "English", "German", "French", "Spanish", "Italian", "Swedish"], default=["English"])
    
with c3:
    st.markdown(f"**{t['behavior']}**")
    color_ops = ["Red (Director)", "Yellow (Inspirer)", "Green (Supporter)", "Blue (Analyst)"]
    p_primary = st.selectbox(t["prim_p"], color_ops, help=tt_text)
    p_secondary = st.selectbox(t["sec_p"], color_ops, index=1, help=tt_text)
    
    def get_color(p):
        if "Red" in p: return "#FF4B4B", "white"
        if "Yellow" in p: return "#FFEB3B", "black"
        if "Green" in p: return "#4CAF50", "white"
        return "#0083B0", "white"
    
    c_hex_p, f_c_p = get_color(p_primary)
    c_hex_s, f_c_s = get_color(p_secondary)
    
    st.markdown(f"""
    <div style='display: flex; justify-content: space-between;'>
        <div style='width: 48%; padding:10px; border-radius:10px; background-color:{c_hex_p}; color:{f_c_p}; text-align:center;'><b>Primary:</b><br>{p_primary}</div>
        <div style='width: 48%; padding:10px; border-radius:10px; background-color:{c_hex_s}; color:{f_c_s}; text-align:center; opacity: 0.8;'><b>Secondary:</b><br>{p_secondary}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
flight_risk = "🟢 Low Risk"
if tenure in ["1-3 Years (Experienced)", "3+ Years (Veteran)"]: flight_risk = "🟡 Medium Risk"
st.markdown(f"**{t['flight']}:** {flight_risk}")

# --- 3. QA ---
st.subheader(t["exp2"])
qa1, qa2 = st.columns(2)
with qa1: qa_score = st.number_input(t["qa_score"], value=82.0)
with qa2: qa_notes = st.text_area(t["qa_notes"])

# --- COACHING WORKFLOW TABS ---
st.divider()
tab1, tab2, tab3, tab4, tab5 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"], t["tab5"]])

with tab1:
    cols = st.columns(4)
    w_data = {}
    for i in range(1, 5):
        with cols[i-1]:
            st.markdown(f"**{t['week']} {i}**")
            c = st.number_input(f"CSAT %", value=float(t_csat), key=f"c{i}")
            q = st.number_input(f"QA %", value=float(t_qa), key=f"q{i}")
            w_data[f"W{i}"] = [c, q]
            
    df = pd.DataFrame(w_data, index=["CSAT", "QA"])
    df['MTD'] = df.mean(axis=1)
    
    st.markdown("---")
    viz1, viz2 = st.columns([1, 2])
    with viz1:
        st.markdown(f"**{t['mtd_vs_tgt']}**")
        st.metric("CSAT", f"{df.loc['CSAT', 'MTD']:.1f}%")
        st.progress(min(int(df.loc['CSAT', 'MTD']), 100))
        st.metric("QA", f"{df.loc['QA', 'MTD']:.1f}%")
        st.progress(min(int(df.loc['QA', 'MTD']), 100))
        
    with viz2:
        c_type = st.radio(t["chart_type"], ["Radar", "Bar", "Line", "Area"], horizontal=True)
        if "Radar" in c_type:
            fig = px.line_polar(df[['MTD']].reset_index(), r='MTD', theta='index', line_close=True)
            fig.update_traces(fill='toself', line_color='#0083B0')
        elif "Bar" in c_type: fig = px.bar(df.drop(columns='MTD').T, barmode='group')
        elif "Line" in c_type: fig = px.line(df.drop(columns='MTD').T, markers=True)
        else: fig = px.area(df.drop(columns='MTD').T)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown(f"**{t['tab2']}**")
    for w in range(st.session_state['num_whys']):
        st.text_input(f"Why {w+1}?", key=f"why_{w}")
    
    if st.session_state['num_whys'] < 5:
        if st.button("➕ " + t["add_why"]):
            st.session_state['num_whys'] += 1
            st.rerun()
            
    st.markdown("---")
    st.markdown(f"**{t['rc_ident']}**")
    base_roots = list(rc_action_map.keys())
    
    c_rc1, c_rc2 = st.columns(2)
    with c_rc1:
        sel_pri_rc = st.selectbox(t["pri_rc"], ["-- Custom --"] + base_roots + st.session_state['custom_roots'])
        fin_pri_rc = st.text_input(t["def_rc"], key="pri_rc_inp") if sel_pri_rc == "-- Custom --" else sel_pri_rc
    with c_rc2:
        sel_sec_rc = st.selectbox(t["sec_rc"], ["-- None --", "-- Custom --"] + base_roots + st.session_state['custom_roots'])
        if sel_sec_rc == "-- Custom --":
            fin_sec_rc = st.text_input(t["def_rc"], key="sec_rc_inp")
        elif sel_sec_rc == "-- None --":
            fin_sec_rc = "None"
        else:
            fin_sec_rc = sel_sec_rc

with tab3:
    st.markdown(f"**{t['smart_title']}**")
    s1, s2 = st.columns(2)
    with s1:
        s_spec = st.text_input(t["s_s"])
        s_meas = st.text_input(t["s_m"])
        s_achi = st.text_input(t["s_a"])
    with s2:
        s_rele = st.text_input(t["s_r"])
        s_time = st.text_input(t["s_t"])
        
    st.markdown("---")
    st.markdown(f"**{t['ap_title']}**")
    suggested_actions = rc_action_map.get(fin_pri_rc, [])
    all_actions = ["-- Custom --"] + suggested_actions + st.session_state['custom_actions']
    selected_action = st.selectbox(t["strat_ap"], all_actions)
    final_action = st.text_input(t["def_ap"], key="fin_ap_inp") if selected_action == "-- Custom --" else selected_action
    deadline = st.date_input(t["deadline"], datetime.date.today() + datetime.timedelta(days=14))

with tab4:
    st.markdown(f"### {t['kudos_title']}")
    if st.button(t["kudos_btn"]): st.success(f"Great job, {agent_name}!")
    
    st.markdown("---")
    st.markdown(f"### {t['comp_title']}")
    is_outlier = st.toggle(t["flag_out"])
    action_taken = st.selectbox(t["comp_action"], ["Verbal Warning", "Written Warning", "PIP"]) if is_outlier else "None"

# --- DIGITAL SIGNATURE & SAVE ---
st.divider()
st.subheader(t["sign_title"])

col_sig1, col_sig2 = st.columns(2)
with col_sig1: agent_agrees = st.checkbox(t["sign_text"])
with col_sig2: agent_initials = st.text_input(t["initials"], max_chars=3)

if st.button("📥 " + t["save_btn"], use_container_width=True):
    if not agent_agrees or not agent_initials:
        st.error(t["err_sign"])
    else:
        if fin_pri_rc and fin_pri_rc != "-- Custom --" and fin_pri_rc not in base_roots and fin_pri_rc not in st.session_state['custom_roots']: st.session_state['custom_roots'].append(fin_pri_rc)
        if fin_sec_rc and fin_sec_rc != "None" and fin_sec_rc != "-- Custom --" and fin_sec_rc not in base_roots and fin_sec_rc not in st.session_state['custom_roots']: st.session_state['custom_roots'].append(fin_sec_rc)
        if final_action and final_action != "-- Custom --" and final_action not in rc_action_map.get(fin_pri_rc, []) and final_action not in st.session_state['custom_actions']: st.session_state['custom_actions'].append(final_action)

        csat_mtd = round(df.loc['CSAT', 'MTD'], 1)
        
        session_data = {
            "Date": str(coaching_date), "Agent": agent_name, "TL": coach_name, 
            "Target CSAT": t_csat, "Target QA": t_qa, "CSAT": csat_mtd, "QA": f"{qa_score}%", 
            "Primary Root Cause": fin_pri_rc, "Secondary Root Cause": fin_sec_rc, 
            "Action Plan": final_action, 
            "SMART_S": s_spec, "SMART_M": s_meas, "SMART_A": s_achi, "SMART_R": s_rele, "SMART_T": s_time,
            "Signed": agent_initials
        }
        st.session_state['coaching_history'].append(session_data)
        
        st.session_state['num_whys'] = 1
        st.success(t["succ_save"])

# TAB 5: HISTORY, EXPORT, DELETE & EMAIL
with tab5:
    st.markdown(f"### {t['db_mgmt']}")
    del1, del2 = st.columns(2)
    with del1:
        if st.button(t["del_all"]):
            st.session_state['coaching_history'] = []
            st.rerun()
    with del2:
        if len(st.session_state['coaching_history']) > 0:
            del_opts = [f"{i}: {s['Date']} - {s['Agent']}" for i, s in enumerate(st.session_state['coaching_history'])]
            sel_del = st.selectbox(t["sel_del"], del_opts)
            if st.button(t["del_sel"]):
                idx = int(sel_del.split(":")[0])
                st.session_state['coaching_history'].pop(idx)
                st.rerun()
                
    st.markdown("---")

    if len(st.session_state['coaching_history']) > 0:
        h_df = pd.DataFrame(st.session_state['coaching_history'])
        
        st.markdown(f"### {t['hist_ag']} {agent_name}")
        agent_df = h_df[h_df['Agent'] == agent_name]
        if not agent_df.empty:
            st.dataframe(agent_df, use_container_width=True)
            
            st.markdown("---")
            st.markdown(f"### {t['email_gen']}")
            
            session_options = agent_df['Date'].tolist()
            selected_session_date = st.selectbox(t["sel_sess"], reversed(session_options))
            sel_session = agent_df[agent_df['Date'] == selected_session_date].iloc[-1]
            
            subject = t["email_subject"].format(sel_session['Date'])
            body = t["email_body"].format(
                sel_session.get('Agent', agent_name), 
                sel_session.get('Target CSAT', t_csat), sel_session.get('CSAT', '-'), 
                sel_session.get('Target QA', t_qa), sel_session.get('QA', '-'), 
                sel_session.get('Primary Root Cause', sel_session.get('Root Cause', '-')), 
                sel_session.get('Secondary Root Cause', 'None'),
                sel_session.get('SMART_S', '-'), sel_session.get('SMART_M', '-'), sel_session.get('SMART_A', '-'), sel_session.get('SMART_R', '-'), sel_session.get('SMART_T', '-'),
                sel_session.get('Action Plan', '-'), sel_session.get('TL', coach_name)
            )
            mailto_link = f"mailto:{work_email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
            
            st.markdown(f"<a href='{mailto_link}' target='_blank'><button style='background-color:#0083B0; color:white; padding:10px 24px; border:none; border-radius:4px; cursor:pointer;'>{t['send_btn']}</button></a>", unsafe_allow_html=True)
            
            with st.expander(t["prev_email"], expanded=False):
                st.text(body)
                
        else:
            st.info(f"No records found for {agent_name}.")
            
        st.markdown("---")
        st.markdown(f"### {t['db_team']}")
        
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            csv = h_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label=t["export_btn"], data=csv, file_name=f"Nexus_Full_Export_{datetime.date.today()}.csv", mime="text/csv")
            
    else:
        st.info("No historical data found. Complete and save a session.")

st.divider()
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>Corporate Performance Management System | v24.2 Ultimate Edition</p>", unsafe_allow_html=True)