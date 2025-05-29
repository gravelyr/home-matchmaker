# Home Matchmaker - Streamlit Survey App
# Full-page version using real Zillow API call, now using user preferences

import streamlit as st
import requests
import json

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
    .result-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
    }
    .result-card {
        background-color: #ffffff;
        color: #000000;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
        width: calc(33.333% - 16px);
        box-sizing: border-box;
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

st.title("🏡 Bernie and Clem's Find a Home Tool!")
st.markdown("### Fill out the form below to get matched with homes and communities based on your preferences.")

# Function to fetch real Zillow listings via bounding box using user preferences
def fetch_zillow_listings(beds_min, baths_min, home_type, min_price, max_price, region):
    region_bounds = {
        "Southeast": "-81.2 32.0, -81.2 34.0, -79.0 34.0, -79.0 32.0",
        "Southwest": "-117.0 32.0, -117.0 36.0, -110.0 36.0, -110.0 32.0",
        "Pacific Coast": "-124.0 32.0, -124.0 42.0, -117.0 42.0, -117.0 32.0",
        "Midwest": "-97.0 36.0, -97.0 46.0, -85.0 46.0, -85.0 36.0",
        "Northeast": "-80.0 40.0, -80.0 45.0, -70.0 45.0, -70.0 40.0",
        "Mountain West": "-115.0 36.0, -115.0 45.0, -105.0 45.0, -105.0 36.0"
    }
    selected_polygon = region_bounds.get(region[0], region_bounds["Southeast"])

    url = "https://zillow-com1.p.rapidapi.com/propertyByPolygon"
    querystring = {
        "polygon": selected_polygon,
        "status_type": "ForSale",
        "home_type": home_type[0] if home_type else "Houses",
        "beds_min": beds_min,
        "baths_min": baths_min,
        "price_min": min_price,
        "price_max": max_price
    }

    headers = {
        "x-rapidapi-host": "zillow-com1.p.rapidapi.com",
        "x-rapidapi-key": "941903cba9msh1acce231bdba4f0p1366fajsn7ffc07b009ec"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        filtered = [prop for prop in data.get("props", []) if prop.get("price") and min_price <= prop.get("price") <= max_price]
        return {"props": filtered}
    else:
        return {"error": f"API error: {response.status_code}"}

with st.form(key="home_form"):
    region = st.multiselect("Which regions of the U.S. are you open to?", [
        "Southeast", "Southwest", "Pacific Coast", "Midwest", "Northeast", "Mountain West"])

    climate = st.multiselect("What climate do you prefer?", [
        "Warm year-round", "Four seasons", "Mild winters", "Coastal", "Mountain", "Dry/Desert"])

    home_type = st.multiselect("What type of home do you prefer?", [
        "Single-family", "Townhome", "Condo", "55+ Community"])

    sqft = st.selectbox("Ideal home square footage:", [
        "< 1500", "1500–2000", "2000–2500", "> 2500"])
    beds = st.slider("Minimum number of bedrooms", 1, 5, 3)
    baths = st.slider("Minimum number of bathrooms", 1, 4, 2)
    min_price = st.number_input("Minimum Price ($)", min_value=0, value=200000, step=10000)
    max_price = st.number_input("Maximum Price ($)", min_value=50000, value=600000, step=10000)

    desirable_nearby = st.multiselect("Must be within 30 minutes of:", ["Lake", "Mountain", "Beach", "Shopping", "Hospital", "Airport", "Family", "Friends"])
    family_zip = st.text_input("ZIP code of family you'd like to be near (optional)")
    friends_zip = st.text_input("ZIP code of friends you'd like to be near (optional)")

    submitted = st.form_submit_button("🔍 Find My Matches")

if submitted:
    st.success("🎉 Thank you! Your preferences have been saved. You are ready to view your matches.")
    listings = fetch_zillow_listings(beds, baths, home_type, min_price, max_price, region)

    if "error" in listings:
        st.error(listings["error"])
    elif listings.get("props"):
        results = listings["props"][:12]  # Show up to 12 results in a grid layout
        st.markdown("<div class='result-grid'>", unsafe_allow_html=True)
        for result in results:
            st.markdown(f"""
            <div class='result-card'>
                <img src='{result.get('imgSrc', '')}' alt='Home Image' class='home-image'/>
                <h4>{result.get('addressCity', 'City')}, {result.get('addressState', '')} — ${result.get('price', 'N/A'):,}</h4>
                <p><strong>{result.get('beds', '?')} BR / {result.get('baths', '?')} BA</strong><br/>
                Features: {result.get('statusType', 'Available')}<br/>
                <a href='https://www.zillow.com{result.get('detailUrl', '')}' target='_blank'>🔗 View Listing</a></p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No listings found in the selected area.")
