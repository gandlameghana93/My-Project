import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Skill Exchange Platform", page_icon="🤝", layout="wide")

# ---------------------------------------------------------
# CUSTOM HTML / CSS STYLING FOR ATTRACTIVE LOOK
# ---------------------------------------------------------
custom_css = """
<style>
    /* Main Background & Font */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Gradient Style */
    .main-header {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
    }
    .main-header p {
        margin-top: 8px;
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* Streamlit Cards Styling Override */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: white !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    
    /* Card Hover Effect */
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
        border-color: #cbd5e1 !important;
    }

    /* Custom Badges */
    .badge-offer {
        background-color: #dcfce7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-want {
        background-color: #fef3c7;
        color: #92400e;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }

    /* Custom Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        opacity: 0.95 !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4) !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER SECTION WITH GRADIENT
# ---------------------------------------------------------
st.markdown("""
    <div class="main-header">
        <h1>🤝 Peer Skill Exchange Platform</h1>
        <p>Barter your skills • Learn for free • Grow together</p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 1. INITIALIZE SESSION STATE (Mock Database)
# ---------------------------------------------------------
if "current_user" not in st.session_state:
    st.session_state.current_user = {
        "Name": "You (Logged In)",
        "Offer": ["Python", "Machine Learning", "Data Analysis"],
        "Want": ["Guitar", "UI/UX Design", "French"]
    }

if "users" not in st.session_state:
    st.session_state.users = [
        {"id": 1, "Name": "Priya Patel", "Offer": ["Guitar", "Music Theory"], "Want": ["Python", "Data Analysis"], "Email": "priya@gmail.com"},
        {"id": 2, "Name": "Anand Verma", "Offer": ["UI/UX Design", "Figma"], "Want": ["Node.js", "Python"], "Email": "anand@gmail.com"},
        {"id": 3, "Name": "Rahul Sharma", "Offer": ["French", "Spoken English"], "Want": ["Machine Learning"], "Email": "rahul@gmail.com"},
        {"id": 4, "Name": "Sneha Reddy", "Offer": ["Java", "Spring Boot"], "Want": ["React", "UI/UX Design"], "Email": "sneha@gmail.com"},
    ]

if "requests" not in st.session_state:
    st.session_state.requests = []

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = {
        "Priya Patel": [
            {"sender": "Priya Patel", "text": "Hi! I saw you offer Python. Can we exchange for Guitar lessons?"}
        ]
    }

# ---------------------------------------------------------
# 2. MATCH SCORE ALGORITHM
# ---------------------------------------------------------
def calculate_match_score(user_offer, user_want, peer_offer, peer_want):
    my_offer_set = set([s.lower().strip() for s in user_offer])
    my_want_set = set([s.lower().strip() for s in user_want])
    peer_offer_set = set([s.lower().strip() for s in peer_offer])
    peer_want_set = set([s.lower().strip() for s in peer_want])

    i_can_learn = my_want_set.intersection(peer_offer_set)
    they_can_learn = my_offer_set.intersection(peer_want_set)

    total_possible_matches = max(len(my_want_set) + len(peer_want_set), 1)
    matched_items = len(i_can_learn) + len(they_can_learn)

    if len(i_can_learn) > 0 and len(they_can_learn) > 0:
        score = min(100, int((matched_items / total_possible_matches) * 100) + 50)
    elif len(i_can_learn) > 0 or len(they_can_learn) > 0:
        score = 50
    else:
        score = 10

    return score, list(i_can_learn), list(they_can_learn)

# ---------------------------------------------------------
# 3. SIDEBAR (Your Profile Info)
# ---------------------------------------------------------
st.sidebar.header("👤 Active Profile")
st.sidebar.info(f"**User:** {st.session_state.current_user['Name']}")
st.sidebar.write(f"🟢 **Offering:** {', '.join(st.session_state.current_user['Offer'])}")
st.sidebar.write(f"🟡 **Seeking:** {', '.join(st.session_state.current_user['Want'])}")

st.sidebar.divider()
st.sidebar.header("➕ Add New Member")
with st.sidebar.form("add_user_form"):
    new_name = st.text_input("Name")
    new_offer = st.text_input("Teaches (comma separated)")
    new_want = st.text_input("Wants (comma separated)")
    new_email = st.text_input("Email")
    submitted = st.form_submit_button("Add User")

    if submitted and new_name:
        st.session_state.users.append({
            "id": len(st.session_state.users) + 1,
            "Name": new_name,
            "Offer": [s.strip() for s in new_offer.split(",") if s],
            "Want": [s.strip() for s in new_want.split(",") if s],
            "Email": new_email
        })
        st.sidebar.success(f"{new_name} added successfully!")

