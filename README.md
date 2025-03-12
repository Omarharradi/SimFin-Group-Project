# Automated Daily Trading System

## Overview

This project involves the development of an **Automated Daily Trading System** using Python. The system consists of two main components:

1. **Data Analytics Module** – A machine learning model for market movement forecasting using at least five US companies.
2. **Web-Based Application** – A multi-page interactive web application developed with **Streamlit** that allows users to visualize predictive analytics and interact with the trading system.

## Features

### 1. Data Analytics Module

- **ETL Pipeline**: Extracts, transforms, and loads stock market data from SimFin.
- **Machine Learning Model**: Predicts market movement (price rise or fall) for the next trading session.
- **Trading Strategy**: Implements a trading decision mechanism based on the model’s predictions.

### 2. Web-Based Trading System

- **Python API Wrapper**: Retrieves real-time stock market data from SimFin.
- **Interactive UI**: Users can select stock tickers and view real-time and historical data.
- **Predictive Analytics Dashboard**: Displays stock price predictions and trading signals.
- **Cloud Deployment**: Hosted on a cloud platform for public access.

## Data Source

The project utilizes financial data from **SimFin (Simple Financials)**:

- Historical and real-time financial metrics.
- Share prices, income statements, balance sheets, and cash flow reports.
- Data is retrieved via **bulk downloads** (historical) and the **SimFin API** (real-time).

## Technologies Used

- **Python** (for ETL, ML, API interaction)
- **Pandas** (for data processing)
- **Scikit-Learn / TensorFlow** (for machine learning models)
- **Streamlit** (for web application development)
- **SimFin API** (for financial data retrieval)
- **Matplotlib / Plotly / SeaBorn** (for data visualization)

## Installation

To run the project locally, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo-url.git
   cd your-repo-folder

