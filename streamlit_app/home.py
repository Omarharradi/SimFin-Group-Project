import sys
import os
import streamlit as st
import utils  # Now import utils.py

utils.set_custom_page_config(title="Home - ForesightX", icon="🏠")
def main():
    utils.hide_streamlit_sidebar()
    utils.navigation_bar()
    utils.apply_custom_styles()
    utils.display_home_header()
    
    # Quick Overview of the App with larger text for readability
    st.markdown("# Overview of the App", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='font-size:22px;'>
        📈 Predicts if a stock price will rise or fall using Machine Learning<br>
        📊 Provides real-time stock market data<br>
        💹 Suggests Buy, Sell, or Hold decisions
        </p>
        """,
        unsafe_allow_html=True,
    )
    
    # Easy Steps to Get Started
    st.markdown("# Easy Steps to Get Started", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='font-size:22px;'>
        ✅ Step 1: Go to the 'Predictor' page and select the ticker (AAPL, MSFT, BRO, FAST, and ODFL).<br>
        ✅ Step 2: View real-time stock data & our AI-powered prediction.<br>
        ✅ Step 3: Check trading recommendations for next day.<br>
        ✅ Step 4: Review the past performance.
        </p>
        """,
        unsafe_allow_html=True,
    )
    
    # Team Information
    st.markdown("# Development Team", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='font-size:22px;'>
        🔍 This project is developed by our group as part of a school assignment.<br>
        👨‍💻 ML Team: Responsible for building the predictive model.<br>
        🛠️ DEV Team: Responsible for building the Streamlit application and integrating the ML model.
        </p>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        "<p style='font-size:18px;'> 📧 Have feedback? Reach out to us!.</p>",
        unsafe_allow_html=True,
    )
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='font-size:18px;'>For any inquiries, please reach out to our development team.</p>",
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()