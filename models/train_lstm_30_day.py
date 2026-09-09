import numpy as np
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    LSTM,
    Dense,
    Dropout,
    RepeatVector,
    TimeDistributed,
    LayerNormalization
)
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau,
    ModelCheckpoint
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ============================================================
# SETTINGS
# ============================================================

DATA_PATH = "../Data/Train_test_30_day_data.npz"
MODEL_PATH = "../trained_models/LSTM_30_day_model.keras"

SEQUENCE_LENGTH = 60
FORECAST_HORIZON = 30
FEATURES = 4


# ============================================================
# LOAD DATA
# ============================================================

print("Loading dataset...")

data = np.load(DATA_PATH)

X_train = data["X_train"]
y_train = data["y_train"]

X_test = data["X_test"]
y_test = data["y_test"]

train_companies = data["train_companies"]
test_companies = data["test_companies"]


print("\nDataset:")
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)

print("X_test :", X_test.shape)
print("y_test :", y_test.shape)


# ============================================================
# CHECK DATA
# ============================================================

if X_train.ndim != 3:
    raise ValueError("X_train must have shape (samples, 60, 4)")

if y_train.ndim != 3:
    raise ValueError("y_train must have shape (samples, 30, 4)")

if X_train.shape[1] != SEQUENCE_LENGTH:
    raise ValueError("Input sequence length must be 60")

if X_train.shape[2] != FEATURES:
    raise ValueError("Number of input features must be 4")

if y_train.shape[1] != FORECAST_HORIZON:
    raise ValueError("Forecast horizon must be 30")

if y_train.shape[2] != FEATURES:
    raise ValueError("Number of output features must be 4")


# ============================================================
# CREATE VALIDATION DATA
#
# Take the LAST 20% of each company's TRAINING sequences.
#
# This is better than validation_split=0.2 because the dataset
# contains multiple companies.
# ============================================================

print("\nCreating validation set...")

X_train_final = []
y_train_final = []

X_val = []
y_val = []

companies = np.unique(train_companies)

for company in companies:

    indices = np.where(train_companies == company)[0]

    company_X = X_train[indices]
    company_y = y_train[indices]

    split = int(len(company_X) * 0.80)

    if split == 0:
        continue

    company_train_X = company_X[:split]
    company_train_y = company_y[:split]

    company_val_X = company_X[split:]
    company_val_y = company_y[split:]

    X_train_final.append(company_train_X)
    y_train_final.append(company_train_y)

    X_val.append(company_val_X)
    y_val.append(company_val_y)

    print(
        f"{company}: "
        f"train={len(company_train_X)}, "
        f"validation={len(company_val_X)}"
    )


X_train_final = np.concatenate(X_train_final, axis=0)
y_train_final = np.concatenate(y_train_final, axis=0)

X_val = np.concatenate(X_val, axis=0)
y_val = np.concatenate(y_val, axis=0)


print("\nFinal training data:")
print("X_train:", X_train_final.shape)
print("y_train:", y_train_final.shape)

print("\nValidation data:")
print("X_val:", X_val.shape)
print("y_val:", y_val.shape)


# ============================================================
# BUILD MODEL
# ============================================================

print("\nBuilding LSTM model...")


model = Sequential([

    # ========================================================
    # ENCODER
    # ========================================================

    LSTM(
        128,
        return_sequences=True,
        input_shape=(SEQUENCE_LENGTH, FEATURES),
        kernel_regularizer=l2(0.0001)
    ),

    LayerNormalization(),

    Dropout(0.20),


    LSTM(
        64,
        return_sequences=False,
        kernel_regularizer=l2(0.0001)
    ),

    LayerNormalization(),

    Dropout(0.20),


    # ========================================================
    # CONVERT ENCODED INFORMATION INTO 30 FUTURE STEPS
    # ========================================================

    RepeatVector(FORECAST_HORIZON),


    # ========================================================
    # DECODER
    # ========================================================

    LSTM(
        64,
        return_sequences=True,
        kernel_regularizer=l2(0.0001)
    ),

    LayerNormalization(),

    Dropout(0.15),


    LSTM(
        32,
        return_sequences=True,
        kernel_regularizer=l2(0.0001)
    ),

    LayerNormalization(),

    Dropout(0.10),


    # ========================================================
    # OUTPUT
    #
    # 30 timesteps × 4 values
    #
    # Open
    # High
    # Low
    # Close
    # ========================================================

    TimeDistributed(
        Dense(
            FEATURES,
            activation="linear"
        )
    )
])


