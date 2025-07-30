def peer_comparison(ticker_symbol, df_stocks):
    ticker = yf.Ticker(ticker_symbol)
    sector = ticker.info.get("sector", None)

    if not sector:
        st.warning("⚠️ Could not retrieve sector information from the ticker.")
        return

    st.write(f"🔍 Sector identified: **{sector}**")

    # Find peers in the same sector using `df_stocks`
    df_stocks["Ticker"] = df_stocks["Ticker"].str.strip()
    peer_tickers = []

    for symbol in df_stocks["Ticker"]:
        try:
            peer_info = yf.Ticker(symbol).info
            if peer_info.get("sector", "") == sector:
                peer_tickers.append({
                    "Ticker": symbol,
                    "Company": df_stocks[df_stocks["Ticker"] == symbol]["Company"].values[0],
                    "Sector": sector,
                    "Market Cap": peer_info.get("marketCap", None),
                    "PE Ratio": peer_info.get("trailingPE", None),
                    "Price": peer_info.get("currentPrice", None)
                })
        except:
            continue

    if peer_tickers:
        df_peers = pd.DataFrame(peer_tickers)
        st.dataframe(df_peers.set_index("Ticker"))
    else:
        st.info("No peers found in the same sector.")
