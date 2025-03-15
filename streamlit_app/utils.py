# Libraries
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
from backtesting import Backtest, Strategy
from io import StringIO
import tempfile
from PIL import Image, ImageOps, ImageDraw

# Python Wrapper for the SimFin API
class PySimFin:
    """
    A wrapper for interacting with the SimFin API to fetch financial data.
    """

    def __init__(self, api_key):
        """
        Initializes the PySimFin instance with the provided API key.

        Parameters:
            api_key (str): The API key for authentication with the SimFin API.

        Returns:
            None
        """
        self.__api_key = api_key
        self.headers = {
            "accept": "application/json",
            "Authorization": f"{self.__api_key}"  
        }

    def get_stock_prices(self, tickers: list, days: int) -> pd.DataFrame:
        """
        Fetches historical stock data for a list of tickers from the last amount of days.

        Parameters:
            tickers (list): A list of stock tickers to retrieve price data for.
            days (int): The number of past days from today to fetch data from.

        Returns:
            pd.DataFrame: A DataFrame containing stock price data with columns 
                        [Date, Open, High, Low, Close, Volume, Ticker].
        """
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
    
    def get_company_info(self, tickers: list) -> pd.DataFrame:
        """
        Fetches general information for a list of companies identified by their tickers.

        Parameters:
            tickers (list): A list of company tickers to retrieve general information for.

        Returns:
            pd.DataFrame: A DataFrame containing company general information with columns
                        such as [Ticker, Name, Sector, Industry, etc.].

        Raises:
            Exception: If the API response status code is not 200 or if the response format is unexpected.
        """
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
    
    def get_predictions_data(self) -> pd.DataFrame:
        """
        Fetches and processes stock price data for a predefined list of tickers to generate a structured dataset for predictions.

        Parameters:
            None

        Returns:
            pd.DataFrame: A DataFrame containing processed stock price data with pivoted columns for multiple tickers,
                        structured for predictive modeling.

        Process:
            - Fetches stock price data for a predefined list of tickers in batches to avoid API overload.
            - Renames columns for consistency.
            - Aggregates data across tickers and pivots it to structure the dataset.
            - Merges the transformed data back to maintain ticker-specific target variables.
            - Drops redundant columns to prepare the dataset for modeling.

        Raises:
            Exception: If data retrieval fails due to an API error.
        """
        # Predictions needs all the highly correlated tickers information:
        tickers = ["AAPL", "MSFT", "BRO", "FAST", "ODFL"]

        # SimFin compact Prices API has a limit of two tickers per request, so we do it in mini batches:
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
            time.sleep(0.3) # In order to not reach the contraint of 2 requests per second in free API key

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
    
    def get_predictions_data_backtest(self, start_date, end_date) -> pd.DataFrame:
        '''
        Does pretty much the same as the function above, only that it needs to work with start_date and end_date parameters.
        '''
        tickers = ["AAPL", "MSFT", "BRO", "FAST", "ODFL"]
        batch_size = 2
        all_data = []

        for i in range(0, len(tickers), batch_size):
            batch = tickers[i:i + batch_size]
            df_tickers = self.get_stock_prices_backtest(batch, start_date, end_date)
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
    
    def get_stock_prices_backtest(self, tickers: list, start_date, end_date) -> pd.DataFrame:
        """
        Fetches historical stock price data for a list of tickers within a specified date range,
        structured for backtesting purposes.

        Parameters:
            tickers (list): A list of stock tickers to retrieve historical price data for.
            start_date (datetime): The start date of the backtest period.
            end_date (datetime): The end date of the backtest period.

        Returns:
            pd.DataFrame: A DataFrame containing historical stock price data with columns
                        [Date, Open, High, Low, Close, Volume, Ticker], filtered by the given date range.

        Process:
            - Converts start and end dates to the required format.
            - Constructs the API request URL with the specified tickers and start date.
            - Fetches the stock price data from the SimFin API.
            - Parses the response and structures it into a DataFrame.
            - Ensures the 'Date' column is in datetime format for filtering.
            - Sorts the data by 'Ticker' and 'Date' for consistency.
            - Filters the dataset to include only records within the specified date range.

        Raises:
            Exception: If the API request fails or returns an unexpected response format.
        """
        base_url = "https://backend.simfin.com/api/v3/companies/prices/compact" 
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
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
        final_df['Date'] = pd.to_datetime(final_df['Date'])  # Ensure Date column is in datetime format
        final_df = final_df.sort_values(by=["Ticker", "Date"])

        # Filter by the date range
        final_df = final_df.loc[(final_df['Date'] >= start_date) & (final_df['Date'] <= end_date)]

        return final_df

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


