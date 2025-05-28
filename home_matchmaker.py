# Home Matchmaker - Streamlit Survey App
# Enhanced UI with step-by-step navigation, progress bar, and restart feature

import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="Home Matchmaker Survey", layout="wide")

# CSS Styling
st.markdown("""
    <style>
    body {
        background-color: #6699CC;
        color: #ffffff;
    }
    .stApp {
        background-color: #6699CC;
        padding: 2rem;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 1.1rem;
    }
    .stButton > button {
        background-color: #004080;
        color: white;
        font-size: 1rem;
        padding: 0.5rem 1.5rem;
        border-radius: 6px;
        border: none;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #ffffff;
    }
    .result-card {
        background-color: #ffffff;
        color: #000000;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
    }
    a {
        color: #004080;
        text-decoration: none;
        font-weight: 600;
    }
    a:hover {
        text-decoration: underline;
    }
    .home-image {
        width: 100%;
        height: auto;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("🏡 Bernie and Clem's Find a Home Tool!")
st.markdown("### Begin by telling us what you like — this survey will guide you to homes and communities that fit your needs.")

# Initialize session state for navigation and form values
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.responses = {}

# Restart functionality
if st.button("🔄 Start a New Search"):
    st.session_state.step = 1
    st.session_state.responses = {}
    st.experimental_rerun()

# Progress bar
total_steps = 5
progress = int((st.session_state.step / total_steps) * 100)
st.progress(progress)

# Step 1
if st.session_state.step == 1:
    region = st.multiselect("Which regions of the U.S. are you open to?", [
        "Southeast", "Southwest", "Pacific Coast", "Midwest", "Northeast", "Mountain West"])
    if st.button("Next"):
        st.session_state.responses['region'] = region
        st.session_state.step += 1
        st.experimental_rerun()

# Step 2
elif st.session_state.step == 2:
    climate = st.multiselect("What climate do you prefer?", [
        "Warm year-round", "Four seasons", "Mild winters", "Coastal", "Mountain", "Dry/Desert"])
    if st.button("Next"):
        st.session_state.responses['climate'] = climate
        st.session_state.step += 1
        st.experimental_rerun()

# Step 3
elif st.session_state.step == 3:
    home_type = st.multiselect("What type of home do you prefer?", [
        "Single-family", "Townhome", "Condo", "55+ Community"])
    if st.button("Next"):
        st.session_state.responses['home_type'] = home_type
        st.session_state.step += 1
        st.experimental_rerun()

# Step 4
elif st.session_state.step == 4:
    sqft = st.selectbox("Ideal home square footage:", [
        "< 1500", "1500–2000", "2000–2500", "> 2500"])
    beds = st.slider("Minimum number of bedrooms", 1, 5, 3)
    baths = st.slider("Minimum number of bathrooms", 1, 4, 2)
    if st.button("Next"):
        st.session_state.responses['sqft'] = sqft
        st.session_state.responses['beds'] = beds
        st.session_state.responses['baths'] = baths
        st.session_state.step += 1
        st.experimental_rerun()

# Step 5 - Completion
elif st.session_state.step == 5:
    st.success("🎉 Thank you! Your preferences have been saved. You are ready to view your matches.")
    st.json(st.session_state.responses)
    if st.button("🔍 Show My Matches"):
        st.markdown("### Matches (sample)")
        mock_results = [
            {
                "location": "Summerville, SC",
                "score": 92,
                "home": "3BR / 2BA | 2100 sq ft | $430K",
                "features": "Single-story, Open Floor Plan, Screened Porch",
                "link": "https://www.realtor.com/realestateandhomes-detail/2100-Preserve-Way_Summerville_SC_29483_M95867-16314",
                "image": "https://cdn.realtor.com/medias/2100-preserve-way.jpg"
            }
        ]
        for result in mock_results:
            st.markdown(f"""
            <div class='result-card'>
                <img src='{result['image']}' alt='Home Image' class='home-image'/>
                <h4>{result['location']} — Match Score: {result['score']}%</h4>
                <p><strong>{result['home']}</strong><br/>
                Features: {result['features']}<br/>
                <a href='{result['link']}' target='_blank'>🔗 View Listing</a></p>
            </div>
            """, unsafe_allow_html=True)
        st.download_button("📥 Download My Matches", data=json.dumps(mock_results, indent=2), file_name="home_match_results.json")
