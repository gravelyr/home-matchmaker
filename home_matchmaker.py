# Home Matchmaker - Streamlit Survey App
# This is the prototype script for your hosted tool with enhanced UI and on-screen results

import streamlit as st
import pandas as pd
import json
from datetime import datetime

# MUST be the first Streamlit command
st.set_page_config(page_title="Home Matchmaker Survey", layout="wide")

# Inject CSS for custom theming and visuals
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #f5f7fa, #c3cfe2);
        color: #333;
    }
    .stApp {
        background: linear-gradient(to bottom, #f8f9fa, #e0e0e0);
        padding: 2rem;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton > button {
        background-color: #0071e3;
        color: white;
        font-size: 1rem;
        padding: 0.5rem 1.5rem;
        border-radius: 6px;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #0052cc;
    }
    .result-card {
        background-color: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏡 Find Your Ideal Home and Location")
st.markdown("Use this survey to help determine your best match for your next home and neighborhood.")

# Initialize dummy values to avoid NameError
region = []
climate = []
community_size = ""
proximity = []
priority_areas = ""
home_type = []
sqft = ""
beds = 0
baths = 0
floorplan = []
outdoor = []
amenities = []
lifestyle = []
budget = ""
monthly = ""
tax_pref = []
loan_type = ""
reasons = []
must_haves = ""
nice_haves = ""

if st.button("🔍 Find My Matches"):
    survey_data = {
        "timestamp": datetime.now().isoformat(),
        "region": region,
        "climate": climate,
        "community_size": community_size,
        "proximity": proximity,
        "priority_areas": priority_areas,
        "home_type": home_type,
        "sqft": sqft,
        "beds": beds,
        "baths": baths,
        "floorplan": floorplan,
        "outdoor": outdoor,
        "amenities": amenities,
        "lifestyle": lifestyle,
        "budget": budget,
        "monthly": monthly,
        "tax_pref": tax_pref,
        "loan_type": loan_type,
        "reasons": reasons,
        "must_haves": must_haves,
        "nice_haves": nice_haves
    }

    st.success("Matches generated below based on your preferences!")

    # Mock match results for prototype display
    mock_results = [
        {
            "location": "Summerville, SC",
            "score": 92,
            "home": "3BR / 2BA | 2100 sq ft | $430K",
            "features": "Single-story, Open Floor Plan, Screened Porch",
            "link": "https://www.realtor.com/realestateandhomes-detail/Summerville_SC"
        },
        {
            "location": "Asheville, NC",
            "score": 88,
            "home": "2BR / 2BA | 1800 sq ft | $395K",
            "features": "Mountain View, 55+ Community, Garden Area",
            "link": "https://www.realtor.com/realestateandhomes-detail/Asheville_NC"
        },
        {
            "location": "Bluffton, SC",
            "score": 84,
            "home": "4BR / 3BA | 2400 sq ft | $520K",
            "features": "Gated Entry, Resort-Style Pool, Golf Nearby",
            "link": "https://www.realtor.com/realestateandhomes-detail/Bluffton_SC"
        }
    ]

    for result in mock_results:
        st.markdown(f"""
        <div class='result-card'>
            <h4>{result['location']} — Match Score: {result['score']}%</h4>
            <p><strong>{result['home']}</strong><br/>
            Features: {result['features']}<br/>
            <a href='{result['link']}' target='_blank'>🔗 View Listing</a></p>
        </div>
        """, unsafe_allow_html=True)

    st.download_button("📥 Download My Matches", data=json.dumps(mock_results, indent=2), file_name="home_match_results.json")
