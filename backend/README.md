# Stock Market Prediction — Backend

## Run

From the project root, using the existing venv:

```bash
.\venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Or from this folder:

```bash
cd backend
..\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Optional: set `TWELVEDATA_API_KEY` in the environment (defaults to the same key used in historical data collection).

## Endpoint

`POST /api/predict`

```json
{ "symbol": "AAPL", "horizon_days": 1 }
```

Allowed symbols: INFY, AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META
Only next-day prediction is supported (`horizon_days` must be `1`).

For each symbol, the backend fetches the latest 60 completed trading days of OHLC data from
Twelve Data, applies the company-specific scaler used at training time, and runs each of the
Random Forest, XGBoost, and LSTM one-day models to predict the next trading day's Open, Close,
High, and Low (Volume is not predicted).

To request only one model for a frontend model picker, use `POST /api/predict-model`:

```json
{ "symbol": "AAPL", "horizon_days": 1, "model": "lstm" }
```
