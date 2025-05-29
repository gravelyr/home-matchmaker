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
        width: calc(33% - 16px);
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

# Function to fetch real Zillow listings via polygon using user preferences
def fetch_zillow_listings(beds_min, baths_min, home_type, min_price, max_price):
    url = "https://zillow-com1.p.rapidapi.com/propertyByPolygon"
    querystring = {
        "polygon": "-118.50394248962402 34.02926010734425, -118.5084056854248 34.02926010734425, -118.51286888122559 34.028691046671696, -118.51527214050293 34.02570341552858, -118.51321220397949 34.02257340341831, -118.51750373840332 34.0215774662657, -118.51681709289551 34.017878168811684, -118.51286888122559 34.016455319170184, -118.51080894470215 34.013324966013194, -118.50789070129395 34.010621386310234, -118.50411415100098 34.008629219864694, -118.49982261657715 34.008486920473, -118.49570274353027 34.007063913440916, -118.4919261932373 34.00891381793271, -118.48849296569824 34.01119056813859, -118.4860897064209 34.014463289606894, -118.48471641540527 34.018020452464164, -118.48042488098145 34.01858958468914, -118.4780216217041 34.0215774662657, -118.47939491271973 34.0249920592766, -118.47681999206543 34.02797971546417, -118.47493171691895 34.03125178964367, -118.4721851348877 34.034381481654364, -118.47733497619629 34.035377268536706, -118.48231315612793 34.035377268536706, -118.48677635192871 34.035377268536706, -118.49141120910645 34.03495050416125, -118.49604606628418 34.034096968969656, -118.49621772766113 34.03054047990366, -118.50033760070801 34.02926010734425, -118.50239753723145 34.032532132148006, -118.50394248962402 34.02926010734425",
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
        return response.json()
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

    submitted = st.form_submit_button("🔍 Find My Matches")

if submitted:
    st.success("🎉 Thank you! Your preferences have been saved. You are ready to view your matches.")
    listings = fetch_zillow_listings(beds, baths, home_type, min_price, max_price)

    if "error" in listings:
        st.error(listings["error"])
    elif listings.get("props"):
        results = listings["props"][:10]  # Show first 10 results
        st.markdown("<div class='result-grid'>", unsafe_allow_html=True)
        for result in results:
            st.markdown(f"""
            <div class='result-card'>
                <img src='{result.get('imgSrc', '')}' alt='Home Image' class='home-image'/>
                <h4>{result.get('addressCity', 'City')}, {result.get('addressState', '')} — {result.get('price', 'N/A')}</h4>
                <p><strong>{result.get('beds', '?')}BR / {result.get('baths', '?')}BA</strong><br/>
                Features: {result.get('statusType', 'Available')}<br/>
                <a href='https://www.zillow.com{result.get('detailUrl', '')}' target='_blank'>🔗 View Listing</a></p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No listings found in the selected area.")
