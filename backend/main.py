"""
FastAPI backend for stock price prediction.
Loads LSTM, Random Forest, and XGBoost models and runs iterative forecasts.
"""

from __future__ import annotations

import os
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Literal

import joblib
import numpy as np
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from tensorflow.keras.models import load_model

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
TRAINED_DIR = ROOT_DIR / "trained_models"
SCALER_PATH = ROOT_DIR / "scaler" / "company_scalers.pkl"
TEST_DATA_PATH = ROOT_DIR / "Data" / "Train_test_data.npz"

FEATURES = ["open", "close", "high", "low", "volume"]
SEQUENCE_LENGTH = 60
EVAL_SAMPLES = 150
ALLOWED_SYMBOLS = {"INFY", "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META"}
NEXT_DAY_HORIZON = 1

# Same key used in Data creation and collection/historical_data.py
TWELVE_DATA_API_KEY = os.getenv(
    "TWELVEDATA_API_KEY",
    "5e2d32211d6b4d35a4aeb7324192bc4d",
)

app = FastAPI(title="Stock Market Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lstm_model = None
rf_model = None
xgb_model = None
company_scalers: dict[str, Any] = {}
evaluation_charts_cache: dict[str, Any] | None = None


class PredictRequest(BaseModel):
    symbol: str = Field(..., examples=["AAPL"])
    horizon_days: int = Field(1, examples=[1])


class OhlcPoint(BaseModel):
    date: str
    open: float
    close: float
    high: float
    low: float


class HistoryPoint(OhlcPoint):
    volume: float


class ModelForecast(BaseModel):
    direction: Literal["Up", "Down"]
    predicted_price: float
    predictions: list[OhlcPoint]


class PredictResponse(BaseModel):
    symbol: str
    current_price: float
    horizon_days: int
    target_date: str
    history: list[HistoryPoint]
    random_forest: ModelForecast
    lstm: ModelForecast
    xgboost: ModelForecast


class SelectedPredictRequest(PredictRequest):
    model: Literal["random_forest", "xgboost", "lstm"]


class SelectedPredictResponse(BaseModel):
    symbol: str
    current_price: float
    horizon_days: int
    target_date: str
    history: list[HistoryPoint]
    model: str
    forecast: ModelForecast


class EvaluationSeries(BaseModel):
    title: str
    actual_open: list[float]
    predicted_open: list[float]
    actual_close: list[float]
    predicted_close: list[float]
    actual_high: list[float]
    predicted_high: list[float]
    actual_low: list[float]
    predicted_low: list[float]


class EvaluationChartsResponse(BaseModel):
    samples: int
    random_forest: EvaluationSeries
    xgboost: EvaluationSeries
    lstm: EvaluationSeries


def inverse_ohlc(scaler, pred4: np.ndarray) -> np.ndarray:
    dummy = np.zeros((1, 5))
    dummy[0, :4] = pred4
    return scaler.inverse_transform(dummy)[0, :4]


def inverse_ohlc_batch(
    scaled_y: np.ndarray,
    companies: np.ndarray,
    scalers: dict[str, Any],
) -> np.ndarray:
    """Same company-specific inverse scaling as test_lstm.py."""
    out = np.zeros_like(scaled_y, dtype=float)
    for i, company in enumerate(companies):
        scaler = scalers[str(company)]
        out[i] = inverse_ohlc(scaler, scaled_y[i])
    return out


def series_payload(title: str, actual: np.ndarray, predicted: np.ndarray) -> dict[str, Any]:
    return {
        "title": title,
        "actual_open": actual[:, 0].tolist(),
        "predicted_open": predicted[:, 0].tolist(),
        "actual_close": actual[:, 1].tolist(),
        "predicted_close": predicted[:, 1].tolist(),
        "actual_high": actual[:, 2].tolist(),
        "predicted_high": predicted[:, 2].tolist(),
        "actual_low": actual[:, 3].tolist(),
        "predicted_low": predicted[:, 3].tolist(),
    }


def build_evaluation_charts() -> dict[str, Any]:
    data = np.load(TEST_DATA_PATH, allow_pickle=True)
    X_test = data["X_test"][:EVAL_SAMPLES]
    y_test = data["y_test"][:EVAL_SAMPLES]
    test_companies = data["test_companies"][:EVAL_SAMPLES]

    lstm_pred_scaled = lstm_model.predict(X_test, verbose=0)
    X_flat = X_test.reshape(X_test.shape[0], -1)
    rf_pred_scaled = np.asarray(rf_model.predict(X_flat), dtype=float)
    xgb_pred_scaled = np.asarray(xgb_model.predict(X_flat), dtype=float)

    actual = inverse_ohlc_batch(y_test, test_companies, company_scalers)
    lstm_pred = inverse_ohlc_batch(lstm_pred_scaled, test_companies, company_scalers)
    rf_pred = inverse_ohlc_batch(rf_pred_scaled, test_companies, company_scalers)
    xgb_pred = inverse_ohlc_batch(xgb_pred_scaled, test_companies, company_scalers)

    return {
        "samples": EVAL_SAMPLES,
        "random_forest": series_payload(
            "Random Forest — Actual vs Predicted", actual, rf_pred
        ),
        "xgboost": series_payload("XGBoost — Actual vs Predicted", actual, xgb_pred),
        "lstm": series_payload("LSTM — Actual vs Predicted", actual, lstm_pred),
    }


def fetch_history(symbol: str) -> list[dict[str, Any]]:
    """
    Fetch daily bars via Twelve Data REST API.
    Returns last 60 completed trading days (ascending), through yesterday.
    Each row: {date, open, close, high, low, volume}
    """
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": "1day",
        "outputsize": 100,
        "order": "ASC",
        "apikey": TWELVE_DATA_API_KEY,
    }

    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Twelve Data request failed: {exc}") from exc

    if payload.get("status") == "error" or "values" not in payload:
        msg = payload.get("message") or payload.get("code") or "Unknown Twelve Data error"
        raise HTTPException(status_code=502, detail=f"Twelve Data error: {msg}")

    today = date.today()
    rows: list[dict[str, Any]] = []

    for item in payload["values"]:
        try:
            d = datetime.strptime(item["datetime"][:10], "%Y-%m-%d").date()
        except (KeyError, ValueError) as exc:
            raise HTTPException(status_code=502, detail="Invalid date in Twelve Data response") from exc

        if d >= today:
            continue

        try:
            rows.append(
                {
                    "date": d.isoformat(),
                    "open": float(item["open"]),
                    "high": float(item["high"]),
                    "low": float(item["low"]),
                    "close": float(item["close"]),
                    "volume": float(item["volume"]),
                }
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise HTTPException(
                status_code=502, detail="Incomplete OHLC/volume from Twelve Data"
            ) from exc

    rows.sort(key=lambda r: r["date"])

    if len(rows) < SEQUENCE_LENGTH:
        raise HTTPException(
            status_code=502,
            detail=f"Need at least {SEQUENCE_LENGTH} completed trading days; got {len(rows)}",
        )

    return rows[-SEQUENCE_LENGTH:]


def future_business_dates(start_after: date, n: int) -> list[date]:
    """Next n weekdays after start_after (approx. trading days)."""
    dates: list[date] = []
    cursor = start_after + timedelta(days=1)
    while len(dates) < n:
        if cursor.weekday() < 5:
            dates.append(cursor)
        cursor += timedelta(days=1)
    return dates


def iterative_predict(
    model,
    window60_scaled: np.ndarray,
    scaler,
    horizon: int,
    kind: str,
    last_real_volume: float,
    debug: bool = True,
) -> list[np.ndarray]:
    """
    Recursive multi-step forecast.

    Models see scaled windows of shape (60, 5) =
      [open, close, high, low, volume]
    and emit the next day's scaled OHLC (4 values).

    Volume is NOT predicted. Strategy: carry forward the latest REAL
    historical volume from the end of the initial 60-day window for every
    future day. Each step:

      1. Predict next-day OHLC in scaled space.
      2. Inverse-transform OHLC to price units (exactly once).
      3. Build a raw 5-feature row:
           [pred_open, pred_close, pred_high, pred_low, last_real_volume]
      4. Re-scale that full row with the company scaler.
      5. Roll the window: drop oldest day, append the new scaled row.

    Returns list of length `horizon`, each item is real-price OHLC (4,).
    """
    if window60_scaled.shape != (SEQUENCE_LENGTH, 5):
        raise ValueError(
            f"Expected window shape ({SEQUENCE_LENGTH}, 5), got {window60_scaled.shape}"
        )

    sequence = np.array(window60_scaled, dtype=float, copy=True)
    real_preds: list[np.ndarray] = []

    for day_idx in range(horizon):
        # --- 1. Predict next day from current 60-day scaled sequence ---
        if kind == "lstm":
            pred_scaled = np.asarray(
                model.predict(sequence[np.newaxis, ...], verbose=0)[0],
                dtype=float,
            ).reshape(4)
        else:
            pred_scaled = np.asarray(
                model.predict(sequence.reshape(1, -1))[0],
                dtype=float,
            ).reshape(4)

        # --- 2. Inverse-transform OHLC once (price units) ---
        pred_ohlc = inverse_ohlc(scaler, pred_scaled)  # open, close, high, low
        real_preds.append(pred_ohlc.copy())

        # --- 3. Build raw 5-feature row with carried volume ---
        future_volume = float(last_real_volume)
        new_row_raw = np.array(
            [
                float(pred_ohlc[0]),
                float(pred_ohlc[1]),
                float(pred_ohlc[2]),
                float(pred_ohlc[3]),
                future_volume,
            ],
            dtype=float,
        )

        # --- 4. Scale the full row back into model input space ---
        new_row_scaled = scaler.transform(new_row_raw.reshape(1, 5))[0]

        if debug and day_idx < 5:
            last_input_row = sequence[-1].copy()
            print(
                f"[recursive {kind}] Day {day_idx + 1}: "
                f"Open={pred_ohlc[0]:.4f} Close={pred_ohlc[1]:.4f} "
                f"High={pred_ohlc[2]:.4f} Low={pred_ohlc[3]:.4f} "
                f"FutureVolume={future_volume:.4f}"
            )
            print(f"  input sequence last row (scaled)={np.round(last_input_row, 6)}")
            print(f"  new_row_raw={np.round(new_row_raw, 6)}")
            print(f"  new_row_scaled={np.round(new_row_scaled, 6)}")

        # --- 5. Roll window: remove oldest, append predicted day ---
        sequence = np.concatenate(
            [sequence[1:], new_row_scaled.reshape(1, 5)],
            axis=0,
        )

    return real_preds


def build_model_forecast(
    model,
    kind: str,
    window_scaled: np.ndarray,
    scaler,
    horizon: int,
    future_dates: list[date],
    yesterday_open: float,
    last_real_volume: float,
) -> ModelForecast:
    real_preds = iterative_predict(
        model=model,
        window60_scaled=window_scaled,
        scaler=scaler,
        horizon=horizon,
        kind=kind,
        last_real_volume=last_real_volume,
        debug=True,
    )

    points: list[OhlcPoint] = []
    for d, ohlc in zip(future_dates, real_preds):
        points.append(
            OhlcPoint(
                date=d.isoformat(),
                open=float(ohlc[0]),
                close=float(ohlc[1]),
                high=float(ohlc[2]),
                low=float(ohlc[3]),
            )
        )

    # Sanity: multi-day forecasts should not be a single repeated constant vector.
    if horizon > 1:
        open_series = np.array([p.open for p in points], dtype=float)
        unique_opens = len(np.unique(np.round(open_series, 6)))
        print(
            f"[ok {kind}] {horizon}-day opens: unique={unique_opens}/{horizon} "
            f"std={float(np.nanstd(open_series)):.6f} "
            f"range=[{open_series.min():.4f}, {open_series.max():.4f}]"
        )
        if unique_opens == 1:
            print(
                f"[warn {kind}] all predicted opens identical — "
                "recursive window may not be updating."
            )

    target_open = points[-1].open
    direction: Literal["Up", "Down"] = "Up" if target_open > yesterday_open else "Down"

    return ModelForecast(
        direction=direction,
        predicted_price=round(target_open, 4),
        predictions=points,
    )


@app.on_event("startup")
def load_artifacts() -> None:
    global lstm_model, rf_model, xgb_model, company_scalers

    company_scalers = joblib.load(SCALER_PATH)
    lstm_model = load_model(TRAINED_DIR / "LSTM_stock_model.keras")
    rf_model = joblib.load(TRAINED_DIR / "Random_Forest_stock_model.pkl")
    xgb_model = joblib.load(TRAINED_DIR / "XGBoost_stock_model.pkl")
    print("Models and scalers loaded.")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/evaluation-charts", response_model=EvaluationChartsResponse)
def evaluation_charts() -> EvaluationChartsResponse:
    global evaluation_charts_cache
    if evaluation_charts_cache is None:
        if lstm_model is None:
            raise HTTPException(status_code=503, detail="Models are still loading")
        evaluation_charts_cache = build_evaluation_charts()
    return evaluation_charts_cache


@app.post("/api/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:
    if lstm_model is None or rf_model is None or xgb_model is None or not company_scalers:
        raise HTTPException(status_code=503, detail="Models are still loading")

    symbol = req.symbol.strip().upper()
    horizon = int(req.horizon_days)

    if symbol not in ALLOWED_SYMBOLS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported symbol. Use one of: {', '.join(sorted(ALLOWED_SYMBOLS))}",
        )
    if horizon != NEXT_DAY_HORIZON:
        raise HTTPException(
            status_code=400,
            detail="Only next-day (horizon_days=1) predictions are supported",
        )
    if symbol not in company_scalers:
        raise HTTPException(status_code=400, detail=f"No scaler found for {symbol}")

    history_rows = fetch_history(symbol)
    scaler = company_scalers[symbol]

    # Feature order must match training: open, close, high, low, volume
    raw = np.array(
        [[r["open"], r["close"], r["high"], r["low"], r["volume"]] for r in history_rows],
        dtype=float,
    )
    scaled = scaler.transform(raw)
    window = np.array(scaled[-SEQUENCE_LENGTH:], dtype=float, copy=True)
    last_real_volume = float(raw[-1, 4])

    yesterday = datetime.strptime(history_rows[-1]["date"], "%Y-%m-%d").date()
    yesterday_open = float(history_rows[-1]["open"])
    future_dates = future_business_dates(yesterday, horizon)

    history = [
        HistoryPoint(
            date=r["date"],
            open=float(r["open"]),
            close=float(r["close"]),
            high=float(r["high"]),
            low=float(r["low"]),
            volume=float(r["volume"]),
        )
        for r in history_rows
    ]

    rf_forecast = build_model_forecast(rf_model, "rf", window, scaler, horizon, future_dates, yesterday_open, last_real_volume)
    lstm_forecast = build_model_forecast(lstm_model, "lstm", window, scaler, horizon, future_dates, yesterday_open, last_real_volume)
    xgb_forecast = build_model_forecast(xgb_model, "xgb", window, scaler, horizon, future_dates, yesterday_open, last_real_volume)
    return PredictResponse(
        symbol=symbol,
        current_price=round(yesterday_open, 4),
        horizon_days=horizon,
        target_date=future_dates[-1].isoformat(),
        history=history,
        random_forest=rf_forecast,
        lstm=lstm_forecast,
        xgboost=xgb_forecast,
    )


@app.post("/api/predict-model", response_model=SelectedPredictResponse)
def predict_model(req: SelectedPredictRequest) -> SelectedPredictResponse:
    """Endpoint for a frontend model picker; /api/predict remains backward compatible."""
    if req.horizon_days != NEXT_DAY_HORIZON:
        raise HTTPException(status_code=400, detail="Only next-day (horizon_days=1) predictions are supported")
    full = predict(PredictRequest(symbol=req.symbol, horizon_days=req.horizon_days))
    forecasts = {"random_forest": full.random_forest, "xgboost": full.xgboost, "lstm": full.lstm}
    return SelectedPredictResponse(
        symbol=full.symbol, current_price=full.current_price, horizon_days=full.horizon_days,
        target_date=full.target_date, history=full.history, model=req.model, forecast=forecasts[req.model],
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
