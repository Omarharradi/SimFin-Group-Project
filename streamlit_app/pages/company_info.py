import streamlit as st
import pandas as pd
import utils

# Streamlit UI Config
st.set_page_config(page_title="Company Info", page_icon=":fire:", layout="wide")
st.title(":fire: Company Information")

# Add navigation
utils.navigation_bar()

# Hide Streamlit's default sidebar
utils.hide_streamlit_sidebar()

# Initialize API
API_KEY = "0ce27565-392d-4c49-a438-71e3b39f298f"
simfin = utils.PySimFin(API_KEY)

# Define allowed tickers
tickers = ["AAPL", "MSFT", "BRO", "FAST", "ODFL"]

# Dropdown for ticker selection
ticker = st.selectbox("Select a Stock Ticker:", tickers, key="selected_ticker")

if ticker:
    company_info = simfin.get_company_info([ticker])

    if not company_info.empty:
        # Extract the first row (since it's a single company)
        company_name = company_info.loc[0, "name"]
        ticker_name = company_info.loc[0, "ticker"]
        industry_name = company_info.loc[0, "industryName"]
        sector_name = company_info.loc[0, "sectorName"]
        description = company_info.loc[0, "companyDescription"]
        employees = company_info.loc[0, "numEmployees"]
        market = company_info.loc[0, "market"]
        isin = company_info.loc[0, "isin"]

        # Generate a meaningful company description
        company_description = f"""
        **{company_name} ({ticker_name})** operates in the **{industry_name}** industry within the **{sector_name}** sector. 
        It is registered on the **{market}** market with the **{isin}** number and employs approximately **{employees:,}** people. 
        
        **About the Company:**  
        {description}
        """

        # Display information in Streamlit
        st.markdown(company_description)