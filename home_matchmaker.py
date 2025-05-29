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

# Function to fetch real Zillow listings via region using extended search

def fetch_zillow_listings(beds_min, baths_min, home_type, min_price, max_price, region):
    city_lookup = {
        "Southeast": "Charleston, SC",
        "Southwest": "Phoenix, AZ",
        "Pacific Coast": "San Diego, CA",
        "Midwest": "Columbus, OH",
        "Northeast": "Boston, MA",
        "Mountain West": "Boise, ID"
    }
    cities = [city_lookup[r] for r in region if r in city_lookup]

    headers = {
        "x-rapidapi-host": "zillow-com1.p.rapidapi.com",
        "x-rapidapi-key": "941903cba9msh1acce231bdba4f0p1366fajsn7ffc07b009ec"
    }

    all_results = []
    url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
    for city in cities:
        querystring = {
            "location": city,
            "status_type": "ForSale",
            "home_type": home_type[0].lower().replace("+ ", "").replace(" ", "") if home_type else "house",
            "beds_min": beds_min,
            "baths_min": baths_min,
            "price_min": min_price,
            "price_max": max_price
        }
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            filtered_props = [
                prop for prop in data.get("props", [])
                if prop.get("price") and min_price <= prop.get("price") <= max_price
                and prop.get("beds", 0) >= beds_min
                and prop.get("baths", 0) >= baths_min
            ]
            all_results.extend(filtered_props)

    return {"props": all_results} if all_results else {"error": "No listings found for selected region(s)."}

with st.form(key="home_form"):
    region = st.multiselect("Which regions of the U.S. are you open to (will be used to search multiple cities)?", [
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

    desirable_nearby = st.multiselect("Must be within 30 minutes of:", ["Lake", "Mountain", "Beach", "Shopping", "Hospital", "Airport"])

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
            city = result.get('city', 'Unknown City')
            state = result.get('state', '')
            price = result.get('price', 'N/A')
            beds = result.get('beds', '?')
            baths = result.get('baths', '?')
            features = result.get('statusText', '')
            url = result.get('detailUrl')
            full_url = f"https://www.zillow.com{url}" if url and not url.startswith("http") else url
            st.markdown(f"""
            <div class='result-card'>
                <img src='{result.get('imgSrc', '')}' alt='Home Image' class='home-image'/>
                <h4>{city}, {state} — ${price:,}</h4>
                <p><strong>{beds} BR / {baths} BA</strong><br/>
                Features: {features}<br/>
                <a href='{full_url}' target='_blank'>🔗 View Listing</a></p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No listings found in the selected area.")
