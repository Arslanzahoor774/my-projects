"""
breast_cancer_knn_nb.py

Loads sklearn's breast cancer dataset, performs EDA, finds best K for KNN (with and without scaling),
evaluates metrics on test set, and compares the best KNN with Gaussian Naive Bayes.

Outputs:
 - best K (cross-validated)
 - classification reports, confusion matrices, and accuracy/precision/recall/F1 for models
 - a plot (saved) showing cross-val score vs k for scaled/unscaled pipelines
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report)

# ---------- 1. Load dataset ----------
data = load_breast_cancer(as_frame=True)
X = data.data
y = data.target
feature_names = data.feature_names
target_names = data.target_names

print("Dataset shape:", X.shape)
print("Target distribution:\n", pd.Series(y).value_counts())

# ---------- 2. Quick EDA ----------
print("\nFeature sample (first 5 rows):")
print(X.head())

print("\nSummary statistics:")
print(X.describe().T[['mean', 'std', 'min', 'max']])

# Optional: correlation heatmap for quick insight
plt.figure(figsize=(12, 10))
sns.heatmap(X.corr(), cmap='coolwarm', center=0, cbar_kws={'shrink': .5})
plt.title("Feature correlation matrix")
plt.tight_layout()
plt.savefig("correlation_heatmap.png", dpi=150)
plt.close()
print("Saved correlation heatmap to correlation_heatmap.png")

# ---------- 3. Train / Test split ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42
)
print("\nTrain shape:", X_train.shape, "Test shape:", X_test.shape)

# ---------- 4. Prepare pipelines ----------
pipe_scaled = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

pipe_unscaled = Pipeline([
    ('knn', KNeighborsClassifier())
])

# Grid: odd k values and weight options
param_grid = {
    'knn__n_neighbors': list(range(1, 26, 2)),  # 1,3,5,...,25
    'knn__weights': ['uniform', 'distance']
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

gs_scaled = GridSearchCV(pipe_scaled, param_grid, cv=cv, scoring='accuracy', n_jobs=-1, verbose=1)
gs_unscaled = GridSearchCV(pipe_unscaled, param_grid, cv=cv, scoring='accuracy', n_jobs=-1, verbose=1)

# ---------- 5. Run grid search (scaled vs unscaled) ----------
print("\nRunning GridSearchCV for scaled KNN ...")
gs_scaled.fit(X_train, y_train)
print("Best scaled KNN params:", gs_scaled.best_params_, "Best CV accuracy:", gs_scaled.best_score_)

print("\nRunning GridSearchCV for unscaled KNN ...")
gs_unscaled.fit(X_train, y_train)
print("Best unscaled KNN params:", gs_unscaled.best_params_, "Best CV accuracy:", gs_unscaled.best_score_)

# ---------- 6. Collect CV results and plot k vs CV accuracy ----------
def extract_cv_scores(gs_result):
    # returns dict: k -> best mean test score (averaged across weights)
    cv_results = pd.DataFrame(gs_result.cv_results_)
    # parse n_neighbors from param_k
    cv_results['n_neighbors'] = cv_results['param_knn__n_neighbors'].astype(int)
    grouped = cv_results.groupby('n_neighbors')['mean_test_score'].max()
    return grouped.sort_index()

scores_scaled = extract_cv_scores(gs_scaled)
scores_unscaled = extract_cv_scores(gs_unscaled)

plt.figure(figsize=(8,5))
plt.plot(scores_scaled.index, scores_scaled.values, marker='o', label='Scaled KNN')
plt.plot(scores_unscaled.index, scores_unscaled.values, marker='o', label='Unscaled KNN')
plt.xlabel('n_neighbors (k)')
plt.ylabel('CV Accuracy')
plt.title('CV Accuracy vs k (scaled vs unscaled)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("cv_accuracy_vs_k.png", dpi=150)
plt.close()
print("Saved plot: cv_accuracy_vs_k.png")

# ---------- 7. Evaluate best estimators on the hold-out test set ----------
def evaluate_model(name, model, X_test, y_test):
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n=== {name} ===")
    print(f"Accuracy: {acc:.4f}  Precision: {prec:.4f}  Recall: {rec:.4f}  F1: {f1:.4f}")
    print("Confusion Matrix:\n", cm)
    print("Classification Report:\n", classification_report(y_test, y_pred, target_names=target_names, zero_division=0))
    return {'acc': acc, 'prec': prec, 'rec': rec, 'f1': f1}

best_scaled = gs_scaled.best_estimator_
best_unscaled = gs_unscaled.best_estimator_

res_scaled = evaluate_model("KNN (scaled) - best", best_scaled, X_test, y_test)
res_unscaled = evaluate_model("KNN (unscaled) - best", best_unscaled, X_test, y_test)

# ---------- 8. Compare with Gaussian Naive Bayes ----------
pipe_nb = Pipeline([
    ('scaler', StandardScaler()),   # NB benefits from scaling in many cases, keep for parity
    ('nb', GaussianNB())
])
pipe_nb.fit(X_train, y_train)
res_nb = evaluate_model("Gaussian Naive Bayes", pipe_nb, X_test, y_test)

# ---------- 9. Summarize & recommend ----------
print("\n--- SUMMARY / RECOMMENDATION ---")
print(f"Best scaled KNN (CV acc): {gs_scaled.best_score_:.4f}, params: {gs_scaled.best_params_}")
print(f"Test results scaled KNN: acc={res_scaled['acc']:.4f}, f1={res_scaled['f1']:.4f}")
print(f"Best unscaled KNN (CV acc): {gs_unscaled.best_score_:.4f}, params: {gs_unscaled.best_params_}")
print(f"Test results unscaled KNN: acc={res_unscaled['acc']:.4f}, f1={res_unscaled['f1']:.4f}")
print(f"GaussianNB test f1: {res_nb['f1']:.4f}")

# Recommend model:
if res_scaled['f1'] >= max(res_unscaled['f1'], res_nb['f1']):
    recommend = ("KNN with scaling", gs_scaled.best_params_)
elif res_unscaled['f1'] >= max(res_scaled['f1'], res_nb['f1']):
    recommend = ("KNN without scaling", gs_unscaled.best_params_)
else:
    recommend = ("GaussianNB", "default")

print("\nRecommended model for deployment:", recommend)
print("\nAll done. Check the saved plots (correlation_heatmap.png, cv_accuracy_vs_k.png) and printed metrics.")
