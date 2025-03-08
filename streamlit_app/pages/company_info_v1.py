import streamlit as st
import pandas as pd
import utils
import os

# Streamlit UI Config
utils.set_custom_page_config(title="Company Information", icon="🏢")
utils.hide_streamlit_sidebar()
utils.navigation_bar()
utils.apply_custom_styles()

# Display large logo in the top-left corner
utils.display_large_top_left_logo()

st.title("🏢 Company Information")
st.write("Get insights on companies by selecting a stock ticker below.")

# Initialize API
API_KEY = "0ce27565-392d-4c49-a438-71e3b39f298f"
simfin = utils.PySimFin(API_KEY)

# Define allowed tickers
tickers = ["AAPL", "MSFT", "BRO", "FAST", "ODFL"]

# Dropdown for ticker selection with a default value
ticker = st.selectbox("Select a Stock Ticker:", tickers, index=0, key="selected_ticker")

# Fetch company logo from local resources
@st.cache_data(ttl=600)
def fetch_ticker_logo(ticker):
    logo_path = f"resources/{ticker}_logo.png"
    if os.path.exists(logo_path):
        return logo_path
    return "resources/placeholder.png"  # Fallback placeholder image

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
            logo_path = fetch_ticker_logo(ticker)
            
            # Display company logo next to company name
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 15px;">
                    <img src="{logo_path}" width="100">
                    <h2 style="color:white;">{company_name}</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Display company details with styling
            st.markdown("## <span style='color:#2C9795;'>US Registration Number:</span>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:white; font-size:18px;'>{registration_number}</p>", unsafe_allow_html=True)
            
            st.markdown("## <span style='color:#2C9795;'>Number of Employees:</span>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:white; font-size:18px;'>{employees:,}</p>", unsafe_allow_html=True)
            
            st.markdown("## <span style='color:#2C9795;'>About:</span>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:white; font-size:18px;'>{about}</p>", unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error loading company information: {str(e)}")