import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz
import requests
from datetime import datetime, timedelta
import json
import streamlit as st
import base64
import time
import requests
import xgboost as xgb
import joblib

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
    
    def get_predictions_data(self):
        tickers = ["AAPL", "MSFT", "BRO", "FAST", "ODFL"]
        batch_size = 2
        all_data = []

        for i in range(0, len(tickers), batch_size):
            batch = tickers[i:i + batch_size]
            df_tickers = self.get_stock_prices(batch, 1)
            df_tickers = df_tickers.rename(columns={
                "Date": "Date", "Opening Price": "Open", "Highest Price": "High",
                "Lowest Price": "Low", "Last Closing Price": "Close", 
                "Trading Volume": "Volume", "Adjusted Closing Price": "Adj. Close",
                "Common Shares Outstanding": "Shares Outstanding"
            })
            all_data.append(df_tickers)
            time.sleep(0.3)

        # Combine all data
        df_tickers = pd.concat(all_data)

        pivoted_df = df_tickers.pivot(index="Date", columns="Ticker", values=["Open", "High", "Low", "Close", "Adj. Close", "Volume"])

        # Flatten column names
        pivoted_df.columns = [f"{col[0]}_{col[1]}" for col in pivoted_df.columns]
        pivoted_df.reset_index(inplace=True)

        # Merge with original dataset to ensure each ticker retains its own target variable
        merged_df = df_tickers.merge(pivoted_df, on="Date", how="left")

        cols_to_drop = ["Open", "High", "Low", "Close", "Adj. Close", "Volume", "Dividend Paid"]
        merged_df.drop(columns=cols_to_drop, inplace=True)
        return merged_df

def predict_market(df):
        # Load the trained XGBoost model
        model = joblib.load("resources/model/xgb.joblib")

        # Store the 'Date' and 'Ticker' columns separately
        date_ticker = df[['Date', 'Ticker']]

        # Drop the columns before prediction
        X = df.drop(columns=['Date', 'Ticker'])

        dmat = xgb.DMatrix(X)

        # Generate predictions
        predictions = model.predict(dmat)

        # Create a DataFrame with the original 'Date' and 'Ticker' and add predictions
        df_predictions = date_ticker.copy()
        df_predictions['Prediction'] = predictions
        return df_predictions

def is_market_open():
    # Define NYSE timezone
    nyse_tz = pytz.timezone('America/New_York')
    
    # Get current time in NYSE timezone
    now = datetime.now(nyse_tz)
    
    # Market hours (9:30 AM - 4:00 PM EST)
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    
    # Check if it's a weekday and within trading hours
    if now.weekday() < 5 and market_open <= now <= market_close:
        return True
    return False

# Check if NYSE is open
print("NYSE is open:", is_market_open())


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

def navigation_bar():
    logo_base64 = get_base64("resources/images/logo.png")  # Ensure correct logo path

    st.markdown(
        f"""
        <style>
            .top-nav {{
                display: flex;
                align-items: center;
                justify-content: start; /* Align logo and menu to the left */
                background-color: #002149;
                padding: 25px 40px; /* Increase top and bottom padding */
                border-radius: 8px;
            }}
            .top-nav img {{
                width: 300px;  /* Make logo bigger */
                height: auto;
                margin-right: 40px; /* Increase space between logo and menu */
            }}
            .menu-container {{
                display: flex;
                align-items: center;
                gap: 100px; /* Increase space between menu items */
            }}
            .menu-container button {{
                background: none !important;
                border: none !important;
                color: white !important;
                font-size: 50px !important; /* Increase font size of menu */
                font-weight: bold !important;
                padding: 10px 20px !important; /* Increase button padding */
                cursor: pointer;
            }}
            .menu-container button:hover {{
                text-decoration: underline !important;
            }}
        </style>
        <div class="top-nav">
            <img src="data:image/png;base64,{logo_base64}" alt="Company Logo">
            <div class="menu-container">
                <div id="home"></div>
                <div id="company"></div>
                <div id="prediction"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Injecting `st.page_link()` buttons inline using st.empty()
    menu_placeholder = st.empty()
    with menu_placeholder.container():
        inline_col = st.columns([1, 1, 1])  # Keep buttons close together
        with inline_col[0]:
            st.page_link("home.py", label="Home", use_container_width=False)
        with inline_col[1]:
            st.page_link("pages/company_info_v1.py", label="Company Overview", use_container_width=False)
        with inline_col[2]:
            st.page_link("pages/go_live_v5.py", label="Prediction", use_container_width=False)


# Adds a navigation sidebar for easy access to pages
#def navigation_bar():
    #with st.sidebar:
        #st.title("📌 Main Menu")
        #st.page_link("home.py", label="🏠 Home")
        #st.page_link("pages/go_live_v4_5.py", label="📊 Prediction")
        #st.page_link("pages/company_info_v1.py", label="🏢 Ticker Overview")

# Applies global styling for the app
def apply_custom_styles():
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #002149; /* Keep Dark Background */
            }
            h1, h2, h3 {
                color: #4DCF9E !important; /* Apply New Title Color */
            }
            .stMarkdown {
                color: white !important; /* Keep all regular text white */
            }
            hr {
                border: 1px solid #4DCF9E !important; /* Apply same color to dividers */
            }
            .stButton>button {
                background-color: #2C9795 !important;
                color: white !important;
                font-weight: bold;
                border-radius: 5px;
            }
            .stButton>button:hover {
                background-color: #237878 !important;
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
def display_home_header():
    st.markdown(
        f"""
        <style>
            .page-title {{
                margin-top: -20px !important;  /* Pull title closer */
                text-align: center;
            }}
        </style>
        <div class="page-title">
            <h1 style="font-size: 60px; font-weight: bold; color: #4DCF9E;">Welcome to ForesightX</h1>
        </div>
        <hr style="border: 1px solid #4DCF9E;">
        <div style="text-align: center; font-size: 35px; font-weight: bold; color: white;">
            Your AI-Powered Stock Prediction Assistant!
        </div>
        <hr style="border: 1px solid #4DCF9E;">
        """,
        unsafe_allow_html=True
    )

# Displays the logo in the top-left corner above the title
def display_top_left_logo_above_title(logo_path="resources/images/logo.png"):
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
def display_large_top_left_logo(logo_path="resources/images/logo.png"):
    logo_base64 = get_base64(logo_path)
    st.markdown(
        f"""
        <div style="position: absolute; top: 1px; left: 1px;">
            <img src="data:image/png;base64,{logo_base64}" width="250">
        </div>
       <br><br><br><br><br><br><br>  <!-- Adds extra space below the logo -->
        """,
        unsafe_allow_html=True
    )
# time retries and delays SinFim API
def get_company_info(self, tickers: list, max_retries=3, delay=5):
    base_url = "https://backend.simfin.com/api/v3/companies/general/compact" 
    ticker_list = ",".join(tickers)
    url = f"{base_url}?ticker={ticker_list}"  
    
    for attempt in range(max_retries):
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            if "columns" in data and "data" in data:
                return pd.DataFrame(data["data"], columns=data["columns"])
            else:
                raise Exception(f"Unexpected API response format: {data}")

        elif response.status_code == 429:
            # Too many requests - wait and retry
            wait_time = (attempt + 1) * delay
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            raise Exception(f"API Error {response.status_code}: {response.text}")

    raise Exception("Max retries reached. API request failed.")