def predict_market(df: pd.DataFrame) -> pd.DataFrame:
    """
    Predicts market movements using a pre-trained XGBoost model.

    Parameters:
        df (pd.DataFrame): A DataFrame containing historical stock data and relevant features for prediction.
                           Must include 'Date' and 'Ticker' columns, along with feature columns.

    Returns:
        pd.DataFrame: A DataFrame containing the original 'Date' and 'Ticker' columns, along with a new 'Prediction' column.

    Process:
        - Loads a pre-trained XGBoost model from the specified file path.
        - Extracts and stores 'Date' and 'Ticker' columns separately.
        - Drops non-feature columns before making predictions.
        - Converts the dataset into an XGBoost DMatrix format for efficient prediction.
        - Generates market movement predictions using the loaded model.
        - Merges the predictions back with the 'Date' and 'Ticker' information.

    Raises:
        FileNotFoundError: If the model file is missing or cannot be loaded.
        ValueError: If the DataFrame is missing required columns.
    """
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

def is_market_open() -> bool:
    """
    Checks if the New York Stock Exchange (NYSE) is currently open.

    Returns:
        bool: True if the market is open, False otherwise.
    """
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

def is_trading_day():
    """
    Checks if today is a trading day or not.

    Note: Holidays are not included in this function, just plain weekday/weekend classification.

    Returns:
        bool: True if the market is open, False otherwise.
    """
    nyse_tz = pytz.timezone("America/New_York")
    today = datetime.now(nyse_tz).date()
    return today.weekday() < 5  # Monday to Friday are trading days

class SignalStrategy(Strategy):
    """
    A strategy that follows the given signals with TP and SL.
    Buys at signal 1 and sells at signal 0, waiting for TP/SL to be hit.
    """
    # Define default tp and sl as class variables, but we'll override them later
    tp = 0.005  # Default take profit percentage
    sl = 0.005  # Default stop loss percentage

    def init(self):
        # Initialize the strategy with take profit and stop loss parameters
        self.tp_percent = self.tp  # Access tp directly
        self.sl_percent = self.sl  # Access sl directly
        self.signal = self.data.signal
        self.entry_price = None

    def next(self):
        """
        Executes the trading logic on each new bar in the backtesting engine.
        """
        # Called on every new bar
        if self.position:
            # We have an open position
            # Calculate TP and SL prices
            tp_price = self.entry_price * (1 + self.tp_percent)
            sl_price = self.entry_price * (1 - self.sl_percent)

            # Check for TP or SL exit
            if self.data.High[-1] >= tp_price:
                self.position.close()
                self.entry_price = None
            elif self.data.Low[-1] <= sl_price:
                self.position.close()
                self.entry_price = None
            elif self.signal[-1] == 0:  # Sell signal
                self.position.close()
                self.entry_price = None
        else:
            # No open position
            if self.signal[-1] == 1:  # Buy signal
                self.buy()
                self.entry_price = self.data.Close[-1]


