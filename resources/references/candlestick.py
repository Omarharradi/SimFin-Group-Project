import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

price = pd.read_csv("data/us-shareprices-daily.csv", delimiter=";")
ohlc_df = price[price["Ticker"].isin(["KHC"])]

# Create a figure with a secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])


fig.add_trace(
    go.Candlestick(
        x=ohlc_df.index,
        open=ohlc_df['Open'],
        high=ohlc_df['High'],
        low=ohlc_df['Low'],
        close=ohlc_df['Close'],
        name='Candlestick'
    ),
    secondary_y=False,
)

colors = np.where(ohlc_df['Close'] >= ohlc_df['Open'], 'green', 'red')
fig.add_trace(
    go.Bar(
        x=ohlc_df.index,
        y=ohlc_df['Volume'],
        marker_color=colors,
        name='Volume'
    ),
    secondary_y=True,
)

# Update layout and axes titles
fig.update_layout(title='Candlestick Chart with Volume on Secondary Axis')
fig.update_yaxes(title_text='Price', secondary_y=False)
fig.update_yaxes(title_text='Volume', secondary_y=True)

fig.show()
