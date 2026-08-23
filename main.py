from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/get_options/{ticker}")
def get_options_data(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        exp_dates = stock.options
        if not exp_dates:
            return {"error": "No options available"}
            
        next_friday = exp_dates[0]
        opt_chain = stock.option_chain(next_friday)
        
        top_calls = opt_chain.calls.sort_values(by='openInterest', ascending=False).head(2)
        top_puts = opt_chain.puts.sort_values(by='openInterest', ascending=False).head(2)
        
        return {
            "status": "success",
            "ticker": ticker.upper(),
            "c1_p": float(top_calls.iloc[0]['strike']),
            "c1_oi": int(top_calls.iloc[0]['openInterest']),
            "c2_p": float(top_calls.iloc[1]['strike']),
            "c2_oi": int(top_calls.iloc[1]['openInterest']),
            "p1_p": float(top_puts.iloc[0]['strike']),
            "p1_oi": int(top_puts.iloc[0]['openInterest']),
            "p2_p": float(top_puts.iloc[1]['strike']),
            "p2_oi": int(top_puts.iloc[1]['openInterest']),
        }
    except Exception as e:
        return {"error": str(e)}
