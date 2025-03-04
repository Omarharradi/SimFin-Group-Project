import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from datetime import datetime, timedelta

# Streamlit UI Config
st.set_page_config(page_title="Go Live", page_icon="📊", layout="wide")
st.title("📊 Go Live - Stock Analysis")

# Define PySimFin class
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

# Initialize API
#API_KEY = st.secrets["SIMFIN_API_KEY"]  # Store the API key securely in Streamlit Secrets
API_KEY = "0ce27565-392d-4c49-a438-71e3b39f298f"
simfin = PySimFin(API_KEY)

# Define allowed tickers
tickers = ["AAPL", "MSFT", "BRO", "FAST", "ODFL"]

# Dropdown for ticker selection
ticker = st.selectbox("Select a Stock Ticker:", tickers)

# Dropdown for time period selection
time_periods = {
    "Last Week": 7,
    "Last Month": 30,
    "Last 3 Months": 90,
    "Last 6 Months": 180,
    "Last Year": 365,
    "Custom": None  # Placeholder for user input
}
selected_period = st.selectbox("Select Time Period:", list(time_periods.keys()))

# Custom time period input (if user selects "Custom")
if selected_period == "Custom":
    custom_days = st.number_input("Enter custom period (1 to 730 days):", min_value=1, max_value=730, value=30)
    days = custom_days
else:
    days = time_periods[selected_period]

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

            def plot_candlestick_chart(df):
                df = df.dropna(subset=["open", "high", "low", "close", "volume"]).reset_index(drop=True)
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
                        name="Volume",
                        opacity=0.3  # Reduce opacity to make it dimmer
                    ),
                    secondary_y=True,
                )

                fig.update_layout(
                    title=f"{ticker} Candlestick Chart with Volume",
                    template="plotly_dark",
                    height=900,
                    width=1400,
                    xaxis=dict(
                        type="category",  # Ensure only existing dates are plotted
                        tickformat="%Y-%m-%d"
                    ),
                    xaxis_rangeslider_visible=True,
                    dragmode='zoom'
                )
                fig.update_yaxes(title_text="Price", secondary_y=False, fixedrange=False)
                fig.update_yaxes(title_text="Volume", secondary_y=True, fixedrange=False, showgrid=False, zeroline=False)

                st.plotly_chart(fig, use_container_width=True)

            plot_candlestick_chart(stock_data)
    except Exception as e:
        st.error(f"❌ Error fetching stock data: {e}")