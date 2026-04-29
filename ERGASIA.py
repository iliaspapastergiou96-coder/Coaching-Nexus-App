import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import urllib.parse
import streamlit.components.v1 as components

# Προσπάθεια εισαγωγής της βιβλιοθήκης του Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# --- CONFIG & SYSTEM MEMORY ---
st.set_page_config(page_title="Nexus Pro | Management OS", layout="wide", initial_sidebar_state="expanded")

if 'coaching_history' not in st.session_state: st.session_state['coaching_history'] = []
if 'custom_roots' not in st.session_state: st.session_state['custom_roots'] = []
if 'custom_actions' not in st.session_state: st.session_state['custom_actions'] = []
if 'num_whys' not in st.session_state: st.session_state['num_whys'] = 1
if 'teams' not in st.session_state: st.session_state['teams'] = {"Alpha Team": ["Nick Kalas", "Maria S."]}
if 'active_team' not in st.session_state: st.session_state['active_team'] = None
if 'page' not in st.session_state: st.session_state['page'] = "Home"
if 'language' not in st.session_state: st.session_state['language'] = "English 🇬🇧"
if 'ai_chat_history' not in st.session_state: st.session_state['ai_chat_history'] = []
if 'gemini_api_key' not in st.session_state: st.session_state['gemini_api_key'] = ""

# AI MAPPING: Expanded BPO-Specific Root Causes -> Action Plans
rc_action_map = {
    "Product Knowledge Gap (e.g. Policies, Refunds)": ["Review KB Article", "Complete LMS Module", "Quiz on Policies"],
    "System Latency / Inefficient Navigation": ["Teach Keyboard Shortcuts", "Optimize Browser/Cache", "Dual Monitor Setup Training"],
    "Burnout / Mental Fatigue / Low Motivation": ["Schedule Wellbeing Check-in", "Review PTO Accrual", "Assign 'Easy' Queue temporarily"],
    "Process Confusion (SOP not followed)": ["Side-by-Side Shadowing", "Print & Highlight SOP", "Process Walkthrough"],
    "AHT Pressure (Dead air, long holds)": ["Call Control Coaching", "Hold-time Best Practices", "Shadow Low-AHT Performer"],
    "Missed QA Verification (Security/GDPR)": ["Compliance Refresher", "Sticky Note Reminder on Monitor", "Zero Tolerance Policy Review"],
    "Lack of Empathy / Tone of Voice": ["Soft Skills Workshop", "Empathy Phrasing Practice", "Listen to 'Golden Calls'"],
    "Ineffective Probing / Issue Identification": ["Active Listening Exercises", "Roleplay Discovery Questions", "Call Recording Review"],
    "Language / Communication Barriers": ["Scripting Assistance", "Grammar/Vocab Resource Link", "Peer-to-Peer Language Buddy"]
}

# PRE-DEFINED S.M.A.R.T. OPTIONS
opt_specific = ["-- Custom --", "Reduce AHT on complex bookings/cancellations", "Improve CSAT by showing genuine empathy", "Increase FCR (First Contact Resolution)", "Eliminate Auto-Fail/Fatal QA errors (e.g. GDPR)", "Improve Schedule Adherence & minimize Shrinkage", "Improve probing skills to identify root issues"]
opt_measurable = ["-- Custom --", "Decrease AHT by 30-45 seconds", "Achieve >= 90% CSAT for the week", "Score 100% on Compliance QA", "Maintain 95%+ Schedule Adherence", "Resolve 8/10 calls without escalation"]
opt_achievable = ["-- Custom --", "By shadowing a top performer for 1 hour", "By using the new macro templates", "By keeping the KB open on the second monitor", "By practicing call control techniques", "By taking a 15-min daily mental break"]
opt_relevant = ["-- Custom --", "Aligns with department goal to reduce customer wait times", "Directly improves Customer Loyalty & NPS", "Ensures legal/security compliance", "Reduces team workload and callback volume", "Helps agent achieve monthly performance bonus"]
opt_timebound = ["-- Custom --", "By the end of the week (Friday)", "Within the next 14 days", "By the end of the current month", "Starting next shift", "Over the next 30 days"]