# ---------------------------------------------------------
# 4. MAIN TABS
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["🎯 Smart Matches", "📩 Exchange Requests", "💬 Live Chat"])

# --- TAB 1: SMART MATCHES ---
with tab1:
    st.caption("Algorithmic Ranking based on Skill Overlap Score")

    ranked_users = []
    my_user = st.session_state.current_user
    
    for peer in st.session_state.users:
        score, i_learn, they_learn = calculate_match_score(
            my_user["Offer"], my_user["Want"], peer["Offer"], peer["Want"]
        )
        ranked_users.append({
            **peer,
            "match_score": score,
            "i_learn": i_learn,
            "they_learn": they_learn
        })

    ranked_users = sorted(ranked_users, key=lambda x: x["match_score"], reverse=True)

    cols = st.columns(2)
    for idx, user in enumerate(ranked_users):
        col = cols[idx % 2]
        with col:
            with st.container(border=True):
                # User Name & Match Score
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"### {user['Name']}")
                with c2:
                    score = user["match_score"]
                    if score >= 80:
                        st.markdown(f"<span style='color:#15803d; font-weight:bold;'>🔥 {score}% Match</span>", unsafe_allow_html=True)
                    elif score >= 50:
                        st.markdown(f"<span style='color:#1d4ed8; font-weight:bold;'>⚡ {score}% Match</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span style='color:#b45309; font-weight:bold;'>💡 {score}% Match</span>", unsafe_allow_html=True)

                st.progress(score / 100)

                # HTML Badges for Skills
                st.markdown(f"<div><span class='badge-offer'>Teaches</span> <b>{', '.join(user['Offer'])}</b></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='margin-top:6px;'><span class='badge-want'>Wants</span> <b>{', '.join(user['Want'])}</b></div>", unsafe_allow_html=True)

                # Expandable Reason
                if user["i_learn"] or user["they_learn"]:
                    with st.expander("🔍 Match Details"):
                        if user["i_learn"]:
                            st.write(f"• You learn: **{', '.join(user['i_learn'])}**")
                        if user["they_learn"]:
                            st.write(f"• You teach: **{', '.join(user['they_learn'])}**")

                st.write("")
                if st.button(f"Request Swap 🔄", key=f"btn_{user['id']}"):
                    st.session_state.requests.append({
                        "To": user["Name"],
                        "Match Score": f"{score}%",
                        "Status": "PENDING ⏳"
                    })
                    st.toast(f"Exchange Request Sent to {user['Name']}!", icon="🎉")

# --- TAB 2: REQUESTS STATUS ---
with tab2:
    st.subheader("Sent Exchange Requests")
    if st.session_state.requests:
        st.dataframe(pd.DataFrame(st.session_state.requests), use_container_width=True)
    else:
        st.info("No requests sent yet. Go to 'Smart Matches' tab to send requests.")

# --- TAB 3: LIVE CHAT ---
with tab3:
    st.subheader("💬 Peer-to-Peer Skill Chat")
    peer_names = [u["Name"] for u in st.session_state.users]
    selected_peer = st.selectbox("Select peer to chat:", peer_names)

    if selected_peer not in st.session_state.chat_messages:
        st.session_state.chat_messages[selected_peer] = []

    chat_container = st.container(height=300, border=True)
    with chat_container:
        messages = st.session_state.chat_messages[selected_peer]
        if not messages:
            st.caption("No messages yet. Start the conversation!")
        for msg in messages:
            if msg["sender"] == "You":
                st.chat_message("user").write(msg["text"])
            else:
                st.chat_message("assistant").write(f"**{msg['sender']}:** {msg['text']}")

    prompt = st.chat_input(f"Message {selected_peer}...")
    if prompt:
        st.session_state.chat_messages[selected_peer].append({"sender": "You", "text": prompt})
        st.session_state.chat_messages[selected_peer].append({
            "sender": selected_peer, 
            "text": f"Hey! Thanks for messaging. Let's schedule our skill swap session!"
        })
        st.rerun()