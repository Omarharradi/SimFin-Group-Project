import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz
import requests
from datetime import datetime, timedelta
import json
import streamlit as st
import base64


def fetch_latest_ohlc(tickers):
    """
    Fetches the latest OHLC data for a list of tickers.
    
    Parameters:
        tickers (list): A list of stock/forex tickers.
        
    Returns:
        pd.DataFrame: DataFrame with columns [Ticker, Timestamp, Open, High, Low, Close].
    """
    madrid_tz = pytz.timezone("Europe/Madrid")
    all_data = []
    
    for ticker in tickers:
        df = yf.download(ticker, period="1d", interval="1d")
        if df.empty:
            continue  # Skip if no data is returned
        
        latest = df.iloc[-1]
        
        timestamp = datetime.now(pytz.utc).astimezone(madrid_tz)
        
        data = {
            "Ticker": ticker,
            "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "Open": float(latest["Open"].iloc[0]),
            "High": float(latest["High"].iloc[0]),
            "Low": float(latest["Low"].iloc[0]),
            "Close": float(latest["Close"].iloc[0]),
            "Volume": float(latest["Volume"].iloc[0])
        }
        
        all_data.append(data)
    
    return pd.DataFrame(all_data)


class PySimFin:
    def __init__(self, api_key):
        self.__api_key = api_key
        self.headers = {
            "accept": "application/json",
            "Authorization": f"{self.__api_key}"  
        }

    def get_stock_prices(self, tickers: list, days: int):
        base_url = "https://backend.simfin.com/api/v3/companies/prices/compact" 
        start_date = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')
        ticker_list = ",".join(tickers)
        url = f"{base_url}?ticker={ticker_list}&start={start_date}"
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.text)
        all_data = []

        for company_data in data:
            columns = company_data['columns']
            rows = company_data['data']
            ticker = company_data['ticker']
            df = pd.DataFrame(rows, columns=columns)
            df['Ticker'] = ticker
            all_data.append(df)

        final_df = pd.concat(all_data, ignore_index=True)
        return final_df
    
    def get_company_info(self, tickers: list):
        base_url = "https://backend.simfin.com/api/v3/companies/general/compact" 
        ticker_list = ",".join(tickers)
        url = f"{base_url}?ticker={ticker_list}"  
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text}")
        data = json.loads(response.text)  # Parse JSON response
        if not isinstance(data, dict) or "columns" not in data or "data" not in data:
            raise Exception(f"Unexpected API response format: {data}")
        columns = data["columns"]
        rows = data["data"]
        df = pd.DataFrame(rows, columns=columns)
        return df

# Encodes an image to base64 format
def get_base64(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode()

# Sets the page configuration for all pages
def set_custom_page_config(title="ForesightX", icon="📌"):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="collapsed"
    )

# Hides the default Streamlit sidebar
def hide_streamlit_sidebar():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )

# Adds a navigation sidebar for easy access to pages
def navigation_bar():
    with st.sidebar:
        st.title("📌 Main Menu")
        st.page_link("home.py", label="🏠 Home")
        st.page_link("pages/go_live_v4_5.py", label="📊 Prediction")
        st.page_link("pages/company_info.py", label="🏢 Ticker Overview")

# Applies global styling for the app
def apply_custom_styles():
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #002149;
            }
            .stButton>button {
                background-color: #05CC77 !important;
                color: white !important;
                font-weight: bold;
                border-radius: 5px;
            }
            .stButton>button:hover {
                background-color: #04A76F !important;
            }
            h1, h2, h3 {
                color: #05CC77;
            }
            .stTextInput>div>div>input {
                background-color: #004080;
                color: white;
                border-radius: 5px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Displays the homepage header with the logo and title
def display_home_header(logo_path="logo.png"):
    logo_base64 = get_base64(logo_path)
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: center; gap: 20px;">
            <img src="data:image/png;base64,{logo_base64}" width="300">
            <h1 style="font-size: 60px; font-weight: bold; color: #F2F3F4;">Welcome to ForesightX</h1>
        </div>
        <hr style="border: 1px solid #05CC77;">
        <div style="text-align: center; font-size: 35px; font-weight: bold; color: #05CC77;">Your AI-Powered Stock Prediction Assistant!</div>
        <hr style="border: 1px solid #05CC77;">
        """,
        unsafe_allow_html=True
    )

# Displays the logo in the top-left corner above the title
def display_top_left_logo_above_title(logo_path="logo.png"):
    logo_base64 = get_base64(logo_path)
    st.markdown(
        f"""
        <div style="position: absolute; top: 10px; left: 10px;">
            <img src="data:image/png;base64,{logo_base64}" width="200">
        </div>
        <br><br><br><br>  <!-- Adds spacing to prevent overlap with the title -->
        """,
        unsafe_allow_html=True
    )

# Displays a larger logo in the top-left corner
def display_large_top_left_logo(logo_path="logo.png"):
    logo_base64 = get_base64(logo_path)
    st.markdown(
        f"""
        <div style="position: absolute; top: 10px; left: 10px;">
            <img src="data:image/png;base64,{logo_base64}" width="250">
        </div>
        <br><br><br><br>  <!-- Adds spacing to prevent overlap -->
        """,
        unsafe_allow_html=True
    )
