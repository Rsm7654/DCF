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

# Streamlit user input for stock ticker
ticker_input = st.text_input("Enter stock ticker", "AAPL")
symbol_input = ticker_input.upper()

# Fetch the ticker data using yfinance
ticker = yf.Ticker(symbol_input)

# Show the chart
show_chart(ticker, symbol_input)
