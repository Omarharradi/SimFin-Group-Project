import streamlit as st
import utils 
from PIL import Image

#First line of the whole app needs to be the page config:
utils.set_custom_page_config(title="Home - ForesightX", icon="\U0001F3E0")

def main():
    # Apply overall styling to the page
    utils.hide_streamlit_sidebar()
    utils.navigation_bar()
    #utils.apply_custom_styles()
    utils.display_home_header()
    utils.hide_streamlit_sidebar()
    
    # Quick Overview of the App with larger text for readability
    st.markdown("<br>", unsafe_allow_html=True) 
    st.markdown("# Overview of the App", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='font-size:22px;'>
        \U0001F4CA Provides historical and real-time stock market data<br>
        \U0001F4C8 Predicts if a stock price will rise or fall today using Machine Learning<br>
        \U0001F4B9 Suggests Buy, Sell, or Hold decisions and let's you try them out in our interactive Backtesting Module!
        </p>
        """,
        unsafe_allow_html=True,
    )
    
    # Easy Steps to Get Started
    st.markdown("<br>", unsafe_allow_html=True) 
    st.markdown("# Easy Steps to Get Started", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='font-size:22px;'>
        \U0001F3E6 <strong>Step 1:</strong> Review the company's information to understand its fundamentals.<br>
        \U0001F4D6 <strong>Step 2:</strong> Visit the Prediction page and select a stock ticker (AAPL, MSFT, BRO, FAST, ODFL) you wish to analyze.<br>
        \U0001F4C5 <strong>Step 3:</strong> Access historical and real-time stock data as well as our AI-generated prediction for that stock!<br>
        \U0001F680 <strong>Step 4:</strong> Analyze our trading recommendations for the upcoming trading session.<br>
        \U0001F50D <strong>Step 5:</strong> Utilize the Backtesting Tool to validate trading strategies and evaluate the model performance.<br>
        </p>
        """,
        unsafe_allow_html=True,
    )
    
    # Team Information
    st.markdown("<br>", unsafe_allow_html=True) 
    st.markdown("# Development Team", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='font-size:22px;'>
        🔍 This project is developed by our group as part of a school assignment<br>
        👨‍💻 ML Team: Responsible for building the predictive model<br>
        🛠️ DEV Team: Responsible for building the Streamlit application and integrating the ML model
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True) 
    
    # Display team members' images
    st.markdown("## Meet the ForesightX Team")
    st.markdown("<br><br>", unsafe_allow_html=True) 
    team_names = ["Ignacio Amigó", "Omar Harradi", "Afonso Santos", "Lucas Ihnen", "Laura Silva"]
    team_images = [
        "resources/images/team_member_1.jpg",
        "resources/images/team_member_2.jpg",
        "resources/images/team_member_3.jpg",
        "resources/images/team_member_4.jpg",
        "resources/images/team_member_5.jpg",
    ]
    
    # Load, crop to circle, and resize images
    resized_images = [utils.crop_to_circle(Image.open(img)) for img in team_images]
    
    # Adjust layout to properly center the second-row images with names
    col1, col2, col3 = st.columns([1, 1, 1])
    width = 380
    with col1: 
        st.image(resized_images[0], use_container_width=False, width=width)
        st.markdown(f"<p style='text-align:center; font-size:22px;'>{team_names[0]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; font-size:16px;'>Machine Learning Team</p>", unsafe_allow_html=True)
    with col2: 
        st.image(resized_images[1], use_container_width=False, width=width)
        st.markdown(f"<p style='text-align:center; font-size:22px;'>{team_names[1]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; font-size:16px;'>Machine Learning Team</p>", unsafe_allow_html=True)
    with col3: 
        st.image(resized_images[2], use_container_width=False, width=width)
        st.markdown(f"<p style='text-align:center; font-size:22px;'>{team_names[2]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; font-size:16px;'>Machine Learning Team</p>", unsafe_allow_html=True)
    
    col_space1, col4, col_space2, col5, col_space3 = st.columns([0.5, 1, 0.5, 1, 0.5])
    with col4: 
        st.image(resized_images[3], use_container_width=False, width=width)
        st.markdown(f"<p style='text-align:center; font-size:22px;'>{team_names[3]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; font-size:16px;'>Developer Team</p>", unsafe_allow_html=True)
    with col5: 
        st.image(resized_images[4], use_container_width=False, width=width)
        st.markdown(f"<p style='text-align:center; font-size:22px;'>{team_names[4]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; font-size:16px;'>Developer Team</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(
        "<p style='font-size:22px;'> 📧 Have feedback? <a href='mailto:dsierra@faculty.ie.edu'>Reach out to us!</a></p>",
    unsafe_allow_html=True,
)
if __name__ == "__main__":
    main()