def backtest(ticker: list, start_date, end_date, cash: float, tp: float, sl: float) -> tuple:
    """
    Performs a backtest on a trading strategy using historical stock data and a pre-trained XGBoost model.

    Parameters:
        ticker (list): A list of stock tickers to backtest.
        start_date (datetime): The start date for the backtest period.
        end_date (datetime): The end date for the backtest period.
        cash (float): The initial capital available for the backtest.
        tp (float): The take-profit threshold for the trading strategy.
        sl (float): The stop-loss threshold for the trading strategy.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: Processed dataset used for backtesting, including stock prices and trade signals.
            - str: HTML content of the backtest plot.
            - str: Logged backtest statistics.

    Process:
        - Initializes the `PySimFin` API wrapper with an API key.
        - Fetches historical stock price data for the specified ticker and date range.
        - Retrieves processed stock price data for prediction.
        - Loads the pre-trained XGBoost model and generates buy/sell predictions.
        - Merges predictions with the historical stock data.
        - Cleans and structures the dataset for backtesting.
        - Runs the backtest using the `Backtest` framework with the specified take-profit (TP) and stop-loss (SL) values.
        - Captures the backtest results, including:
            - Strategy performance statistics.
            - HTML visualization of the backtest results.
            - Log output containing key metrics.

    Raises:
        FileNotFoundError: If the XGBoost model file is missing.
        ValueError: If input parameters are invalid or if the required columns are missing from the dataset.

    Notes:
        - The function assumes a signal-based strategy (`SignalStrategy`) for trading decisions.
        - Market commissions are set to 0.2% (`.002`).
        - The HTML output of the backtest visualization is stored temporarily to avoid opening a browser window.

    Example:
        >>> df_results, html_plot, logs = backtest(["AAPL"], datetime(2022, 1, 1), datetime(2023, 1, 1), 10000, 0.05, 0.02)
        >>> print(logs)
    """
    API_KEY = "0ce27565-392d-4c49-a438-71e3b39f298f"
    simfin = PySimFin(API_KEY)
    df = simfin.get_stock_prices_backtest(ticker, start_date, end_date)
    merged_df = simfin.get_predictions_data_backtest(start_date, end_date)

    # Load the pre-trained XGBoost model
    model = joblib.load("resources/model/xgb.joblib")
    X = merged_df.drop(columns=['Date', 'Ticker'])

    # Generate predictions
    dmat = xgb.DMatrix(X)
    predictions = model.predict(dmat)
    predictions = (predictions > 0.5).astype(int)

    df_predictions = df.copy()
    merged_df['Prediction'] = predictions
    merged_df = merged_df[merged_df['Ticker'].isin(ticker)]
    df_predictions['signal'] = merged_df['Prediction'].values
    df_predictions = df_predictions.rename(columns={
        'Opening Price': 'Open',
        'Highest Price': 'High',
        'Lowest Price': 'Low',
        'Last Closing Price': 'Close',
        'Trading Volume': 'Volume',
        'Adjusted Closing Price': 'Adj. Close',
        'Common Shares Outstanding': 'Shares Outstanding'
    })

    df_predictions = df_predictions.drop(columns=['Dividend Paid'])
    df_predictions = df_predictions[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Adj. Close', 'Volume', 'Shares Outstanding', 'signal']]

    bck = df_predictions[df_predictions['Ticker'].isin(ticker)]
    bck['Date'] = pd.to_datetime(bck['Date'])
    bck.set_index('Date', inplace=True)

    # Run backtest with the strategy and provided TP/SL values
    bt = Backtest(bck, SignalStrategy, cash=cash, commission=.002)
    
    # Redirect print statements to a string buffer
    log_output = StringIO()
    
    # Capture backtest statistics
    stats = bt.run(tp=tp, sl=sl)
    print(stats, file=log_output)

    # Use a temporary file for HTML output but prevent opening a new tab
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmpfile:
        bt.plot(filename=tmpfile.name, open_browser=False)
        with open(tmpfile.name, "r", encoding="utf-8") as f:
            html_content = f.read()  # Read the HTML content into memory

    # Retrieve log output
    log_info = log_output.getvalue()
    
    return df_predictions, html_content, log_info

### STREAMLIT PAGE FORMATTING FUNCTIONS:
def get_base64(image_path):
    """
    Encodes an image to base64 format
    """
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode()

def set_custom_page_config(title="ForesightX", icon="📌"):
    """
    Sets the page configuration for all pages
    """
    st.set_page_config(
        page_title=title,  # Title shown in browser tab
        page_icon=icon,  # Emoji/icon for the page
        layout="wide",  # Full-width layout
        initial_sidebar_state="expanded"  # Hide default Streamlit sidebar
    )

def hide_streamlit_sidebar():
    """
    Hides the default Streamlit sidebar
    """
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )

def navigation_bar():
    """
    Adds a navigation sidebar for easy access to pages
    """
    with st.sidebar:
        st.title("📌 Main Menu")
        st.page_link("home.py", label="🏠 Home")
        st.page_link("pages/company_info_v1.py", label="🏢 Company Overview")
        st.page_link("pages/go_live_v5.1.py", label="📊 Prediction")
        st.page_link("pages/backtest.py", label = "📈 Backtest")
        
