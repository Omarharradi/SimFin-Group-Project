import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the data
price = pd.read_csv("data/us-shareprices-daily.csv", delimiter=";")
ohlc_df = price[price["Ticker"].isin(["KHC"])]

# Create a figure with a secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add candlestick trace
fig.add_trace(
    go.Candlestick(
        x=ohlc_df['Date'],  # Ensure that you use the 'Date' column here
        open=ohlc_df['Open'],
        high=ohlc_df['High'],
        low=ohlc_df['Low'],
        close=ohlc_df['Close'],
        name='Candlestick'
    ),
    secondary_y=False,
)

# Add volume trace
colors = np.where(ohlc_df['Close'] >= ohlc_df['Open'], 'green', 'red')
fig.add_trace(
    go.Bar(
        x=ohlc_df['Date'],  # Use 'Date' here as well
        y=ohlc_df['Volume'],
        marker_color=colors,
        name='Volume'
    ),
    secondary_y=True,
)

# Update layout and axes titles
fig.update_layout(
    title='Candlestick Chart with Volume on Secondary Axis',
    xaxis_title='Date',
    yaxis_title='Price',
    yaxis2_title='Volume',
    xaxis_rangeslider_visible=True,  # Show range slider
    dragmode='zoom',  # Allow zooming and dragging
)

# Allow users to manually adjust the y-axis range like TradingView
fig.update_yaxes(
    autorange=True,  # Automatically adjust the y-axis for the primary y-axis
    secondary_y=False,
    fixedrange=False,  # Allows manual resizing
)
fig.update_yaxes(
    autorange=True,  # Automatically adjust the y-axis for the secondary y-axis
    secondary_y=True,
    fixedrange=False,  # Allows manual resizing
)

# Show the figure
fig.show()
