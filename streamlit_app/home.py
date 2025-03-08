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
    
    #  Quick Overview of the App
    st.header("Overview of the App")
    st.write(
        "Predicts if a stock price will rise or fall using Machine Learning"
        "\n- Provides real-time stock market data"
        "\n- Suggests Buy, Sell, or Hold decisions"
    )
    
    st.header("Easy Steps to Get Started")
    st.write("✅ **Step 1:** Go to the 'Predictor' page and select the ticker (AAPL, MSFT, BRO, FAST, and ODFL).")
    st.write("✅ **Step 2:** View real-time stock data & our AI-powered prediction.")
    st.write("✅ **Step 3:** Check trading recommendations for next day.")
    st.write("✅ **Step 4:** Review the past performance.")

    # Team Information
    st.header("Development Team")
    st.write("🔍 This project is developed by our group as part of a school assignment.")
    st.markdown("- **ML Team**: Responsible for building the predictive model.")
    st.markdown("- **DEV Team**: Responsible for building the Streamlit application and integrating the ML model.")
    
    st.markdown("📧 Have feedback? Reach out to us!")

    # Footer
    st.markdown("---")
    st.write("For any inquiries, please reach out to our development team.")

if __name__ == "__main__":
    main()