def apply_custom_styles():
    """
    Applies global styling for the app
    """
    st.markdown(
        """
        <style>
            /* Light Mode */
            @media (prefers-color-scheme: light) {
                body, .stApp {
                    background-color: #ffffff;
                    color: black !important;
                }
                h1, h2, h3, label {
                    color: #002149 !important;  /* Ensures readability */
                }
                .stSlider label {
                    color: #002149 !important;  /* Slider title stays visible */
                }
                /* Tooltip (Help icon) - Always white */
                [data-testid="stTooltipIcon"] svg {
                color: white !important;  /* Keeps only the '?' icon white */
                fill: white !important; 
                }
                /* Button Text */
                .stButton>button {
                    background-color: #05CC77 !important; /* Green button */
                    color: white !important;  /* Ensures button text is visible */
                    font-weight: bold;
                    border-radius: 5px;
                }
                .stButton>button:hover {
                    background-color: #04A76F !important;
                }
            }

            /* Dark Mode */
            @media (prefers-color-scheme: dark) {
                body, .stApp {
                    background-color: #002149;
                    color: white !important;
                }
                h1, h2, h3, label {
                    color: #34ABA2 !important;
                }
                .stSlider label {
                    color: white !important;
                }
                /* Tooltip (Help icon) */
                [data-testid="stTooltipIcon"] {
                    color: white !important; /* White tooltip in dark mode */
                }
                /* Button Text */
                .stButton>button {
                    background-color: #05CC77 !important;
                    color: white !important;  /* Ensures button text stays visible */
                    font-weight: bold;
                    border-radius: 5px;
                }
                .stButton>button:hover {
                    background-color: #04A76F !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def display_home_header(logo_path="resources/images/logo.png"):
    """
    Displays the homepage header with the logo and title
    """
    logo_base64 = get_base64(logo_path)
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: center; gap: 0px;">
            <img src="data:image/png;base64,{logo_base64}" width="300">
            <h1 style="font-size: 60px; font-weight: bold; color: #F2F3F4;">Welcome to ForesightX</h1>
        </div>
        <hr style="border: 1px solid #F2F3F4;">
        <div style="text-align: center; font-size: 35px; font-weight: bold; color:white;">Your AI-Powered Stock Prediction Assistant!</div>
        <hr style="border: 1px solid #F2F3F4;">
        """,
        unsafe_allow_html=True
    )

def display_company_header(logo_path="resources/images/logo.png"):
    """
    Displays company header
    """
    logo_base64 = get_base64(logo_path)
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: center; gap: 20px;">
            <img src="data:image/png;base64,{logo_base64}" width="300">
            <h1 style="font-size: 60px; font-weight: bold; color: #F2F3F4;">Company Overview</h1>
        </div>
        <hr style="border: 1px solid #F2F3F4;">
        """,
        unsafe_allow_html=True
    )

def get_base64(image_path):
    """
    Encodes an image to Base64 format
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def display_backtesting_header(logo_path="resources/images/logo.png"):
    """
    Displays the Backtesting Tool header with reduced spacing.
    """
    logo_base64 = get_base64(logo_path)

    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: center; gap: 20px;">
            <img src="data:image/png;base64,{logo_base64}" width="300">
            <h1 style="font-size: 60px; font-weight: bold; color: #F2F3F4; margin-bottom: 10px;">Backtesting Tool</h1>
        </div>
        <hr style="border: 1px solid #F2F3F4; margin-top: 5px; margin-bottom: 5px;">
        """,
        unsafe_allow_html=True
    )

# Displays predictor header
def display_predictor_header(logo_path="resources/images/logo.png"):
    """
    Displays the Prediction page header with reduced spacing.
    """
    logo_base64 = get_base64(logo_path)
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: center; gap: 20px;">
            <img src="data:image/png;base64,{logo_base64}" width="300">
            <h1 style="font-size: 60px; font-weight: bold; color: #F2F3F4;">Go Live - Stock Analysis</h1>
        </div>
        <hr style="border: 1px solid #F2F3F4;">
        """,
        unsafe_allow_html=True
    )

# Displays a larger logo in the top-left corner
def display_large_top_left_logo(logo_path="resources/images/logo.png"):
    """
    Auxiliary function to display the logo in the top left
    """
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

# Custom label go live
def custom_label(text, font_size=22, color="#DDE2E5"):
    """
    Displays a custom-styled label using st.markdown.

    Parameters:
        text (str): The label text to display.
        font_size (int): The font size of the label (default is 22px).
        color (str): The hex color of the label text (default is #DDE2E5).
    """
    st.markdown(
        f"<p style='font-size:{font_size}px; color:{color} !important; margin-bottom: -30px;'>{text}</p>", 
        unsafe_allow_html=True
    )

def crop_to_circle(image: Image.Image):
    """
    Crops an image into a circular shape with smooth edges
    """
    size = min(image.size)  # Ensure the image is a square crop
    mask = Image.new("L", (size, size), 0)  # Create a blank mask
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)  # Smooth circle mask

    # Crop image to square first to ensure correct dimensions
    image = ImageOps.fit(image, (size, size), centering=(0.5, 0.5))
    
    # Apply mask with antialiasing
    circular_image = Image.new("RGBA", (size, size))
    circular_image.paste(image, (0, 0), mask)
    return circular_image