lang_dict = {
    "Ελληνικά 🇬🇷": {
        "home_desc": "Δημιουργήστε νέες ομάδες ή επιλέξτε μια υπάρχουσα.",
        "create_team": "➕ Νέα Ομάδα", "enter_team_sec": "🏢 Είσοδος σε Ομάδα", "team_name_ph": "Όνομα...", "create_btn": "Δημιουργία", "enter_btn": "Είσοδος στο Workspace", "select_team": "Επιλέξτε:",
        "back_home": "🏠 Αλλαγή Ομάδας", "team_mgmt": "👥 Ρόστερ", "add_agent": "Προσθήκη", "add_btn": "➕", "sel_agent": "Ενεργός Agent", "rem_btn": "❌ Διαγραφή",
        "ws_menu": ["📝 Νέο Coaching", "🗂️ Ιστορικό Agent", "📈 KPI Review", "⚙️ Other Actions"],
        "c_type_label": "Τύπος Συνεδρίας:", "c_date_label": "Ημερομηνία Coaching:",
        "ctype_case": "🎯 Specific Case / Interaction", "ctype_weekly": "📅 Weekly Coaching", "ctype_monthly": "📊 Monthly Review", "ctype_quarterly": "📈 Quarterly Review",
        "call_id": "Call / Ticket ID (Προαιρετικό)", "rebuttal": "Αυτοαξιολόγηση Agent / Σχόλια", "assign_lms": "📚 Ανάθεση Micro-learning", "pip_gen": "⚠️ Δημιουργία P.I.P.",
        "adherence": "⏱️ Έλεγχος Adherence & Shrinkage", "extract_ag": "📥 Εξαγωγή Agent Data", "disc_action": "⚖️ Πειθαρχική Ενέργεια",
        "time_filter": "Φίλτρο Χρόνου", "tf_opts": ["Last Week", "Last Month", "Last Quarter", "Last Year"],
        "tab1": "📊 1. Μετρικές & KPIs", "tab2": "🔍 Ανάλυση Αιτιών (5 Whys)", "tab3": "📝 S.M.A.R.T. & Action Plan", "tab4": "✍️ Έλεγχος & Υπογραφές",
        "add_why": "Προσθήκη Why", "rem_why": "Αφαίρεση Why",
        "save_btn": "📥 ΑΠΟΘΗΚΕΥΣΗ SESSION",
        "ai_title": "🤖 Gemini AI Assistant", "ai_ph": "Π.χ. Δώσε μου 3 tips για το AHT...", "ai_btn": "Αποστολή 🚀",
        "chart_sel": "Τύπος Γραφήματος:", "chart_opts": ["📉 Trend Line (Εξέλιξη)", "📊 Bar Chart (Ραβδόγραμμα)", "🌊 Area Chart (Εμβαδού)", "🥧 Pie Chart (Κατανομή Αιτιών)"]
    },
    "English 🇬🇧": {
        "home_desc": "Create new teams or select an existing one.",
        "create_team": "➕ New Team", "enter_team_sec": "🏢 Enter Team", "team_name_ph": "Name...", "create_btn": "Create", "enter_btn": "Enter Workspace", "select_team": "Select:",
        "back_home": "🏠 Switch Team", "team_mgmt": "👥 Roster", "add_agent": "Add Agent", "add_btn": "➕", "sel_agent": "Active Agent", "rem_btn": "❌ Remove",
        "ws_menu": ["📝 New Coaching", "🗂️ Agent History", "📈 KPI Review", "⚙️ Other Actions"],
        "c_type_label": "Session Type:", "c_date_label": "Coaching Date:",
        "ctype_case": "🎯 Specific Case / Interaction", "ctype_weekly": "📅 Weekly Coaching", "ctype_monthly": "📊 Monthly Review", "ctype_quarterly": "📈 Quarterly Review",
        "call_id": "Call / Ticket Reference ID", "rebuttal": "Agent Self-Assessment / Rebuttal", "assign_lms": "📚 Assign LMS Micro-learning", "pip_gen": "⚠️ Generate P.I.P.",
        "adherence": "⏱️ Adherence & Shrinkage Review", "extract_ag": "📥 Extract Agent Data (Excel)", "disc_action": "⚖️ Disciplinary Action",
        "time_filter": "Time Filter", "tf_opts": ["Last Week", "Last Month", "Last Quarter", "Last Year"],
        "tab1": "📊 1. Metrics & Data (KPIs)", "tab2": "🔍 Root Causes & 5 Whys", "tab3": "📝 S.M.A.R.T. & Action Plan", "tab4": "✍️ Sign-off & Self-Reflection",
        "add_why": "Add Why", "rem_why": "Remove Why",
        "save_btn": "📥 SAVE SESSION",
        "ai_title": "🤖 Gemini AI Assistant", "ai_ph": "E.g. Give me 3 tips to improve AHT...", "ai_btn": "Send 🚀",
        "chart_sel": "Chart Type:", "chart_opts": ["📉 Trend Line", "📊 Bar Chart", "🌊 Area Chart", "🥧 Pie Chart (Root Cause Dist.)"]
    }
}

