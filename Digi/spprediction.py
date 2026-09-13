import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt

# -----------------------------
# 1️⃣ Download Historical Data
# -----------------------------
print("Downloading stock data...")

df = yf.download("AAPL", start="2015-01-01", end="2024-01-01")

print("Data downloaded successfully.\n")

# Keep only required columns
df = df[['Open', 'High', 'Low', 'Volume', 'Close']]

# -----------------------------
# 2️⃣ Create Target Variable
# -----------------------------
# Predict next day's closing price
df['Target'] = df['Close'].shift(-1)

df.dropna(inplace=True)

# Features & Target
X = df[['Open', 'High', 'Low', 'Volume']]
y = df['Target']

# -----------------------------
# 3️⃣ Scale Features
# -----------------------------
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# -----------------------------
# 4️⃣ Train-Test Split (Time Based)
# -----------------------------
split = int(len(df) * 0.8)

X_train = X_scaled[:split]
X_test = X_scaled[split:]

y_train = y[:split]
y_test = y[split:]

# -----------------------------
# 5️⃣ Train Model
# -----------------------------
model = LinearRegression()
model.fit(X_train, y_train)

print("Model trained successfully.\n")

# -----------------------------
# 6️⃣ Predictions
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# 7️⃣ Evaluation
# -----------------------------
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("Model Performance:")
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 4))

# -----------------------------
# 8️⃣ Predict Next Day Price
# -----------------------------
last_row = X_scaled[-1].reshape(1, -1)
next_day_prediction = model.predict(last_row)

print("\nPredicted Next Day Closing Price: $", round(next_day_prediction[0], 2))

# -----------------------------
# 9️⃣ Save Model & Scaler
# -----------------------------
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\n✅ Model and scaler saved successfully.")

# -----------------------------
# 🔟 Plot Actual vs Predicted
# -----------------------------
plt.figure(figsize=(10,5))
plt.plot(y_test.values, label="Actual Price")
plt.plot(y_pred, label="Predicted Price")
plt.title("Actual vs Predicted Closing Price")
plt.legend()
plt.show()