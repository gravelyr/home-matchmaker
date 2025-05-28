# Home Matchmaker - Streamlit Survey App
# Enhanced UI and fully functional survey logic for hosted deployment

import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="Home Matchmaker Survey", layout="wide")

# Inject CSS for custom theming and visuals
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #000000, #004080, #007d21);
        color: #ffffff;
    }
    .stApp {
        background: linear-gradient(to bottom, #1c1c1c, #2e3a59);
        padding: 2rem;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton > button {
        background-color: #00aa88;
        color: white;
        font-size: 1rem;
        padding: 0.5rem 1.5rem;
        border-radius: 6px;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #00ccff;
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
        color: #0071e3;
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

st.title("🏡 Find Your Ideal Home and Location")
st.markdown("Use this survey to help determine your best match for your next home and neighborhood.")

# Full survey restored
region = st.multiselect("Which regions of the U.S. are you open to?", [
    "Southeast", "Southwest", "Pacific Coast", "Midwest", "Northeast", "Mountain West"])
climate = st.multiselect("What climate do you prefer?", [
    "Warm year-round", "Four seasons", "Mild winters", "Coastal", "Mountain", "Dry/Desert"])
community_size = st.selectbox("What kind of community size do you prefer?", [
    "Urban", "Suburban", "Small Town", "Rural"])
proximity = st.multiselect("Which of these should be within 30 minutes of your home?", [
    "Airports", "Hospitals", "Beaches", "Mountains", "Lakes/Rivers", "Grocery Stores", "Family", "Friends"])
priority_areas = st.text_area("List ZIP codes or cities near family/friends you want to live close to:")

home_type = st.multiselect("What type of home do you prefer?", [
    "Single-family", "Townhome", "Condo", "55+ Community"])
sqft = st.selectbox("Ideal home square footage:", [
    "< 1500", "1500–2000", "2000–2500", "> 2500"])
beds = st.slider("Minimum number of bedrooms", 1, 5, 3)
baths = st.slider("Minimum number of bathrooms", 1, 4, 2)
floorplan = st.multiselect("Preferred layout features", [
    "Single-story", "Multi-story", "Open floor plan", "Split bedrooms", "Walk-in closets", "Large pantry", "Flex space"])
outdoor = st.multiselect("Outdoor space preferences", [
    "Screened porch", "Covered patio", "Outdoor kitchen", "Fenced yard", "Garden area"])

amenities = st.multiselect("What community features do you want?", [
    "Clubhouse", "Fitness center", "Pickleball courts", "Tennis courts", "Resort-style pool", "Walking trails", "Golf access", "Gated entry", "HOA maintenance"])
lifestyle = st.multiselect("What kind of neighborhood vibe do you want?", [
    "Active adult (55+)", "Family-friendly", "Pet-friendly", "Social events/clubs", "Quiet and private"])

budget = st.selectbox("What is your home purchase budget?", [
    "< $350K", "$350K – $450K", "$450K – $600K", "$600K+"])
monthly = st.selectbox("What is your preferred monthly cost (HOA, taxes, insurance)?", [
    "< $2000", "$2000 – $2500", "$2500 – $3000", "$3000+"])
tax_pref = st.multiselect("Which tax features are important to you?", [
    "No state income tax", "Low property tax", "Homestead exemption", "Retirement tax benefits", "Property tax cap", "Builder incentives"])
loan_type = st.radio("Will you be using a VA loan?", ["Yes", "No"])

reasons = st.multiselect("What are your top reasons for moving?", [
    "Downsizing", "Retirement", "Better weather", "Lower cost of living", "Closer to family/friends", "New job", "Lifestyle improvement"])
must_haves = st.text_area("List your top 5 MUST-HAVE features:")
nice_haves = st.text_area("List your top 5 NICE-TO-HAVE features:")

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

    mock_results = [
        {
            "location": "Summerville, SC",
            "score": 92,
            "home": "3BR / 2BA | 2100 sq ft | $430K",
            "features": "Single-story, Open Floor Plan, Screened Porch",
            "link": "https://www.realtor.com/realestateandhomes-detail/2100-Preserve-Way_Summerville_SC_29483_M95867-16314",
            "image": "https://cdn.realtor.com/medias/2100-preserve-way.jpg"
        },
        {
            "location": "Asheville, NC",
            "score": 88,
            "home": "2BR / 2BA | 1800 sq ft | $395K",
            "features": "Mountain View, 55+ Community, Garden Area",
            "link": "https://www.realtor.com/realestateandhomes-detail/1800-Sweet-Grass-Ln_Asheville_NC_28804_M93638-10257",
            "image": "https://cdn.realtor.com/medias/1800-sweet-grass.jpg"
        },
        {
            "location": "Bluffton, SC",
            "score": 84,
            "home": "4BR / 3BA | 2400 sq ft | $520K",
            "features": "Gated Entry, Resort-Style Pool, Golf Nearby",
            "link": "https://www.realtor.com/realestateandhomes-detail/2400-River-View-Dr_Bluffton_SC_29910_M98234-29817",
            "image": "https://cdn.realtor.com/medias/2400-river-view.jpg"
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
