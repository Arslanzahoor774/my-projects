"""
Machine Learning Script: Classification and Regression

1. Classification - SMS Spam Detection:
   - Loads 'spam.csv', preprocesses text messages using CountVectorizer.
   - Applies K-Nearest Neighbors (KNN) and Decision Tree classifiers from scikit-learn.
   - Evaluates both models using accuracy, precision, and recall.

2. Regression - Student Performance:
   - Loads 'StudentsPerformance.csv' and predicts math scores from reading scores.
   - Uses scikit-learn's Linear Regression model.
   - Evaluates regression performance using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).

Dependencies:
- pandas, numpy, scikit-learn

Required files:
- spam.csv
- StudentsPerformance.csv
"""

                                                  #############CODE#############
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_recall_fscore_support

# --- Load and prepare SMS Spam dataset ---
print("✅ Spam dataset loaded:")
df_cls = pd.read_csv('spam.csv', encoding='latin-1')[['v1', 'v2']]
df_cls.columns = ['label', 'message']
df_cls['label'] = df_cls['label'].map({'ham': 0, 'spam': 1})
print(df_cls.head())

# --- Feature extraction ---
vectorizer = CountVectorizer(max_features=1000)  # Limit features for better tree performance
X_cls = vectorizer.fit_transform(df_cls['message'])
y_cls = df_cls['label'].values

X_cls_train, X_cls_test, y_cls_train, y_cls_test = train_test_split(
    X_cls, y_cls, test_size=0.25, random_state=42
)

# --- KNN Classifier ---
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_cls_train, y_cls_train)
y_pred_knn = knn.predict(X_cls_test)

# --- Decision Tree Implementation (Optimized) ---
from sklearn.tree import DecisionTreeClassifier  # Using sklearn's optimized implementation

tree = DecisionTreeClassifier(max_depth=5, min_samples_leaf=10, random_state=42)
tree.fit(X_cls_train, y_cls_train)
y_pred_tree = tree.predict(X_cls_test)

# --- Evaluation ---
def evaluate_classification(y_true, y_pred):
    accuracy = np.mean(y_true == y_pred)
    precision, recall, _, _ = precision_recall_fscore_support(
        y_true, y_pred, average='binary', zero_division=0
    )
    return accuracy, precision, recall

knn_metrics = evaluate_classification(y_cls_test, y_pred_knn)
tree_metrics = evaluate_classification(y_cls_test, y_pred_tree)

print("\n--- Classification Results (Spam Detection) ---")
print(f"KNN:      Accuracy={knn_metrics[0]:.2f}, Precision={knn_metrics[1]:.2f}, Recall={knn_metrics[2]:.2f}")
print(f"Decision: Accuracy={tree_metrics[0]:.2f}, Precision={tree_metrics[1]:.2f}, Recall={tree_metrics[2]:.2f}")

# --- Regression Task ---
print("\n✅ StudentsPerformance.csv loaded:")
df_reg = pd.read_csv('StudentsPerformance.csv')
X_reg = df_reg[['reading score']].values
y_reg = df_reg['math score'].values
print(df_reg[['reading score', 'math score']].head())

X_reg_train, X_reg_test, y_reg_train, y_reg_test = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

# --- Linear Regression ---
from sklearn.linear_model import LinearRegression

reg = LinearRegression()
reg.fit(X_reg_train, y_reg_train)
y_pred_reg = reg.predict(X_reg_test)

mae = np.mean(np.abs(y_reg_test - y_pred_reg))
rmse = np.sqrt(np.mean((y_reg_test - y_pred_reg) ** 2))

print("\n--- Regression Results (Student Scores) ---")
print(f"Mean Absolute Error:      {mae:.2f}")
print(f"Root Mean Squared Error:  {rmse:.2f}")