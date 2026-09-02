import numpy as np
import matplotlib.pyplot as plt
import joblib
from tensorflow.keras.models import load_model


# ==========================================
# 1. LOAD DATA
# ==========================================

data = np.load("./Data/Train_test_data.npz")

X_test = data["X_test"]
y_test = data["y_test"]
test_companies = data["test_companies"]


# ==========================================
# 2. LOAD LSTM MODEL
# ==========================================

model = load_model(
    "./models/LSTM_stock_model.keras"
)


# ==========================================
# 3. LOAD COMPANY SCALERS
# ==========================================

company_scalers = joblib.load(
    "./models/company_scalers.pkl"
)


# ==========================================
# 4. PREDICT
# ==========================================

pred_scaled = model.predict(
    X_test,
    verbose=0
)


# ==========================================
# 5. CONVERT PREDICTIONS TO REAL PRICES
# ==========================================

pred = np.zeros_like(pred_scaled)

actual = np.zeros_like(y_test)

for i, company in enumerate(test_companies):

    scaler = company_scalers[company]

    # Prediction
    dummy_pred = np.zeros((1, 5))
    dummy_pred[0, :4] = pred_scaled[i]

    pred[i] = scaler.inverse_transform(
        dummy_pred
    )[0, :4]

    # Actual value
    dummy_actual = np.zeros((1, 5))
    dummy_actual[0, :4] = y_test[i]

    actual[i] = scaler.inverse_transform(
        dummy_actual
    )[0, :4]


# ==========================================
# 6. FIRST 150 TEST SAMPLES
# ==========================================

samples = 150

actual_close = actual[:samples, 1]
predicted_close = pred[:samples, 1]


# ==========================================
# 7. GRAPH
# ==========================================

plt.figure(figsize=(12, 6))

plt.plot(
    actual_close,
    label="Actual Close"
)

plt.plot(
    predicted_close,
    label="Predicted Close"
)

plt.title(
    "LSTM - Actual vs Predicted Close Price (150 Test Samples)"
)

plt.xlabel("Test Sample")

plt.ylabel("Close Price")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.show()