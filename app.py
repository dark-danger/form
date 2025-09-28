import streamlit as st
from datetime import date

# --- Page Config ---
st.set_page_config(page_title="GDSC Event Registration", page_icon="🎉", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    body { background-color: #f9f9f9; font-family: 'Segoe UI', sans-serif; }
    .header-container { display:flex; justify-content:space-between; align-items:center; 
                        padding:15px 30px; background-color:#ffffff; border-radius:12px; 
                        margin:auto; margin-bottom:30px; max-width:1000px; box-shadow:0 2px 6px rgba(0,0,0,0.1);}
    .header-title { font-size:26px; font-weight:bold; color:#202124; }
    .center-container { max-width:900px; margin:auto; }
    .event-card { background:#fff; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.08); 
                  padding:15px; margin-bottom:25px; text-align:center; transition: transform 0.2s ease-in-out; }
    .event-card:hover { transform: translateY(-4px); box-shadow:0 4px 12px rgba(0,0,0,0.15); }
    .event-title { font-size:18px; font-weight:600; margin:10px 0; color:#111; }
    .event-buttons { display:flex; justify-content:space-around; margin-top:10px; }
    </style>
""", unsafe_allow_html=True)

# --- Events Data ---
events = [
    {"name": "Google Sparks", "image": "images/1.png", "desc": "Run through the city streets.", 
     "rules": ["Wear shoes", "Follow route", "No cheating"]},
    {"name": "Tech Quizathon", "image": "images/2.png", "desc": "Short fun quiz run.", 
     "rules": ["Friendly pace", "Hydrate", "No skipping"]},
    {"name": "Robo War", "image": "images/3.png", "desc": "Battle of robots in arena.", 
     "rules": ["Team register", "Safety first", "No outside damage"]},
    {"name": "Startup Pitch", "image": "images/4.png", "desc": "Pitch your startup idea.", 
     "rules": ["5 min pitch", "Slides allowed", "Q&A mandatory"]}
]

# --- Session State ---
if "view" not in st.session_state:
    st.session_state.view = "gallery"
if "selected_event" not in st.session_state:
    st.session_state.selected_event = None

# --- Functions ---
def go_to_form(event): st.session_state.selected_event, st.session_state.view = event, "form"
def go_to_info(event): st.session_state.selected_event, st.session_state.view = event, "info"
def go_back(): st.session_state.selected_event, st.session_state.view = None, "gallery"

# --- Header ---
st.markdown("""
    <div class="header-container">
        <div class="header-title">🎉 GDSC Event Registration</div>
        <img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" width="120">
    </div>
""", unsafe_allow_html=True)

# --- Gallery View ---
if st.session_state.view == "gallery":
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    
    st.subheader("🔥 Upcoming Events")
    
    # Loop through events 2 per row
    for i in range(0, len(events), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(events):
                ev = events[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="event-card">
                            <img src="{ev['image']}" width="100%">
                            <div class="event-title">{ev['name']}</div>
                            <p style="font-size:14px; color:#555;">{ev['desc']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Buttons side by side
                    col_btn1, col_btn2 = st.columns([1,1])
                    with col_btn1:
                        if st.button("Register", key=f"reg_{i+j}"): go_to_form(ev["name"])
                    with col_btn2:
                        if st.button("Event Info", key=f"info_{i+j}"): go_to_info(ev["name"])
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Registration Form View ---
elif st.session_state.view == "form":
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    st.subheader(f"📝 Register for {st.session_state.selected_event}")
    
    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        dob = st.date_input("Date of Birth", min_value=date(1970,1,1))
        phone = st.text_input("Mobile No.")
        waiver = st.checkbox("I agree to the terms and conditions")
        
        col1, col2 = st.columns(2)
        with col1: submit = st.form_submit_button("✅ Submit")
        with col2: back = st.form_submit_button("⬅ Back")
        
        if back: go_back()
        if submit:
            if not waiver: st.error("⚠ Please agree to waiver")
            elif not name or not email: st.error("⚠ Fill all fields")
            else: st.success(f"🎉 Registered for {st.session_state.selected_event}!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Event Info View ---
elif st.session_state.view == "info":
    ev = next(e for e in events if e["name"] == st.session_state.selected_event)
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    
    st.subheader(f"📘 {ev['name']} Info")
    st.markdown(f"**Description:** {ev['desc']}")
    st.markdown("**Rules:**")
    for r in ev["rules"]:
        st.markdown(f"- {r}")
    
    if st.button("⬅ Back to Events"): go_back()
    st.markdown('</div>', unsafe_allow_html=True)
