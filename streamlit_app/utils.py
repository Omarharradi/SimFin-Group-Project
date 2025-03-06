import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

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