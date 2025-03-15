# ForeSightX - Automated Trading System
Group 11: Omar Harradi, Laura Silva, Ignacio Amigó, Afonso Santos, Lucas Ihnen

- [ForeSightX - Automated Trading System](#foresightx---automated-trading-system)
  - [Overview](#overview)
    - [1. Data Analytics Module](#1-data-analytics-module)
    - [2. Web-Based Live App](#2-web-based-live-app)
  - [Data Sources](#data-sources)
  - [Technologies Used](#technologies-used)
  - [Deliverables](#deliverables)
    - [GitHub Repository](#github-repository)
    - [Live Web App](#live-web-app)
    - [Executive summary](#executive-summary)
    - [Video Presentation](#video-presentation)
   
## Overview
This project is made for the Python for Data Analytics II class on the IE University's Master for Business Analytics and Data Science.

It involves the development of an **Automated Daily Trading System** using Python. The system consists of two main components:

1. **Data Analytics Module** – A machine learning model for market movement forecasting using at least five US companies.
2. **Web-Based Application** – A multi-page interactive web application developed with **Streamlit** that allows users to visualize predictive analytics and interact with the trading system, as well as simulate backtesting strategies!

### 1. Data Analytics Module

- **ETL Pipeline**: Extracts, transforms, and loads stock market data from SimFin. 
- **Machine Learning Model**: Predicts market movement (price rise or fall) for the next trading session.
- **Trading Strategy**: Implements a trading decision mechanism based on the model’s predictions.

### 2. Web-Based Live App

- **Python API Wrapper**: Retrieves real-time stock market data from SimFin.
- **Interactive UI**: Users can select stock tickers and view real-time and historical data.
- **Predictive Analytics Dashboard**: Displays stock movement predictions and trading signals.
- **Backtesting Module**: Given our trained model intelligence, you can select parameters to backtest your position holding strategy.
- **Cloud Deployment**: Hosted on Streamlit cloud for public access.

The last version of the application can be found [clicking here](https://g11-pda2-foresightx.streamlit.app/)

## Data Sources

The project utilizes the following data sources:
- Financial data from **SimFin (Simple Financials)**:
  - Historical (bulk download) for model training
  - On-demand financial metrics from the SimFin API using our Python Wrapper and calling the compant prices endpoint
  - Company information from the companies endpoint on the SimFin API
- Real time mid-day trading data from **yFinance**:
  - If the market is open, the idea is that you select a ticker and visualize the market movements updated every 20 seconds to see how well our prediction compares to the actual market movements!
- Company logo information from **[logo.dev](https://www.logo.dev/):**
  - All credit on obtaining ticker logos on demand, in high quality and in a standardized size goes to the Logo.dev team!


## Technologies Used

- **Python** (for ETL, ML, API interaction)
- **Pandas** (for data processing)
- **Scikit-Learn / XGBoost** (for machine learning models and different iterations)
- **Streamlit** (for web application development)
- **SimFin API** (for financial data retrieval)
- **YFinance API** (for real time trading data)
- **Logo.dev API** (for high quality logo retrieval)
- **Matplotlib / Plotly / SeaBorn / Backtesting** (for data visualization)

## Deliverables
### GitHub Repository
It has many different folders:
  - **machine_learning/** *(Main folder containing all machine learning pipeline scripts)*
    - `etl.py` → Extracts, transforms, and loads stock price data from the `data/` folder.
    - `model_training.py` → Trains an XGBoost model using processed data, obtained from the `etl.py` script.
    - `master_pipeline.py` → Orchestrates the execution of both `etl.py` and `model_training.py` in sequence.
    - `logging/` → Stores logs for each script to track execution and debugging.
    - `output/` → Stores the generated objects for the ETL and Model Training Scripts!
    - A `requirements_master.txt` file is included for easy dependencies setup. Install them using
      ```sh
      pip install -r requirements_master.txt
      ```
  - **data/** *(Required for the ETL script)*
    - **Make sure the following files are present before running `etl.py`:**
      - `us-companies.zip`
      - `us-shareprices-daily.zip`
    - These files can be downloaded from the **Bulk Download section** of the **SimFin API**.
    - These files are not uploaded in this repository because of their size and are also ignored within the `.gitignore` file.
  - **resources/**:
      - Folder to organize whatever doesnt fit in the other two, like reference code we tried out and the instructions for the assignment
  - **streamlit_app/**:
      - contains the complete structure for the streamlit app deployment with the best practices:
        - ```home.py```: main file for the app to exist
        - ```./pages/```: contains the sub-pages for the streamlit app 
          - ```backtest.py```: For our backtesting strategy
          - ```company_info_v1.py```: Reviewing company ticker information
          - ```go_live_v5.1.py```: Main functionality of our app, considering both historical and real time financial data as well as a live prediction
        - ```./resources/"```:
          - deprecated: where we left all previous versions of the pages developed
          - images: all images required for the app to work 
          - model: contains the XGBoost model object trained in the machine_learning folder for the app to make live predictions
        - [requirements.txt](streamlit_app/requirements.txt) file with all the libraries required for the app to work.
          - Note: This is the requirements.txt for the streamlit app, do not mix up with the dependencies you could install for your execution of the `master_pipeline.py` script.
    
  - Also included a `.gitignore` file obtained from [gitignore.io](gitignore.io), and a few customized tweaks.

### Live Web App
Deployed in Streamlit cloud and accessed publicly [clicking here](https://g11-pda2-foresightx.streamlit.app/)


### Executive summary
To have a quick read about everything we created on this project, refer to our [Executive Summary documentation](PDA2_G11_Executive_Summary.pdf) which can also be found within this repository!
  
### Video Presentation
  - The video recorded was uploaded to a Google Drive folder and made publicly available [in this link](https://drive.google.com/drive/folders/1Q3PMHrujXyme3BMmPqNvwbcuoiVDUuBi?usp=sharing)
    - The video contains a summary of part 1 and a live demo of our application working!
    - There is also a second video that showcases how our app is able to capture real time trading data when the market is open! (same folder)
    - Lastly, a screenshot on how it looks when the market is closed and no predictions are showed.
  - The presentation used is also within this repository, [click here to see it](PDA2_G11_SlideDeck.pdf)


