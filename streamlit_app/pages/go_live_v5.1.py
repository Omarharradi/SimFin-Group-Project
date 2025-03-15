import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import utils
from utils import custom_label
import time

# Utils for standardized look and feel:
utils.set_custom_page_config(title="Prediction - ForesightX", icon="📊")
utils.hide_streamlit_sidebar()
utils.navigation_bar()
#utils.apply_custom_styles()
utils.display_predictor_header()

# Initialize API
API_KEY = "0ce27565-392d-4c49-a438-71e3b39f298f"
simfin = utils.PySimFin(API_KEY)

# Prediction data with cache (to execute it just once per session)
@st.cache_data
def get_cached_predictions():
    to_predict = simfin.get_predictions_data()
    return utils.predict_market(to_predict)

# Define allowed tickers
tickers = ["AAPL", "MSFT", "BRO", "FAST", "ODFL"]

# Display custom-styled label for the stock ticker dropdown
custom_label("Select a Stock Ticker:")

# Ticker Selectbox with no label (since we already added a custom label above)
ticker = st.selectbox("", tickers, key="selected_ticker")

# Dictionary for time periods
time_periods = {
    "Last Week": 7,
    "Last Month": 30,
    "Last 3 Months": 90,
    "Last 6 Months": 180,
    "Last Year": 365,
    "Custom": None  # Placeholder for user input
}

# Display custom-styled label for the time period dropdown
custom_label("Select Time Period:")

# Time Period Selectbox with no label
selected_period = st.selectbox("", list(time_periods.keys()), key="selected_period")

# Custom time period input (if user selects "Custom")
if selected_period == "Custom":
    custom_days = st.number_input("Enter custom period (1 to 730 days):", min_value=1, max_value=730, value=30, key="custom_days")
    days = custom_days
else:
    days = time_periods[selected_period]

# Fetch stock data based on user selection
if ticker and days:
    try:
        if utils.is_trading_day(): #Understands if it is a trading day or not!
            # Get predictions from cache only if today makes sense to predict
            predictions_df = get_cached_predictions()
            predicted_value = predictions_df.loc[predictions_df["Ticker"] == ticker, "Prediction"].values[0]
            market_movement = "go up 📈" if predicted_value >= 0.5 else "go down 📉"

            # Banner displayed:
            st.markdown(
                f"""
                <style>
                    .banner-container {{
                        position: relative;
                        display: inline-block;
                        width: 100%;
                    }}
                    .banner {{
                        background-color:#f0f0f0;
                        padding:10px;
                        border-radius:5px;
                        text-align:center;
                        font-size:16px;
                        color:black;
                        cursor: help;
                    }}
                    .tooltip-text {{
                        visibility: hidden;
                        width: 280px;
                        background-color: black;
                        color: white;
                        text-align: center;
                        border-radius: 5px;
                        padding: 5px;
                        position: absolute;
                        z-index: 1;
                        top: -40px;
                        left: 50%;
                        transform: translateX(-50%);
                        opacity: 0;
                        transition: opacity 0.3s;
                        font-size: 14px;
                    }}
                    .banner-container:hover .tooltip-text {{
                        visibility: visible;
                        opacity: 1;
                    }}
                </style>

                <div class="banner-container">
                    <div class="banner">
                        <b>The ticker {ticker} for today's market movement is expected to {market_movement} based on yesterday's stock movement!</b>
                    </div>
                    <div class="tooltip-text">The {ticker} ticker has a model prediction value of {predicted_value:.4f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("Note: You can hover over the banner to know the model's predicted value")

        else: #Banner to show in case today there is no prediction because of market being closed:
            st.markdown(
                f"""
                <div style="background-color:#f0f0f0; padding:10px; border-radius:5px; text-align:center; font-size:16px; color:black;">
                    📢 <b>The market is closed today! There are no predictions for today.</b><br>
                    🕒 US Market operates from 9:30 AM to 4:00 PM ET, Monday to Friday.<br>
                    You can still see the past days movement and try out our backtesting feature!
                </div>
                """,
                unsafe_allow_html=True
            )

        # Gets the stock data through the wrapper for the selected ticker and days:
        stock_data = simfin.get_stock_prices([ticker], days=days)
        stock_data = stock_data.rename(columns={
            "Date": "date", "Opening Price": "open", "Highest Price": "high", 
            "Lowest Price": "low", "Last Closing Price": "close", "Trading Volume": "volume"
        })
        
        stock_data["date"] = pd.to_datetime(stock_data["date"])
        stock_data = stock_data.sort_values(by="date")
        stock_data["date"] = stock_data["date"].dt.strftime("%Y-%m-%d")
        
        if stock_data.empty:
            st.warning("No data found for this stock.")
        else:
            st.markdown("<br><br>", unsafe_allow_html=True) 
            st.markdown("<h2 style='text-align: center;'>📊 Candlestick Chart with Volume</h2>", unsafe_allow_html=True)
            chart_placeholder = st.empty()
            
            # Plots the candlestick chart:
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
            
            # Stores the latest data with whatever gets retrieved, only updated when you change something from the selection:
            st.session_state.latest_data = stock_data
            
            while True:
                # Gets into a loop to update every 20 seconds the real time data from Y finance
                if utils.is_market_open():
                    today_data = utils.fetch_latest_ohlc([ticker]) # Calls yfinance API to obtain the ticker movements for today
                    if not today_data.empty:
                        today_data["date"] = datetime.now().strftime("%Y-%m-%d")
                        today_data = today_data.rename(columns={
                            "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"
                        })
                        today_data["Ticker"] = ticker
                        today_data = today_data[["date", "open", "high", "low", "close", "volume", "Ticker"]]
                        st.session_state.latest_data = pd.concat([
                            st.session_state.latest_data,
                            today_data
                        ], ignore_index=True).drop_duplicates(subset=["date"], keep="last")
                
                chart_placeholder.plotly_chart(
                        plot_candlestick_chart(st.session_state.latest_data),
                        use_container_width=True,
                        key=f"candlestick_chart_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    )
                time.sleep(20)  # Check every 10 seconds

    except Exception as e:
        # Raises Exception when you move too fast through the page: Streamlit can easily execute more than 2 requests per second, prompting you to wait and retry! 
        st.error(f"❌ Error fetching stock data, the free version of the SimFin API has a limit of 2 requests per second. Refresh the page or select again!")
