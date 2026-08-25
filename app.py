from fastapi import FastAPI, HTTPException
from nsetools import Nse

app = FastAPI(
    title="NSE Tools Wrapper Service",
    description="Containerised REST API exposing live National Stock Exchange market matrix data.",
    version="1.2"
)

# Initialize the NSE tracking core globally
nse = Nse()

@app.get("/health")
def health_check():
    return {"status": "operational", "engine": "nsetools-fastapi"}

@app.get("/stocks/all")
def fetch_all_stocks():
    """Compiles a complete list of valid stock codes and entity listings."""
    try:
        return nse.get_stock_codes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NSE Fetch Error: {str(e)}")

@app.get("/stocks/quote/{ticker}")
def fetch_stock_quote(ticker: str):
    """Gathers comprehensive data values for a specific active stock code."""
    try:
        quote = nse.get_quote(ticker.lower())
        if not quote:
            raise HTTPException(status_code=404, detail=f"Ticker '{ticker}' not found or invalid.")
        return quote
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NSE Pipeline Error: {str(e)}")

@app.get("/market/gainers")
def fetch_top_gainers():
    """Lists current session's top market gainers."""
    try:
        return nse.get_top_gainers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market/losers")
def fetch_top_losers():
    """Lists current session's top market losers."""
    try:
        return nse.get_top_losers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
