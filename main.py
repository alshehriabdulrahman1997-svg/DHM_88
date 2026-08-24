from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/")
def home():
    return {"status": "DHM88 Server is Active & Running!"}

# مسار لجلب التواريخ المتاحة للسهم
@app.get("/dates/{ticker}")
def get_dates(ticker: str):
    try:
        stock = yf.Ticker(ticker.upper())
        return {"ticker": ticker.upper(), "available_dates": stock.options}
    except Exception as e:
        return {"error": str(e)}

# مسار لجلب العقود لتاريخ محدد (أو أقرب تاريخ إذا ما حددت تاريخ)
@app.get("/get_options/{ticker}")
def get_options(ticker: str, date: str = None):
    try:
        stock = yf.Ticker(ticker.upper())
        exp_dates = stock.options
        if not exp_dates:
            return {"error": "No options found"}
            
        # إذا ما أرسلت تاريخ، ياخذ أول (أقرب) تاريخ
        selected_date = date if date in exp_dates else exp_dates[0]
        
        opt_chain = stock.option_chain(selected_date)
        calls = opt_chain.calls.sort_values(by='openInterest', ascending=False).head(2)
        puts = opt_chain.puts.sort_values(by='openInterest', ascending=False).head(2)
        
        return {
            "ticker": ticker.upper(),
            "expiration": selected_date,
            "c1_p": float(calls.iloc[0]['strike']), "c1_oi": int(calls.iloc[0]['openInterest']),
            "c2_p": float(calls.iloc[1]['strike']), "c2_oi": int(calls.iloc[1]['openInterest']),
            "p1_p": float(puts.iloc[0]['strike']), "p1_oi": int(puts.iloc[0]['openInterest']),
            "p2_p": float(puts.iloc[1]['strike']), "p2_oi": int(puts.iloc[1]['openInterest'])
        }
    except Exception as e:
        return {"error": str(e)}
