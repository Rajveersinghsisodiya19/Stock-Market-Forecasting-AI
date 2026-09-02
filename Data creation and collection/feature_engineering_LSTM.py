import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("../Data/historical_data.csv")

df = df.drop_duplicates()

features = ["open", "close", "high", "low", "volume"]

sequence_length = 60


# ============================================================
# 2. STORAGE
# ============================================================

X_train = []
X_test = []

y_train = []
y_test = []

train_companies = []
test_companies = []

company_scalers = {}


# ============================================================
# 3. PROCESS EACH COMPANY SEPARATELY
# ============================================================

for company in df["company"].unique():

    print("\nProcessing:", company)

    company_data = df[df["company"] == company].copy()

    values = company_data[features].values.astype(float)

    # --------------------------------------------------------
    # Split RAW data
    # --------------------------------------------------------

    split = int(len(values) * 0.8)

    train_values = values[:split]
    test_values = values[split:]

    print("Total days :", len(values))
    print("Train days :", len(train_values))
    print("Test days  :", len(test_values))

    # --------------------------------------------------------
    # IMPORTANT:
    # Create scaler for THIS company only
    # Fit ONLY on training data
    # --------------------------------------------------------

    scaler = StandardScaler()

    scaler.fit(train_values)

    company_scalers[company] = scaler

    # Scale train and test using company's train scaler

    train_scaled = scaler.transform(train_values)

    test_scaled = scaler.transform(test_values)

    # --------------------------------------------------------
    # CREATE TRAIN SEQUENCES
    # --------------------------------------------------------

    for i in range(sequence_length, len(train_scaled)):

        X_train.append(
            train_scaled[i-sequence_length:i]
        )

        y_train.append(
            train_scaled[i, 0:4]
        )

        train_companies.append(company)

    # --------------------------------------------------------
    # CREATE TEST SEQUENCES
    # --------------------------------------------------------
    # IMPORTANT:
    # Test sequences use ONLY test data.
    # Therefore there is ZERO train/test row overlap.
    # --------------------------------------------------------

    for i in range(sequence_length, len(test_scaled)):

        X_test.append(
            test_scaled[i-sequence_length:i]
        )

        y_test.append(
            test_scaled[i, 0:4]
        )

        test_companies.append(company)


# ============================================================
# 4. CONVERT TO NUMPY
# ============================================================

X_train = np.array(X_train)
X_test = np.array(X_test)

y_train = np.array(y_train)
y_test = np.array(y_test)

train_companies = np.array(train_companies)
test_companies = np.array(test_companies)


print("\n======================================")
print("FINAL DATA")
print("======================================")

print("X_train:", X_train.shape)
print("X_test :", X_test.shape)
print("y_train:", y_train.shape)
print("y_test :", y_test.shape)

print("Train companies:", train_companies.shape)
print("Test companies :", test_companies.shape)


# ============================================================
# 5. SAVE COMPANY SCALERS
# ============================================================

joblib.dump(
    company_scalers,
    "../models/company_scalers.pkl"
)

print("\nCompany scalers saved!")


# ============================================================
# 6. SAVE DATA
# ============================================================

np.savez_compressed(

    "../Data/Train_test_data.npz",

    X_train=X_train,
    X_test=X_test,

    y_train=y_train,
    y_test=y_test,

    train_companies=train_companies,
    test_companies=test_companies
)

print("Train_test_data.npz saved successfully!")