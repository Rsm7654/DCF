import streamlit as st
import pandas as pd
import yfinance as yf

def fetch_sector(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        if info is None:
            st.error(f"Failed to fetch data for {ticker_symbol}. It might be an invalid ticker.")
            return None
        
        # Check if 'sector' exists in the fetched info
        sector = info.get('sector', None)
        if sector is None:
            st.warning(f"Sector information not available for {ticker_symbol}")
        return sector
    except Exception as e:
        st.error(f"Error fetching sector for {ticker_symbol}: {e}")
        return None

