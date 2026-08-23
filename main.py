from fastapi import FastAPI, Request
import yfinance as yf

app = FastAPI()

@app.get("/")
def home():
    return {"status": "DHM88 Server is Active & Running!"}

@app.get("/get_options/{ticker}")
def get_options(ticker: str):
    try:
        stock = yf.Ticker(ticker.upper())
        exp_dates = stock.options
        if not exp_dates:
            return {"error": "No options found for this ticker"}
            
        next_friday = exp_dates[0]
        opt_chain = stock.option_chain(next_friday)
        
        calls = opt_chain.calls.sort_values(by='openInterest', ascending=False).head(2)
        puts = opt_chain.puts.sort_values(by='openInterest', ascending=False).head(2)
        
        return {
            "ticker": ticker.upper(),
            "expiration": next_friday,
            "c1_p": float(calls.iloc[0]['strike']), "c1_oi": int(calls.iloc[0]['openInterest']),
            "c2_p": float(calls.iloc[1]['strike']), "c2_oi": int(calls.iloc[1]['openInterest']),
            "p1_p": float(puts.iloc[0]['strike']), "p1_oi": int(puts.iloc[0]['openInterest']),
            "p2_p": float(puts.iloc[1]['strike']), "p2_oi": int(puts.iloc[1]['openInterest'])
        }
    except Exception as e:
        return {"error": str(e)}

# مسار استقبال الـ Webhook من TradingView
@app.post("/webhook")
async def tradingview_webhook(request: Request):
    try:
        data = await request.json()
        print("📢 تم استقبال تنبيه من TradingView:", data)
        # يمكنك هنا إضافة أي كود إضافي لمعالجة البيانات الواردة من الشارت
        return {"status": "success", "message": "Webhook received successfully", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
