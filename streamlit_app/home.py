import streamlit as st

def main():
    # Set the title of the homepage
    st.set_page_config(page_title="Home", page_icon=":house:")
    st.title("Automated Daily Trading System")
    

    # Project Overview
    st.header("Project Overview")
    st.write(
        "Welcome to the Automated Daily Trading System! This platform utilizes machine learning "
        "to analyze historical financial data and predict next-day stock market movements. "
        "Our system provides interactive tools to explore trading insights and potential strategies."
    )
    
    # Team Information
    st.header("Development Team")
    st.write("This project is developed by our group as part of a school assignment. Our team is divided into two parts:")
    st.markdown("- **ML Team**: Responsible for building the predictive model using historical stock data.")
    st.markdown("- **DEV Team**: Responsible for building the Streamlit application and integrating the ML model.")
    
    # System Purpose and Objectives
    st.header("System Purpose and Objectives")
    st.write(
        "This trading system is designed to:"
        "\n- Extract and preprocess financial data from SimFin."
        "\n- Develop machine learning models to predict stock price movements."
        "\n- Provide users with an interactive web interface to visualize predictions and trading signals."
        "\n- Deploy the application in a cloud environment for accessibility."
    )
    
    # Instructions for Navigation
    st.header("How to Use the Application")
    st.write(
        "\n- Navigate to the **'Go Live'** page to analyze stocks and view predictions."
        "\n- Select a stock ticker to retrieve financial data and predictions."
        "\n- Explore various analytics and model insights provided by the system."
    )
    
    # Footer with contact information (optional)
    st.markdown("---")
    st.write("For any inquiries, please reach out to our development team.")

if __name__ == "__main__":
    main()
