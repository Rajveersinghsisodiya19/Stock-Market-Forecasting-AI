import numpy as np
from xgboost import XGBRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================================
# 1. Load data
# ==========================================

data = np.load("../Data/Train_test_data.npz")

X_train = data["X_train"]
X_test = data["X_test"]

y_train = data["y_train"]
y_test = data["y_test"]


print("Original shapes:")
print("X_train:", X_train.shape)
print("X_test :", X_test.shape)
print("y_train:", y_train.shape)
print("y_test :", y_test.shape)


# ==========================================
# 2. Flatten the sequences
# ==========================================

# (samples, 60, 5) → (samples, 300)

X_train = X_train.reshape(X_train.shape[0], -1)
X_test = X_test.reshape(X_test.shape[0], -1)


print("\nAfter reshaping:")
print("X_train:", X_train.shape)
print("X_test :", X_test.shape)


# ==========================================
# 3. Create XGBoost model
# ==========================================

xgb_model = XGBRegressor(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)


# XGBoost handles one target at a time,
# so we use MultiOutputRegressor
model = MultiOutputRegressor(xgb_model)


# ==========================================
# 4. Train
# ==========================================

print("\nTraining XGBoost...")

model.fit(X_train, y_train)

print("Training completed!")


# ==========================================
# 5. Predictions
# ==========================================

train_pred = model.predict(X_train)
test_pred = model.predict(X_test)


# ==========================================
# 6. Training performance
# ==========================================

train_mae = mean_absolute_error(y_train, train_pred)
train_mse = mean_squared_error(y_train, train_pred)
train_rmse = np.sqrt(train_mse)
train_r2 = r2_score(y_train, train_pred)


print("\n--- XGBoost Training Performance ---")
print("MAE  :", train_mae)
print("MSE  :", train_mse)
print("RMSE :", train_rmse)
print("R²   :", train_r2)


# ==========================================
# 7. Testing performance
# ==========================================

test_mae = mean_absolute_error(y_test, test_pred)
test_mse = mean_squared_error(y_test, test_pred)
test_rmse = np.sqrt(test_mse)
test_r2 = r2_score(y_test, test_pred)


print("\n--- XGBoost Testing Performance ---")
print("MAE  :", test_mae)
print("MSE  :", test_mse)
print("RMSE :", test_rmse)
print("R²   :", test_r2)


import joblib

joblib.dump(model, "../models/XGBoost_stock_model.pkl")

print("XGBoost model saved successfully!")