st.session_state['language'] = st.sidebar.selectbox("🌍 Language", ["English 🇬🇧", "Ελληνικά 🇬🇷"], index=["English 🇬🇧", "Ελληνικά 🇬🇷"].index(st.session_state['language']))
t = lang_dict[st.session_state['language']]

# ==========================================
# PAGE ROUTING LOGIC
# ==========================================

if st.session_state['page'] == "Home":
    
    components.html("""
        <div style="display: flex; justify-content: center; align-items: center; height: 100px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            <h1 style="color: #0083B0; font-size: 3.5rem; font-weight: bold; margin: 0;">
                <span id="text"></span><span style="border-right: 3px solid #0083B0; animation: blink 0.7s infinite;">&nbsp;</span>
            </h1>
        </div>
        <style> @keyframes blink { 50% { border-color: transparent; } } </style>
        <script>
            const words = ["Welcome", "Καλώς ήρθατε", "Bienvenidos", "Willkommen", "Bienvenue", "Välkommen"];
            let i = 0; let timer;
            function typingEffect() {
                let word = words[i].split('');
                var loopTyping = function() {
                    if (word.length > 0) { document.getElementById('text').innerHTML += word.shift(); } 
                    else { setTimeout(deletingEffect, 2000); return false; }
                    timer = setTimeout(loopTyping, 120);
                };
                loopTyping();
            }
            function deletingEffect() {
                let word = words[i].split('');
                var loopDeleting = function() {
                    if (word.length > 0) { word.pop(); document.getElementById('text').innerHTML = word.join(''); } 
                    else { i = (i + 1) % words.length; setTimeout(typingEffect, 500); return false; }
                    timer = setTimeout(loopDeleting, 60);
                };
                loopDeleting();
            }
            typingEffect();
        </script>
    """, height=120)
    
    st.markdown(f"<h4 style='text-align: center; color: gray;'>{t['home_desc']}</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_home1, col_home2 = st.columns(2)
    with col_home1:
        with st.container(border=True):
            st.subheader(t["create_team"])
            new_team_input = st.text_input("", placeholder=t["team_name_ph"])
            if st.button(t["create_btn"], type="primary") and new_team_input and new_team_input not in st.session_state['teams']:
                st.session_state['teams'][new_team_input] = [] 
                st.session_state['active_team'] = new_team_input
                st.session_state['page'] = "Workspace"
                st.rerun()
    with col_home2:
        with st.container(border=True):
            st.subheader(t["enter_team_sec"])
            team_options = list(st.session_state['teams'].keys())
            if team_options:
                selected_team = st.selectbox(t["select_team"], team_options)
                if st.button(t["enter_btn"]):
                    st.session_state['active_team'] = selected_team
                    st.session_state['page'] = "Workspace"
                    st.rerun()

else:
    active_team = st.session_state['active_team']
    team_members = st.session_state['teams'][active_team]
    
    st.sidebar.markdown("---")
    if st.sidebar.button(t["back_home"], use_container_width=True):
        st.session_state['active_team'] = None
        st.session_state['page'] = "Home"
        st.rerun()
        
    st.sidebar.markdown(f"### 📍 Team: **{active_team}**")
    st.sidebar.markdown("---")
    
    # Roster Management
    new_member = st.sidebar.text_input(t["add_agent"], placeholder="Agent Name...")
    if st.sidebar.button(t["add_btn"]):
        if new_member and new_member not in team_members:
            st.session_state['teams'][active_team].append(new_member)
            st.rerun()

    active_agent = ""
    if team_members:
        active_agent = st.sidebar.selectbox(t["sel_agent"], team_members)
        if st.sidebar.button(t["rem_btn"]):
            st.session_state['teams'][active_team].remove(active_agent)
            st.rerun()

    st.sidebar.markdown("---")
    with st.sidebar.expander("🤖 AI API Setup", expanded=False):
        if not GEMINI_AVAILABLE:
            st.error("Missing library! Run: `pip install google-generativeai`")
        api_key = st.text_input("Gemini API Key:", type="password", value=st.session_state['gemini_api_key'], help="Get it free from Google AI Studio")
        if st.button("Save Key"):
            st.session_state['gemini_api_key'] = api_key
            st.success("Key Saved!")

    # ------------------------------------------
    # ΚΥΡΙΩΣ ΟΘΟΝΗ: TEAM WORKSPACE
    # ------------------------------------------
    if st.session_state['page'] == "Workspace":
        st.title(f"Nexus Pro | {active_agent if active_agent else 'Workspace'}")
        
        if not active_agent:
            st.info("👈 Please add and select an Agent from the sidebar to open the Workspace.")
        else:
            ws_action = st.radio("", t["ws_menu"], horizontal=True, label_visibility="collapsed")
            st.divider()

            agent_history = [s for s in st.session_state['coaching_history'] if s['Agent'] == active_agent and s.get('Team') == active_team]

            # --- ΥΠΟ-ΟΘΟΝΗ 1: ΝΕΟ COACHING ---
            if ws_action == t["ws_menu"][0]:
                
                # --- COACHING TYPE & CALENDAR ---
                st.markdown("### 🗓️ Session Details")
                with st.container(border=True):
                    c_date, c_type = st.columns(2)
                    with c_date:
                        coaching_date = st.date_input(t["c_date_label"], datetime.date.today())
                    with c_type:
                        coaching_type = st.selectbox(t["c_type_label"], [t["ctype_case"], t["ctype_weekly"], t["ctype_monthly"], t["ctype_quarterly"]])
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                col_form, col_ai = st.columns([7, 3])
                
                with col_form:
                    # HIDE KPIs IF IT'S JUST A SPECIFIC CASE COACHING
                    has_kpis = coaching_type != t["ctype_case"]
                    df = pd.DataFrame(index=["CSAT", "QA"]) # Default empty df
                    df['MTD'] = 0.0
                    
                    if has_kpis:
                        with st.expander(t["tab1"], expanded=True):
                            c_id, c_csat, c_qa, c_aht = st.columns(4)
                            with c_id: call_ref = st.text_input(t["call_id"], placeholder="e.g. INC-10293")
                            with c_csat: t_csat = st.number_input("Target CSAT %", 70.0, 100.0, 85.0)
                            with c_qa: t_qa = st.number_input("Target QA %", 70.0, 100.0, 90.0)
                            with c_aht: t_aht = st.number_input("Target AHT (sec)", value=280.0)
                            
                            st.markdown("---")
                            w_data = {}
                            w_cols = st.columns(4)
                            for i in range(1, 5):
                                with w_cols[i-1]:
                                    st.markdown(f"**Week {i}**")
                                    c = st.number_input(f"CSAT %", value=float(t_csat), key=f"c{i}")
                                    q = st.number_input(f"QA %", value=float(t_qa), key=f"q{i}")
                                    w_data[f"W{i}"] = [c, q]
                            
                            df = pd.DataFrame(w_data, index=["CSAT", "QA"])
                            df['MTD'] = df.mean(axis=1)
                    else:
                        call_ref = st.text_input(t["call_id"], placeholder="e.g. Interaction ID")

                    with st.expander(t["tab2"], expanded=not has_kpis): # Expand by default if KPIs are hidden
                        for w in range(st.session_state['num_whys']):
                            st.text_input(f"Why {w+1}?", key=f"why_{w}")
                            
                        # Προσθήκη / Αφαίρεση Why Κουμπιά
                        btn_w1, btn_w2, _ = st.columns([2, 2, 6])
                        with btn_w1:
                            if st.session_state['num_whys'] < 5:
                                if st.button("➕ " + t["add_why"], use_container_width=True): 
                                    st.session_state['num_whys'] += 1; st.rerun()
                        with btn_w2:
                            if st.session_state['num_whys'] > 1:
                                if st.button("➖ " + t["rem_why"], use_container_width=True): 
                                    st.session_state['num_whys'] -= 1; st.rerun()
                        
                        st.markdown("---")
                        base_roots = list(rc_action_map.keys())
                        c_rc1, c_rc2 = st.columns(2)
                        with c_rc1:
                            sel_pri_rc = st.selectbox("Primary Root Cause:", ["-- Custom --"] + base_roots + st.session_state['custom_roots'])
                            fin_pri_rc = st.text_input("Define Custom Primary:", key="pri_rc_inp") if sel_pri_rc == "-- Custom --" else sel_pri_rc
                        with c_rc2:
                            sel_sec_rc = st.selectbox("Secondary Root Cause:", ["-- None --", "-- Custom --"] + base_roots + st.session_state['custom_roots'])
                            fin_sec_rc = st.text_input("Define Custom Secondary:", key="sec_rc_inp") if sel_sec_rc == "-- Custom --" else (sel_sec_rc if sel_sec_rc != "-- None --" else "None")

                    with st.expander(t["tab3"]):
                        s1, s2 = st.columns(2)
                        with s1: 
                            sel_s = st.selectbox("Specific:", opt_specific)
                            fin_s = st.text_input("Define Custom Specific:", key="s_cust") if sel_s == "-- Custom --" else sel_s
                            
                            sel_m = st.selectbox("Measurable:", opt_measurable)
                            fin_m = st.text_input("Define Custom Measurable:", key="m_cust") if sel_m == "-- Custom --" else sel_m
                            
                            sel_a = st.selectbox("Achievable:", opt_achievable)
                            fin_a = st.text_input("Define Custom Achievable:", key="a_cust") if sel_a == "-- Custom --" else sel_a
                            
                        with s2: 
                            sel_r = st.selectbox("Relevant:", opt_relevant)
                            fin_r = st.text_input("Define Custom Relevant:", key="r_cust") if sel_r == "-- Custom --" else sel_r
                            
                            sel_t = st.selectbox("Time-bound:", opt_timebound)
                            fin_t = st.text_input("Define Custom Time-bound:", key="t_cust") if sel_t == "-- Custom --" else sel_t
                        
                        st.markdown("---")
                        suggested_actions = rc_action_map.get(fin_pri_rc, [])
                        selected_action = st.selectbox("Strategic Action Plan:", ["-- Custom --"] + suggested_actions + st.session_state['custom_actions'])
                        final_action = st.text_input("Define Custom Action Plan:", key="fin_ap_inp") if selected_action == "-- Custom --" else selected_action

                    with st.expander(t["tab4"]):
                        agent_rebuttal = st.text_area(t["rebuttal"], placeholder="Agent's perspective or agreement notes...")
                        st.markdown("---")
                        col_sig1, col_sig2 = st.columns(2)
                        with col_sig1: agent_agrees = st.checkbox("Agent acknowledges and agrees.")
                        with col_sig2: agent_initials = st.text_input("Agent Initials", max_chars=3)

                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("📥 " + t["save_btn"], use_container_width=True, type="primary"):
                        if not agent_agrees or not agent_initials:
                            st.error("❌ Action Required: Agent must agree and provide initials.")
                        else:
                            if fin_pri_rc and fin_pri_rc != "-- Custom --" and fin_pri_rc not in base_roots and fin_pri_rc not in st.session_state['custom_roots']: st.session_state['custom_roots'].append(fin_pri_rc)
                            if final_action and final_action != "-- Custom --" and final_action not in rc_action_map.get(fin_pri_rc, []) and final_action not in st.session_state['custom_actions']: st.session_state['custom_actions'].append(final_action)
                            
                            session_data = {
                                "Date": str(coaching_date), "Type": coaching_type, "Team": active_team, "Agent": active_agent,
                                "Call ID": call_ref, 
                                "CSAT": round(df.loc['CSAT', 'MTD'], 1) if has_kpis else None, 
                                "QA": round(df.loc['QA', 'MTD'], 1) if has_kpis else None,
                                "Primary Root Cause": fin_pri_rc, "Action Plan": final_action, 
                                "SMART_S": fin_s, "SMART_M": fin_m, "SMART_A": fin_a, "SMART_R": fin_r, "SMART_T": fin_t,
                                "Agent Notes": agent_rebuttal, "Signed": agent_initials
                            }
                            st.session_state['coaching_history'].append(session_data)
                            st.session_state['num_whys'] = 1
                            st.success("✅ Record successfully logged!")

                # --- ΔΕΞΙΑ ΣΤΗΛΗ: AI ASSISTANT PANEL ---
                with col_ai:
                    with st.container(border=True):
                        st.markdown(f"### {t['ai_title']}")
                        
                        chat_container = st.container(height=400)
                        with chat_container:
                            if not st.session_state['ai_chat_history']:
                                st.info("Hello! Ask me to generate an action plan, summarize KPIs, or roleplay a scenario.")
                            for msg in st.session_state['ai_chat_history']:
                                role = "🧑‍💼" if msg['role'] == "user" else "🤖"
                                st.markdown(f"**{role}:** {msg['content']}")
                        
                        user_prompt = st.text_input("", placeholder=t["ai_ph"], key="ai_input")
                        if st.button(t["ai_btn"], use_container_width=True):
                            if user_prompt:
                                st.session_state['ai_chat_history'].append({"role": "user", "content": user_prompt})
                                
                                if st.session_state['gemini_api_key'] and GEMINI_AVAILABLE:
                                    try:
                                        genai.configure(api_key=st.session_state['gemini_api_key'])
                                        model = genai.GenerativeModel('gemini-1.5-flash')
                                        context_prompt = f"Act as an expert BPO Team Leader. You are helping coach an agent named {active_agent}. Keep your answer professional, concise, and formatting-rich. Here is the query: {user_prompt}"
                                        response = model.generate_content(context_prompt)
                                        ai_response = response.text
                                    except Exception as e:
                                        ai_response = f"❌ API Error: {e}. Check if your API Key is valid."
                                else:
                                    ai_response = "⚠️ No API Key found! Please paste your Google Gemini API Key in the Sidebar (AI API Setup) to enable real responses."
                                
                                st.session_state['ai_chat_history'].append({"role": "ai", "content": ai_response})
                                st.rerun() 

            # --- ΥΠΟ-ΟΘΟΝΗ 2: COACHING HISTORY ---
            elif ws_action == t["ws_menu"][1]:
                st.subheader(f"🗂️ History: {active_agent}")
                if len(agent_history) > 0:
                    h_df = pd.DataFrame(agent_history)
                    
                    # --- FIX: Backward Compatibility για παλιά δεδομένα ---
                    if 'Type' not in h_df.columns:
                        h_df['Type'] = "Legacy Record"
                    if 'Date' not in h_df.columns:
                        h_df['Date'] = "Unknown Date"
                    # ------------------------------------------------------
                        
                    # Reorder columns safely
                    cols = ['Date', 'Type'] + [c for c in h_df.columns if c not in ['Date', 'Type']]
                    st.dataframe(h_df[cols], use_container_width=True)
                    
                    st.markdown("### Edit / Delete Records")
                    col_ed1, col_ed2 = st.columns(2)
                    with col_ed1:
                        # Χρήση του .get() για ασφάλεια σε περίπτωση που λείπουν πεδία από παλιές εγγραφές
                        del_opts = [f"{st.session_state['coaching_history'].index(s)}: {s.get('Date', 'No Date')} ({s.get('Type', 'Legacy')}) - {s.get('Primary Root Cause', '')}" for s in agent_history]
                        sel_record = st.selectbox("Select Record:", del_opts)
                        idx_to_mod = int(sel_record.split(":")[0])
                        
                    with col_ed2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("❌ Delete Record", type="primary"):
                            st.session_state['coaching_history'].pop(idx_to_mod)
                            st.rerun()
                            
                    with st.expander("✏️ Quick Edit Action Plan"):
                        new_action = st.text_input("Update Action Plan:", value=st.session_state['coaching_history'][idx_to_mod].get('Action Plan', ''))
                        if st.button("Update"):
                            st.session_state['coaching_history'][idx_to_mod]['Action Plan'] = new_action
                            st.success("Updated!")
                            st.rerun()
                else:
                    st.info("No historical data found for this agent.")

            # --- ΥΠΟ-ΟΘΟΝΗ 3: KPI REVIEW (ΜΕ ΕΠΙΛΟΓΗ ΓΡΑΦΗΜΑΤΟΣ & TIME FILTERS) ---
            elif ws_action == t["ws_menu"][2]:
                st.subheader("📈 KPI Performance Review")
                if len(agent_history) > 0:
                    c_f1, c_f2 = st.columns(2)
                    with c_f1:
                        time_f = st.radio(t["time_filter"], t["tf_opts"], horizontal=True)
                    with c_f2:
                        chart_type = st.selectbox(t["chart_sel"], t["chart_opts"])
                    
                    hist_df = pd.DataFrame(agent_history)
                    
                    # --- FIX: Ασφαλής μετατροπή ημερομηνιών για αποφυγή σφαλμάτων ---
                    hist_df['Date'] = pd.to_datetime(hist_df['Date'], errors='coerce').dt.date
                    hist_df = hist_df.dropna(subset=['Date']) # Διαγραφή εγγραφών με μη-έγκυρη ημερομηνία μόνο για το γράφημα
                    # ----------------------------------------------------------------
                    
                    today = datetime.date.today()
                    if time_f == t["tf_opts"][0]: # Last Week
                        cutoff_date = today - datetime.timedelta(days=7)
                    elif time_f == t["tf_opts"][1]: # Last Month
                        cutoff_date = today - datetime.timedelta(days=30)
                    elif time_f == t["tf_opts"][2]: # Last Quarter
                        cutoff_date = today - datetime.timedelta(days=90)
                    else: # Last Year
                        cutoff_date = today - datetime.timedelta(days=365)
                        
                    filtered_df = hist_df[hist_df['Date'] >= cutoff_date]
                    filtered_df = filtered_df.sort_values('Date')
                    
                    st.markdown("---")
                    
                    if filtered_df.empty:
                        st.warning(f"No coaching data found for the selected period ({time_f}).")
                    else:
                        if "Pie" in chart_type:
                            pie_data = filtered_df['Primary Root Cause'].value_counts().reset_index()
                            pie_data.columns = ['Root Cause', 'Count']
                            fig = px.pie(pie_data, names='Root Cause', values='Count', title=f"Root Cause Distribution ({time_f})", hole=0.4)
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            kpi_df = filtered_df.dropna(subset=['CSAT', 'QA'])
                            
                            if kpi_df.empty:
                                st.info("No KPI data available for this period (Only Case/Behavioral coaching found).")
                            else:
                                if "Trend" in chart_type:
                                    fig = px.line(kpi_df, x='Date', y=['CSAT', 'QA'], markers=True, title=f"Performance Trend ({time_f})")
                                elif "Bar" in chart_type:
                                    fig = px.bar(kpi_df, x='Date', y=['CSAT', 'QA'], barmode='group', title=f"Performance Comparison ({time_f})")
                                elif "Area" in chart_type:
                                    fig = px.area(kpi_df, x='Date', y=['CSAT', 'QA'], title=f"Performance Area ({time_f})")
                                
                                fig.update_layout(yaxis_title="Score %", xaxis_title="Session Date")
                                st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Complete some coaching sessions first to unlock KPI Trends.")

            # --- ΥΠΟ-ΟΘΟΝΗ 4: OTHER ACTIONS ---
            elif ws_action == t["ws_menu"][3]:
                st.subheader("⚙️ Agent Management & Tools")
                
                c_o1, c_o2 = st.columns(2)
                with c_o1:
                    with st.container(border=True):
                        st.markdown(f"**{t['assign_lms']}**")
                        lms_module = st.selectbox("Select Module:", ["Empathy 101", "De-escalation Tactics", "System Navigation", "Security Compliance"])
                        if st.button("Send Assignment"): st.success(f"Assigned {lms_module} to {active_agent}")
                        
                    with st.container(border=True):
                        st.markdown(f"**{t['adherence']}**")
                        st.metric("Schedule Adherence (MTD)", "94.2%", "-1.8%")
                        st.metric("Shrinkage (MTD)", "12.5%", "+0.5%")
                        
                with c_o2:
                    with st.container(border=True):
                        st.markdown(f"**{t['pip_gen']}**")
                        pip_reason = st.text_input("Reason for P.I.P:")
                        if st.button("Generate P.I.P. PDF"): st.info("PDF Generation triggered. Check downloads.")
                        
                    with st.container(border=True):
                        st.markdown(f"**{t['disc_action']}**")
                        disc_lvl = st.selectbox("Action Level:", ["Verbal Warning", "Written Warning", "Final Warning"])
                        if st.button("Log Disciplinary"): st.warning(f"{disc_lvl} logged for {active_agent}.")
                        
                if st.button(t["extract_ag"], use_container_width=True):
                    if len(agent_history) > 0:
                        csv = pd.DataFrame(agent_history).to_csv(index=False).encode('utf-8-sig')
                        st.download_button("Download Now", data=csv, file_name=f"{active_agent}_Data.csv", mime="text/csv")
                    else:
                        st.error("No data to extract.")