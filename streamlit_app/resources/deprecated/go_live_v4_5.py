import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import utils
import time

# Streamlit UI Config
st.set_page_config(page_title="Go Live", page_icon="📊", layout="wide")
st.title("📊 Go Live - Stock Analysis")

# Add navigation
utils.navigation_bar()

# Hide Streamlit's default sidebar
#utils.hide_streamlit_sidebar()

# Initialize API
API_KEY = "0ce27565-392d-4c49-a438-71e3b39f298f"
simfin = utils.PySimFin(API_KEY)

# Define allowed tickers
tickers = ["AAPL", "MSFT", "BRO", "FAST", "ODFL"]

# Dropdown for ticker selection
ticker = st.selectbox("Select a Stock Ticker:", tickers, key="selected_ticker")

# Dropdown for time period selection
time_periods = {
    "Last Week": 7,
    "Last Month": 30,
    "Last 3 Months": 90,
    "Last 6 Months": 180,
    "Last Year": 365,
    "Custom": None  # Placeholder for user input
}
selected_period = st.selectbox("Select Time Period:", list(time_periods.keys()), key="selected_period")

# Custom time period input (if user selects "Custom")
if selected_period == "Custom":
    custom_days = st.number_input("Enter custom period (1 to 730 days):", min_value=1, max_value=730, value=30, key="custom_days")
    days = custom_days
else:
    days = time_periods[selected_period]

# Reset latest data if ticker or period changes
if ("latest_data" in st.session_state and
    (st.session_state.get("prev_ticker") != ticker or st.session_state.get("prev_days") != days)):
    st.session_state.latest_data = None

# Store previous selection to detect changes
st.session_state["prev_ticker"] = ticker
st.session_state["prev_days"] = days

if ticker and days:
    try:
        # Fetch stock data based on user selection
        stock_data = simfin.get_stock_prices([ticker], days=days)
        stock_data = stock_data.rename(columns={
            "Date": "date", "Opening Price": "open", "Highest Price": "high", 
            "Lowest Price": "low", "Last Closing Price": "close", "Trading Volume": "volume"
        })
        
        # Ensure date is in datetime format and sort by date
        stock_data["date"] = pd.to_datetime(stock_data["date"])
        stock_data = stock_data.sort_values(by="date")
        
        # Convert date to string format to remove timestamp
        stock_data["date"] = stock_data["date"].dt.strftime("%Y-%m-%d")
        
        if stock_data.empty:
            st.warning("No data found for this stock.")
        else:
            st.subheader("📊 Candlestick Chart with Volume")
            
            # Reset latest data when ticker or period changes
            st.session_state.latest_data = stock_data

            # Placeholder for dynamic chart updates
            chart_placeholder = st.empty()
            
            def plot_candlestick_chart(df):
                df = df.dropna(subset=["open", "high", "low", "close"]).reset_index(drop=True)
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

                if "volume" in df.columns:
                    colors = np.where(df['close'] >= df['open'], 'green', 'red')
                    fig.add_trace(
                        go.Bar(
                            x=df["date"],
                            y=df["volume"],
                            marker_color=colors,
                            name="Volume",
                            opacity=0.3
                        ),
                        secondary_y=True,
                    )
                
                fig.update_layout(
                    title=f"{ticker} Candlestick Chart with Volume",
                    template="plotly_dark",
                    height=900,
                    width=1400,
                    xaxis=dict(type="category", tickformat="%Y-%m-%d"),
                    xaxis_rangeslider_visible=True,
                    dragmode='zoom'
                )
                fig.update_yaxes(title_text="Price", secondary_y=False)
                fig.update_yaxes(title_text="Volume", secondary_y=True, showgrid=False, zeroline=False)
                
                return fig
            
            # Continuous update loop for new data
            while True:
                today_data = utils.fetch_latest_ohlc([ticker])
                if not today_data.empty:
                    today_data["date"] = datetime.now().strftime("%Y-%m-%d")
                    today_data = today_data.rename(columns={
                        "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"
                    })
                    #today_data["volume"] = 0  # Assign volume as 0 if missing
                    today_data["Ticker"] = ticker  # Ensure ticker is assigned
                    today_data = today_data[["date", "open", "high", "low", "close", "volume", "Ticker"]]
                    
                    # Append today's updated data
                    st.session_state.latest_data = pd.concat([
                        st.session_state.latest_data,
                        today_data
                    ], ignore_index=True).drop_duplicates(subset=["date"], keep="last")
                
                # Update chart dynamically without refreshing the page
                chart_placeholder.plotly_chart(plot_candlestick_chart(st.session_state.latest_data), use_container_width=True)
                
                time.sleep(10)  # Wait for 10 seconds before updating again
    except Exception as e:
        st.error(f"❌ Error fetching stock data: {e}")
