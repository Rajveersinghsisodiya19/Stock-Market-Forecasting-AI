# Stock market Prediction AI CP

## Direct 30- and 60-day forecasting

The original one-day artifacts are retained unchanged. Direct multi-horizon training is in
`models/multihorizon_pipeline.py`; it does not call or recursively roll any one-day model.

For every company, the script first splits its raw chronological OHLCV rows 80/20. It then fits
one `StandardScaler` on only that company's train rows, transforms train and test once, and builds
windows wholly inside their respective partitions. A sample contains 60 OHLCV days and its target
contains the following 30 or 60 real OHLC rows. Thus no test target row can occur in training.

With the current CSV (and its existing row ordering), the exact generated samples are:

- INFY, AAPL, MSFT, GOOGL, AMZN, and NVDA: 30-day = 3,911 train / 911 test each; 60-day = 3,881 train / 881 test each.
- TSLA: 30-day = 3,164 train / 725 test; 60-day = 3,134 train / 695 test.
- META: 30-day = 2,783 train / 629 test; 60-day = 2,753 train / 599 test.

Run all direct models (after repairing/creating the project virtual environment):

```powershell
.\venv\Scripts\python.exe models\multihorizon_pipeline.py
```

Useful targeted runs:

```powershell
.\venv\Scripts\python.exe models\multihorizon_pipeline.py --horizon 30 --models rf xgb lstm
.\venv\Scripts\python.exe models\multihorizon_pipeline.py --horizon 60 --models rf xgb lstm
```

The script prints shapes, exact per-company sample counts, and original-price test metrics overall,
per OHLC target, and at each requested forecast day. It writes:

- `Data/Multi_horizon_{30,60}_day_data.npz` and sample-count JSON files
- `trained_models/Random_Forest_{30,60}_day_model.pkl`
- `trained_models/XGBoost_{30,60}_day_model.pkl`
- `trained_models/LSTM_{30,60}_day_model.keras`
- matching train-only company scalers, metrics JSON, and held-out Close plots

The live backend and website only serve next-day (1-day) predictions from the original one-day
artifacts; the direct 30/60-day artifacts trained here are not currently wired into `POST
/api/predict` or the frontend.

