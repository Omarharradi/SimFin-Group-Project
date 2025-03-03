import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Streamlit UI Config
st.set_page_config(page_title="Go Live", page_icon="📊", layout="wide")  # Set layout to wide for full-page width
st.title("📊 Go Live - Stock Analysis")

# Function to get historical stock data from CSV
@st.cache_data  # Cache to avoid reloading data multiple times
def load_data():
    """
    Load OHLCV stock price data from CSV with optimizations.
    """
    try:
        df = pd.read_csv(
            "../data/us-shareprices-daily.zip", 
            sep=";",
            usecols=["Ticker", "Date", "Open", "High", "Low", "Close", "Volume"],  # Load necessary columns
            dtype={"Ticker": "category", "Open": "float32", "High": "float32", "Low": "float32", "Close": "float32", "Volume": "int64"},  # Optimize memory usage
            parse_dates=["Date"]  # Ensure date is properly parsed
        )
        df.columns = df.columns.str.lower()  # Normalize column names for consistency
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")  # Format dates to remove timestamp
        return df
    except Exception as e:
        st.error(f"❌ Error loading stock data: {e}")
        return pd.DataFrame()

@st.cache_data  # Cache to speed up repeated lookups
def get_historical_data(df, ticker, start="2022-01-01", end="2023-12-31"):
    """
    Fetch and filter historical stock prices for a specific ticker from preloaded data.
    """
    try:
        df_filtered = df.loc[(df["ticker"] == ticker) & (df["date"].between(start, end))]
        df_filtered = df_filtered.sort_values("date").reset_index(drop=True)  # Ensure continuous data
        return df_filtered
    except Exception as e:
        st.error(f"❌ Error fetching stock data: {e}")
        return pd.DataFrame()

# Load data once and use it across function calls
df = load_data()

# Dropdown for ticker selection
ticker = st.selectbox("Select a Stock Ticker:", df["ticker"].unique().tolist())

if ticker:
    historical_data = get_historical_data(df, ticker)

    if historical_data.empty:
        st.warning("No data found for this stock.")
    else:
        st.subheader("📊 Candlestick Chart with Volume")

        def plot_candlestick_chart(df):
            df = df.dropna().reset_index(drop=True)  # Remove missing values to ensure continuity
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            fig.add_trace(
                go.Candlestick(
                    x=df["date"],
                    open=df["open"],
                    high=df["high"],
                    low=df["low"],
                    close=df["close"],
                    name="Candlestick"
                ),
                secondary_y=False,
            )

            colors = np.where(df['close'] >= df['open'], 'green', 'red')
            fig.add_trace(
                go.Bar(
                    x=df["date"],
                    y=df["volume"],
                    marker_color=colors,
                    name="Volume"
                ),
                secondary_y=True,
            )

            # Update layout and axes titles
            fig.update_layout(
                title=f"{ticker} Candlestick Chart with Volume on Secondary Axis",
                template="plotly_dark",
                height=900,  # Increase height for better visualization
                width=1400,   # Increase width for full-page experience
                xaxis=dict(type="category", tickformat="%Y-%m-%d"),  # Format x-axis dates
                xaxis_rangeslider_visible=True,  # Show range slider
                dragmode='zoom'  # Allow zooming and dragging
            )
            #fig.update_yaxes(title_text="Price", secondary_y=False)
            #fig.update_yaxes(title_text="Volume", secondary_y=True)
            # Allow users to manually adjust the y-axis range like TradingView
            fig.update_yaxes(
                title_text="Price",
                autorange=True,  # Automatically adjust the y-axis for the primary y-axis
                secondary_y=False,
                fixedrange=False,  # Allows manual resizing
            )
            fig.update_yaxes(
                title_text="Volume",
                autorange=True,  # Automatically adjust the y-axis for the secondary y-axis
                secondary_y=True,
                fixedrange=False,  # Allows manual resizing
            )

            st.plotly_chart(fig, use_container_width=True)

        plot_candlestick_chart(historical_data)