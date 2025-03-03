import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit UI Config
st.set_page_config(page_title="Go Live", page_icon="📊")
st.title("📊 Go Live - Stock Analysis")

# Function to get historical stock data from CSV
@st.cache_data  # Cache to avoid reloading data multiple times
def load_data():
    """
    Load stock price data from CSV with optimizations.
    """
    try:
        df = pd.read_csv(
            "../data/us-shareprices-daily.zip", 
            sep=";",
            usecols=["Ticker", "Date", "Close"],  # Load only necessary columns
            dtype={"Ticker": "category", "Close": "float32"},  # Optimize memory usage
            parse_dates=["Date"]  # Ensure date is properly parsed
        )
        df.columns = df.columns.str.lower()  # Normalize column names for consistency
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
        st.subheader("📊 Stock Price Trend")

        # Plot with Plotly
        def plot_stock_prices(df):
            fig = px.line(
                df, x="date", y="close",
                title=f"{ticker} Stock Price Over Time",
                labels={"date": "Date", "close": "Stock Price ($)"},
                line_shape="linear",
                template="plotly_dark",  # Better aesthetics
            )
            fig.update_traces(line=dict(color="blue"))  # Customize line color
            fig.update_xaxes(rangeslider_visible=True)  # Adds a range slider for zooming
            st.plotly_chart(fig, use_container_width=True)  # Fit to Streamlit width

        plot_stock_prices(historical_data)
