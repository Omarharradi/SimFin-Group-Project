import sys
import os
import streamlit as st
import utils  # Now import utils.py
from PIL import Image, ImageOps, ImageDraw

utils.set_custom_page_config(title="Home - ForesightX", icon="\U0001F3E0")

def crop_to_circle(image_path, size=(150, 150)):
    image = Image.open(image_path).convert("RGBA")
    image = image.resize(size, Image.LANCZOS)
    
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    
    result = Image.new("RGBA", size, (255, 255, 255, 0))
    result.paste(image, (0, 0), mask)
    return result

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
        \U0001F4C8 Predicts if a stock price will rise or fall using Machine Learning<br>
        \U0001F4CA Provides real-time stock market data<br>
        \U0001F4B9 Suggests Buy, Sell, or Hold decisions
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
    
    # Display team members' images
    st.markdown("## Meet the Dev Team")
    team_images = [
        "resources/images/team_member_1.jpg",
        "resources/images/team_member_2.jpg",
        "resources/images/team_member_3.jpg",
        "resources/images/team_member_4.jpg",
        "resources/images/team_member_5.jpg",
    ]
    
    # Load, crop to circle, and resize images
    resized_images = [crop_to_circle(img, size=(150, 150)) for img in team_images]
    
    # Adjust layout to properly center the second-row images
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1: st.image(resized_images[0], use_container_width=False)
    with col2: st.image(resized_images[1], use_container_width=False)
    with col3: st.image(resized_images[2], use_container_width=False)
    
    col_space1, col4, col_space2, col5, col_space3 = st.columns([0.5, 1, 0.5, 1, 0.5])
    with col4: st.image(resized_images[3], use_container_width=False)
    with col5: st.image(resized_images[4], use_container_width=False)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='font-size:18px;'> 📧 Have feedback? Reach out to us!.</p>",
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()