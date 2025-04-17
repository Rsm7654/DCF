import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

def show_chart(stock_name):
    st.subheader(f"📈 Stock Price Chart - {stock_name}")
    
    # Fetch stock data
    ticker = yf.Ticker(stock_name)
    hist = ticker.history(period="1mo")

    # Create figure
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist["Close"],
        mode='lines',
        name='Close Price',
        line=dict(color='green', width=2)
    ))

    # Customize layout
    fig.update_layout(
        title=f"{stock_name} - 1 Month Performance",
        xaxis_title='Date',
        yaxis_title='Price (INR)',
        showlegend=False,
        height=500,
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='lightgrey'),
    )

    st.plotly_chart(fig, use_container_width=True)
