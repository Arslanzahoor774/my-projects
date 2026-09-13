import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('D:\Model\Sample dataset Australian Vehicle Price Assessment 2  2023 T3.csv')

# Data Preprocessing
# For simplicity, assuming all relevant columns are numerical
X = data.drop('Price', axis=1)
y = data['Price']

# Splitting Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Choose a Regression Model
reg_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Training the Model
reg_model.fit(X_train, y_train)

# Prediction
y_pred = reg_model.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Visualization
plt.scatter(y_test, y_pred)
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.title('Actual Prices vs Predicted Prices')
plt.show()
