import streamlit as st
import yfinance as yf

# Set page config at the top of the script
st.set_page_config(page_title="📈 Stock Analyzer", layout="wide")

def show_chart(ticker, symbol):
    st.subheader(f"📈 Stock Price Chart - {symbol}")
    
    try:
        # Fetch historical data for the past 5 years
        hist = ticker.history(period="5y")
        
        # Round the closing prices to 2 decimal places
        hist["Close"] = hist["Close"].round(2)
        
        # Display the chart
        st.line_chart(hist["Close"])
    
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")

