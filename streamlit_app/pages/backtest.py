import streamlit as st
from datetime import datetime
import utils
import streamlit.components.v1 as components
import time

utils.set_custom_page_config(title="Backtesting - ForesightX", icon="🏢")

# Hardcoded list of tickers
tickers = ["AAPL", "MSFT", "BRO", "FAST", "ODFL"]

# Streamlit UI
st.title("Backtesting Tool")

# Strategy Section
st.subheader("Our Strategy")
st.markdown("""
This strategy follows the model’s predictions to enter and exit trades. It buys when the model predicts **1 (the stock will go up)** and holds the position until one of the following happens:

1. The price reaches the **take profit (TP)** level.  
2. The price drops to the **stop loss (SL)** level.  
3. The model predicts **0** (**sell signal**), at which point it exits the trade.
""")

st.subheader("Do your own backtesting")
st.text("The idea is that you now choose a ticker, time period and define your parameters to do your own backtesting!")

# Layout: First row with ticker, start date, and end date
col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.selectbox("Select a Ticker:", tickers, help="Choose one of the predefined tickers to test your strategy on.")
with col2:
    start_date = st.date_input("Start Date:", value=datetime(2023, 1, 1), help="Select the date when the backtest should begin.")
with col3:
    end_date = st.date_input("End Date:", value=datetime(2023, 12, 31), help="Select the date when the backtest should end.")

# Layout: Second row with cash balance, take profit, and stop loss
col4, col5, col6 = st.columns(3)
with col4:
    cash_balance = st.number_input("Cash Balance (USD):", min_value=0, value=10000, step=100, help="Enter the initial amount of cash available for trading.")
with col5:
    take_profit = st.slider("Take Profit (%):", min_value=0.5, max_value=10.0, value=1.0, step=0.1, help="Define the percentage increase at which you want to sell and secure profits.")
with col6:
    stop_loss = st.slider("Stop Loss (%):", min_value=0.5, max_value=10.0, value=1.0, step=0.1, help="Define the percentage decrease at which you want to sell to limit losses.")

# Backtest Button
if st.button("Backtest"):
    with st.spinner("🏃Running backtest... This may take a few seconds!🏃"):
        time.sleep(1)  # Small delay to show the spinner before processing
        result_df, html_content, log_info = utils.backtest([ticker], start_date, end_date, cash_balance, tp=take_profit/100, sl=stop_loss/100)
    
    st.subheader("Performance Chart")
    components.html(html_content, height=700, scrolling=True)  # Embed directly

    st.subheader("Backtest Log")
    st.text(log_info)
