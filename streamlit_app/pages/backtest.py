import streamlit as st
from datetime import datetime
import utils
import streamlit.components.v1 as components
import time

utils.display_backtesting_header()
utils.hide_streamlit_sidebar()
utils.navigation_bar()
utils.apply_custom_styles()
utils.hide_streamlit_sidebar()

# Hardcoded list of tickers
tickers = ["AAPL", "MSFT", "BRO", "FAST", "ODFL"]

# Streamlit UI
#st.title("Backtesting Tool")

# Add a negative margin to move "Our Strategy" closer
st.markdown("<div style='margin-top: -100px;'></div>", unsafe_allow_html=True)

# Strategy Section (Now moved up)
st.markdown("<h2 style='margin-bottom: 5px; color: #58A6A6;'>Our Strategy</h2>", unsafe_allow_html=True)
st.markdown("""
<div style="font-size: 20px; line-height: 1.6;">
    This strategy follows the model’s predictions to enter and exit trades. It buys when the model predicts 
    <b>1 (the stock will go up)</b> and holds the position until one of the following happens:
    <br><br>
    1. The price reaches the <b>take profit (TP)</b> level.  
    <br>
    2. The price drops to the <b>stop loss (SL)</b> level.  
    <br>
    3. The model predicts <b>0</b> (<b>sell signal</b>), at which point it exits the trade.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True) 

st.subheader("Do your own backtesting")
st.markdown("""
    <div style="font-size: 20px; line-height: 1.6;">
        The idea is that you now choose a ticker, time period and define your parameters to do your own backtesting!
    </div>
    """, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True) 

# Layout: First row with ticker, start date, and end date
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div style='font-size: 16px;'>Select a Ticker:</div>", unsafe_allow_html=True)
    ticker = st.selectbox("", tickers, help="Choose one of the predefined tickers to test your strategy on.")

with col2:
    st.markdown("<div style='font-size: 16px;'>Start Date:</div>", unsafe_allow_html=True)
    start_date = st.date_input("", value=datetime(2023, 1, 1), help="Select the date when the backtest should begin.")

with col3:
    st.markdown("<div style='font-size: 16px;'>End Date:</div>", unsafe_allow_html=True)
    end_date = st.date_input("", value=datetime(2023, 12, 31), help="Select the date when the backtest should end.")


# Layout: Second row with cash balance, take profit, and stop loss
col4, col5, col6 = st.columns(3)
with col4:
    st.markdown("<div style='font-size: 16px;'>End Date:</div>", unsafe_allow_html=True)
    cash_balance = st.number_input("Cash Balance (USD):", min_value=0, value=10000, step=100, help="Enter the initial amount of cash available for trading.")
with col5:
    st.markdown("<div style='font-size: 16px;'>End Date:</div>", unsafe_allow_html=True)
    take_profit = st.slider("Take Profit (%):", min_value=0.5, max_value=10.0, value=1.0, step=0.1, help="Define the percentage increase at which you want to sell and secure profits.")
with col6:
    st.markdown("<div style='font-size: 16px;'>End Date:</div>", unsafe_allow_html=True)
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
