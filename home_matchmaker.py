# Home Matchmaker - Streamlit Survey App
# This is the prototype script for your hosted tool

import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="Home Matchmaker Survey", layout="wide")
st.title("🏡 Find Your Ideal Home and Location")
st.markdown("Use this survey to help determine your best match for your next home and neighborhood.")

# Define sections
st.header("1️⃣ Lifestyle & Location Preferences")
region = st.multiselect("Which regions of the U.S. are you open to?", [
    "Southeast", "Southwest", "Pacific Coast", "Midwest", "Northeast", "Mountain West"
])
climate = st.multiselect("What climate do you prefer?", [
    "Warm year-round", "Four seasons", "Mild winters", "Coastal", "Mountain", "Dry/Desert"
])
community_size = st.selectbox("What kind of community size do you prefer?", [
    "Urban", "Suburban", "Small Town", "Rural"
])

proximity = st.multiselect("Which of these should be within 30 minutes of your home?", [
    "Airports", "Hospitals", "Beaches", "Mountains", "Lakes/Rivers", "Grocery Stores", "Family", "Friends"
])

priority_areas = st.text_area("List ZIP codes or cities near family/friends you want to live close to:")


st.header("2️⃣ Home Features")
home_type = st.multiselect("What type of home do you prefer?", [
    "Single-family", "Townhome", "Condo", "55+ Community"
])
sqft = st.selectbox("Ideal home square footage:", [
    "< 1500", "1500–2000", "2000–2500", "> 2500"
])
beds = st.slider("Minimum number of bedrooms", 1, 5, 3)
baths = st.slider("Minimum number of bathrooms", 1, 4, 2)
floorplan = st.multiselect("Preferred layout features", [
    "Single-story", "Multi-story", "Open floor plan", "Split bedrooms", "Walk-in closets", "Large pantry", "Flex space"
])
outdoor = st.multiselect("Outdoor space preferences", [
    "Screened porch", "Covered patio", "Outdoor kitchen", "Fenced yard", "Garden area"
])


st.header("3️⃣ Neighborhood Amenities")
amenities = st.multiselect("What community features do you want?", [
    "Clubhouse", "Fitness center", "Pickleball courts", "Tennis courts", "Resort-style pool", "Walking trails", "Golf access", "Gated entry", "HOA maintenance"
])
lifestyle = st.multiselect("What kind of neighborhood vibe do you want?", [
    "Active adult (55+)", "Family-friendly", "Pet-friendly", "Social events/clubs", "Quiet and private"
])


st.header("4️⃣ Financial Considerations")
budget = st.selectbox("What is your home purchase budget?", [
    "< $350K", "$350K – $450K", "$450K – $600K", "$600K+"
])
monthly = st.selectbox("What is your preferred monthly cost (HOA, taxes, insurance)?", [
    "< $2000", "$2000 – $2500", "$2500 – $3000", "$3000+"
])
tax_pref = st.multiselect("Which tax features are important to you?", [
    "No state income tax", "Low property tax", "Homestead exemption", "Retirement tax benefits", "Property tax cap", "Builder incentives"
])
loan_type = st.radio("Will you be using a VA loan?", ["Yes", "No"])


st.header("5️⃣ Personal Priorities")
reasons = st.multiselect("What are your top reasons for moving?", [
    "Downsizing", "Retirement", "Better weather", "Lower cost of living", "Closer to family/friends", "New job", "Lifestyle improvement"
])
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

    st.success("Survey saved! Matching engine and results panel will be developed in the next step.")
    st.json(survey_data)
    st.download_button("📥 Download My Responses", data=json.dumps(survey_data, indent=2), file_name="home_match_survey.json")