# ============================================================
# COMPILE
# ============================================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="mse",
    metrics=["mae"]
)


# ============================================================
# MODEL SUMMARY
# ============================================================

model.summary()


# ============================================================
# CALLBACKS
# ============================================================

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=10,
    restore_best_weights=True,
    verbose=1
)


reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=4,
    min_lr=1e-6,
    verbose=1
)


checkpoint = ModelCheckpoint(
    MODEL_PATH,
    monitor="val_loss",
    save_best_only=True,
    verbose=1
)


# ============================================================
# TRAIN
# ============================================================

print("\nStarting training...")

history = model.fit(

    X_train_final,
    y_train_final,

    validation_data=(
        X_val,
        y_val
    ),

    epochs=100,

    batch_size=64,

    shuffle=True,

    callbacks=[
        early_stopping,
        reduce_lr,
        checkpoint
    ],

    verbose=1
)


# ============================================================
# LOAD BEST MODEL
# ============================================================

model = tf.keras.models.load_model(
    MODEL_PATH
)


# ============================================================
# TEST PREDICTION
# ============================================================

print("\nMaking predictions on test data...")

predictions = model.predict(
    X_test,
    batch_size=64,
    verbose=1
)


print("\nPrediction shape:")
print(predictions.shape)


# ============================================================
# OVERALL METRICS
# ============================================================

y_true_flat = y_test.reshape(-1)
y_pred_flat = predictions.reshape(-1)


mae = mean_absolute_error(
    y_true_flat,
    y_pred_flat
)

mse = mean_squared_error(
    y_true_flat,
    y_pred_flat
)

rmse = np.sqrt(mse)

r2 = r2_score(
    y_true_flat,
    y_pred_flat
)


print("\n")
print("=" * 60)
print("30-DAY LSTM TEST RESULTS")
print("=" * 60)

print(f"MAE  : {mae:.6f}")
print(f"MSE  : {mse:.6f}")
print(f"RMSE : {rmse:.6f}")
print(f"R²   : {r2:.6f}")


# ============================================================
# METRICS FOR EACH FEATURE
# ============================================================

feature_names = [
    "Open",
    "High",
    "Low",
    "Close"
]


print("\n")
print("=" * 60)
print("METRICS BY FEATURE")
print("=" * 60)


for feature_index, feature_name in enumerate(feature_names):

    actual = y_test[:, :, feature_index].reshape(-1)
    predicted = predictions[:, :, feature_index].reshape(-1)

    feature_mae = mean_absolute_error(
        actual,
        predicted
    )

    feature_mse = mean_squared_error(
        actual,
        predicted
    )

    feature_rmse = np.sqrt(feature_mse)

    feature_r2 = r2_score(
        actual,
        predicted
    )

    print(f"\n{feature_name}")

    print(f"MAE  : {feature_mae:.6f}")
    print(f"MSE  : {feature_mse:.6f}")
    print(f"RMSE : {feature_rmse:.6f}")
    print(f"R²   : {feature_r2:.6f}")


# ============================================================
# METRICS BY FORECAST DAY
# ============================================================

print("\n")
print("=" * 60)
print("METRICS BY FORECAST HORIZON")
print("=" * 60)


for day in range(FORECAST_HORIZON):

    actual = y_test[:, day, :].reshape(-1)
    predicted = predictions[:, day, :].reshape(-1)

    day_mae = mean_absolute_error(
        actual,
        predicted
    )

    day_mse = mean_squared_error(
        actual,
        predicted
    )

    day_rmse = np.sqrt(day_mse)

    day_r2 = r2_score(
        actual,
        predicted
    )

    print(
        f"Day {day + 1:02d} | "
        f"MAE: {day_mae:.6f} | "
        f"RMSE: {day_rmse:.6f} | "
        f"R²: {day_r2:.6f}"
    )


print("\n")
print("=" * 60)
print("MODEL SAVED")
print("=" * 60)

print(MODEL_PATH)