import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

df= pd.read_csv("historical_data.csv")

# check for null values
print(df.isnull().sum())
# remove duplicates
df = df.drop_duplicates()


features = ["open","close","high","low","volume"]



X = []
Y = []

sequence_length = 60

for company in df["company"].unique():

    company_data = df[df["company"] == company]

    values = company_data[features].values

    for i in range(sequence_length, len(values)):

        # Previous 60 days
        X.append(values[i-sequence_length:i])

        # Next day's OPEN, HIGH, LOW, CLOSE
        Y.append(values[i, 0:4])


x=np.array(X)
y=np.array(Y)


X_train, X_test, y_train, y_test = train_test_split(
    x,
    y,
    train_size=0.8,
    shuffle=False
)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


#normailization 
scaler = StandardScaler()

#reshape for normalization
num_samples, sequence_length, num_features = X_train.shape
X_train_2d = X_train.reshape(-1,num_features)

scaler.fit(X_train_2d)

X_train = scaler.transform(X_train_2d).reshape(
    num_samples,
    sequence_length,
    num_features
)

X_test = scaler.transform(
    X_test.reshape(-1, num_features)
).reshape(
    X_test.shape[0],
    sequence_length,
    num_features
)


np.savez_compressed("Train_test_data.npz",X_train=X_train,X_test=X_test,y_train=y_train,y_test=y_test)
