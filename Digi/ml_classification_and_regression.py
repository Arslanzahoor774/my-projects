"""
This script performs both classification and regression tasks.

1. SMS Spam Classification:
   - Loads and preprocesses an SMS spam dataset.
   - Uses two classifiers: K-Nearest Neighbors (via scikit-learn) and a custom Decision Tree implementation.
   - Evaluates both models using accuracy, precision, and recall.

2. Student Performance Regression:
   - Loads student performance data.
   - Trains a simple linear regression model to predict math scores from reading scores.
   - Evaluates the regression model using MAE and RMSE.

Required CSV files:
- spam.csv
- StudentsPerformance.csv
"""


                                                  #############CODE#############

import numpy as np
import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier  # Used scikit-learn's faster KNN

# -------------------------
# --- Classification: SMS Spam Detection ---
# -------------------------

# ✅ Load and preprocess the SMS Spam dataset
try:
    df_cls = pd.read_csv('spam.csv', encoding='latin-1')[['v1', 'v2']]
    print("✅ Loaded spam.csv successfully")
except FileNotFoundError:
    print("❌ spam.csv not found! Make sure the file is in the same folder.")
    exit()

df_cls.columns = ['label', 'message']
df_cls['label'] = df_cls['label'].map({'ham': 0, 'spam': 1})

# Convert text to numerical features
vectorizer = CountVectorizer()
X_cls = vectorizer.fit_transform(df_cls['message']).toarray()
y_cls = df_cls['label'].values

# Train/test split
X_cls_train, X_cls_test, y_cls_train, y_cls_test = train_test_split(X_cls, y_cls, test_size=0.25, random_state=42)

# ✅ KNN Classification (scikit-learn)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_cls_train, y_cls_train)
y_pred_knn = knn.predict(X_cls_test)

# ✅ Decision Tree (custom implementation)
def gini_index(groups, classes):
    n_instances = float(sum([len(group) for group in groups]))
    gini = 0.0
    for group in groups:
        size = float(len(group))
        if size == 0:
            continue
        score = 0.0
        for class_val in classes:
            proportion = [row[-1] for row in group].count(class_val) / size
            score += proportion ** 2
        gini += (1.0 - score) * (size / n_instances)
    return gini

def test_split(index, value, dataset):
    left, right = [], []
    for row in dataset:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right

def get_split(dataset):
    class_values = list(set(row[-1] for row in dataset))
    b_index, b_value, b_score, b_groups = 999, 999, 999, None
    for index in range(len(dataset[0]) - 1):
        for row in dataset:
            groups = test_split(index, row[index], dataset)
            gini = gini_index(groups, class_values)
            if gini < b_score:
                b_index, b_value, b_score, b_groups = index, row[index], gini, groups
    return {'index': b_index, 'value': b_value, 'groups': b_groups}

def to_terminal(group):
    outcomes = [row[-1] for row in group]
    return max(set(outcomes), key=outcomes.count)

def split(node, max_depth, min_size, depth):
    left, right = node['groups']
    del(node['groups'])
    if not left or not right:
        node['left'] = node['right'] = to_terminal(left + right)
        return
    if depth >= max_depth:
        node['left'] = to_terminal(left)
        node['right'] = to_terminal(right)
        return
    if len(left) <= min_size:
        node['left'] = to_terminal(left)
    else:
        node['left'] = get_split(left)
        split(node['left'], max_depth, min_size, depth + 1)
    if len(right) <= min_size:
        node['right'] = to_terminal(right)
    else:
        node['right'] = get_split(right)
        split(node['right'], max_depth, min_size, depth + 1)

def build_tree(train, max_depth, min_size):
    root = get_split(train)
    split(root, max_depth, min_size, 1)
    return root

def predict(node, row):
    if row[node['index']] < node['value']:
        return predict(node['left'], row) if isinstance(node['left'], dict) else node['left']
    else:
        return predict(node['right'], row) if isinstance(node['right'], dict) else node['right']

# Prepare data for decision tree
train_data = [list(X_cls_train[i]) + [y_cls_train[i]] for i in range(len(X_cls_train))]
test_data = [list(X_cls_test[i]) + [y_cls_test[i]] for i in range(len(X_cls_test))]

# Train decision tree
tree = build_tree(train_data, max_depth=5, min_size=10)
y_pred_tree = [predict(tree, row[:-1]) for row in test_data]

# Evaluation metrics
def evaluate_classification(y_true, y_pred):
    tp = sum((y_true[i] == 1 and y_pred[i] == 1) for i in range(len(y_true)))
    tn = sum((y_true[i] == 0 and y_pred[i] == 0) for i in range(len(y_true)))
    fp = sum((y_true[i] == 0 and y_pred[i] == 1) for i in range(len(y_true)))
    fn = sum((y_true[i] == 1 and y_pred[i] == 0) for i in range(len(y_true)))
    accuracy = (tp + tn) / len(y_true)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    return accuracy, precision, recall

knn_metrics = evaluate_classification(y_cls_test, y_pred_knn)
tree_metrics = evaluate_classification(y_cls_test, y_pred_tree)

print("\n--- Classification Results: SMS Spam Detection ---")
print(f"KNN Evaluation:")
print(f"  Accuracy : {knn_metrics[0]:.2f}")
print(f"  Precision: {knn_metrics[1]:.2f}")
print(f"  Recall   : {knn_metrics[2]:.2f}\n")

print(f"Decision Tree Evaluation:")
print(f"  Accuracy : {tree_metrics[0]:.2f}")
print(f"  Precision: {tree_metrics[1]:.2f}")
print(f"  Recall   : {tree_metrics[2]:.2f}")

# -------------------------
# --- Regression: Student Performance ---
# -------------------------

# ✅ Load and validate regression dataset
try:
    df_reg = pd.read_csv('StudentsPerformance.csv')
    print("✅ Loaded StudentsPerformance.csv successfully")
except FileNotFoundError:
    print("❌ StudentsPerformance.csv not found!")
    exit()

# Simple linear regression: predict math score from reading score
X_reg = df_reg[['reading score']].values
y_reg = df_reg['math score'].values

X_reg_train, X_reg_test, y_reg_train, y_reg_test = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

def add_intercept(X):
    return np.c_[np.ones(X.shape[0]), X]

X_reg_train_b = add_intercept(X_reg_train)
X_reg_test_b = add_intercept(X_reg_test)

def fit_linear_regression(X, y):
    return np.linalg.inv(X.T @ X) @ X.T @ y

def predict_linear(X, theta):
    return X @ theta

theta = fit_linear_regression(X_reg_train_b, y_reg_train)
y_pred_reg = predict_linear(X_reg_test_b, theta)

def mean_absolute_error(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def root_mean_squared_error(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

mae = mean_absolute_error(y_reg_test, y_pred_reg)
rmse = root_mean_squared_error(y_reg_test, y_pred_reg)

print("\n--- Regression Results: Student Performance ---")
print(f"  Mean Absolute Error (MAE)      : {mae:.2f}")
print(f"  Root Mean Squared Error (RMSE) : {rmse:.2f}")
