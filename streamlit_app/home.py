import streamlit as st
import base64
import utils


def get_base64_of_image(image_path):
    """Function to encode the image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Set page layout first
utils.set_custom_page_config(title="Home - ForesightX", icon="🏠")

# Add navigation
utils.navigation_bar()

# Hide Streamlit's default sidebar
utils.hide_streamlit_sidebar()

def main():

    # Path to the logo image
    logo_path = "logo.png"  # Ensure this path is correct
    logo_base64 = get_base64_of_image(logo_path)
    
    # Apply full-page styling with CSS
    st.markdown(
        f"""
        <style>
            /* Background color */
            .stApp {{
                background-color: #002149;
            }}

            /* Container for logo and title */
            .header-container {{
                display: flex;
                align-items: center;
                justify-content: center; /* Centers everything */
                gap: 15px;
                padding: 10px;
                width: 100%;
            }}

            /* Logo styling */
            .logo img {{
                width: 300px; /* Adjust size */
                height: auto;
            }}

            /* Title styling */
            .title {{
                font-size: 60px;
                font-weight: bold;
                color: #F2F3F4;
                text-align: center;
                width: 100%;
                display: block;
            }}

            /* Heading colors */
            h1, h2, h3 {{
                color: #05CC77;
            }}

            /* Text Input */
            .stTextInput>div>div>input {{
                background-color: #004080;
                color: white;
                border-radius: 5px;
            }}

            /* Button Styling */
            .stButton>button {{
                background-color: #05CC77;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }}

            /* Subtitle Styling (Bigger & Centered) */
            .subtitle {{
                font-size: 35px; /* Increased size */
                font-weight: bold; /* Make it stand out */
                color: #05CC77; /* Keep the green color */
                text-align: center; /* Centers the text */
                width: 100%;
                display: block;
                margin-top: 10px;
            }}

            /* Horizontal line styling */
            .line {{
                border: 1px solid #05CC77;
                margin-top: 10px;
                margin-bottom: 10px;
                width: 100%;
            }}
        </style>

        <div class="header-container">
            <div class="logo">
                <img src="data:image/png;base64,{logo_base64}" alt="Company Logo">
            </div>
            <div class="title">
                Welcome to Foresightx
            </div>
        </div>

        <hr class="line">

        <div class="subtitle">
            Your AI-Powered Stock Prediction Assistant!
        </div>

        <hr class="line"> 
        """,
        unsafe_allow_html=True)
    
    
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
    st.write("🔍 This project is developed by our group as part of a school assignment. Our team is divided into two parts:")
    st.markdown("- **ML Team**: Responsible for building the predictive model using historical stock data.")
    st.markdown("- **DEV Team**: Responsible for building the Streamlit application and integrating the ML model.")
    
    st.markdown("📧 Have feedback? Reach out to us!")

    # Footer with contact information (optional)
    st.markdown("---")
    st.write("For any inquiries, please reach out to our development team.")

if __name__ == "__main__":
    main()