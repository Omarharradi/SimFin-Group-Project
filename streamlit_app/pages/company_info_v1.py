import streamlit as st
import pandas as pd
import utils
import requests
from PIL import Image
from io import BytesIO

# Streamlit UI Config
utils.set_custom_page_config(title="Company Information", icon="🏢")
utils.hide_streamlit_sidebar()
utils.navigation_bar()
utils.apply_custom_styles()
utils.display_company_header()

st.markdown(f"<p style='color:white; font-size:24px;'>Get insights on companies by selecting a stock ticker below</p>", unsafe_allow_html=True)

# Initialize API
API_KEY = "0ce27565-392d-4c49-a438-71e3b39f298f"
simfin = utils.PySimFin(API_KEY)

# Define allowed tickers
tickers = ["AAPL", "MSFT", "BRO", "FAST", "ODFL"]

# Dropdown for ticker selection with a default value
st.markdown(
    "<p style='font-size:22px; color:#DDE2E5 !important; margin-bottom: -20px;'>Select a Stock Ticker:</p>", 
    unsafe_allow_html=True
)
ticker = st.selectbox("", tickers, index=0, key="selected_ticker")

@st.cache_data(ttl=600)
def fetch_ticker_logo(ticker):
    """
    Fetches the ticker logo from the API. If the API fails, returns the fallback local image.
    """
    try:
        # API Token
        API_TOKEN = "pk_RQPzczoCTlmAPlHQSCrzJw"
        API_URL = "https://img.logo.dev/ticker/{ticker}?token=" + API_TOKEN + "&size=100" + "&format=png" #+ "&retina=true"
        #Ref = https://img.logo.dev/ticker/MSFT?token=pk_RQPzczoCTlmAPlHQSCrzJw&size=300&format=png&retina=true
        response = requests.get(API_URL.format(ticker=ticker), timeout=5)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))  # Return the image directly

    except requests.RequestException:
        pass  # If the request fails, continue to the fallback

    # Fallback to local "No Image Available"
    return Image.open("resources/images/no_Image_Available.jpg")

# Cache company data to reduce API calls
@st.cache_data(ttl=600)
def fetch_company_data(ticker):
    return simfin.get_company_info([ticker])

if ticker:
    try:
        company_info = fetch_company_data(ticker)
        
        if not company_info.empty:
            company_name = company_info.loc[0, "name"]
            registration_number = company_info.loc[0, "isin"]
            employees = company_info.loc[0, "numEmployees"]
            about = company_info.loc[0, "companyDescription"]

            # Fetch the logo from the resources folder
            logo = fetch_ticker_logo(ticker)
            
            # Display company logo next to company name
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(logo, width=100)
            with col2:
                st.markdown(f"<h2 style='color:white;'>{company_name}</h2>", unsafe_allow_html=True)

            # Display company details with styling
            st.markdown("### <span style='color:#2C9795;'>US Registration Number:</span>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:white; font-size:21px;'>{registration_number}</p>", unsafe_allow_html=True)
            
            st.markdown("### <span style='color:#2C9795;'>Number of Employees:</span>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:white; font-size:18px;'>{employees:,}</p>", unsafe_allow_html=True)
            
            st.markdown("### <span style='color:#2C9795;'>About:</span>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:white; font-size:18px;'>{about}</p>", unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error loading company information: {str(e)}")