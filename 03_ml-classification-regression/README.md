# 📊 ML Classification & Regression — Built From Scratch

A complete machine learning project implementing both classification and regression algorithms **from scratch using NumPy** — without relying on sklearn's built-in model implementations.

## 🎯 Two Tasks in One Project

### Task 1 — SMS Spam Classification
Detects whether an SMS message is spam or legitimate (ham).

**Models implemented:**
- ✅ K-Nearest Neighbors (KNN) — via scikit-learn
- ✅ Decision Tree — **custom implementation from scratch** using Gini Index

### Task 2 — Student Performance Regression
Predicts a student's math score from their reading score.

**Model implemented:**
- ✅ Linear Regression — **built from scratch** using NumPy matrix operations (Normal Equation)

## 📁 Project Files
| File | Description |
|------|-------------|
| `ml_classification_and_regression.py` | Complete ML pipeline for both tasks |
| `spam.csv` | SMS spam dataset (5,572 messages) |
| `StudentsPerformance.csv` | Student exam scores dataset |

## 🛠️ Tech Stack
- Python 3.x
- NumPy
- Pandas
- Scikit-learn (for KNN and vectorization only)

## ⚙️ How to Run

### 1. Install dependencies
```bash
pip install numpy pandas scikit-learn
```

### 2. Run the pipeline
```bash
python ml_classification_and_regression.py
```

## 📊 Output

## 🎯 Key Concepts Demonstrated
- Classification vs Regression
- Decision Tree implementation from scratch (Gini Index splitting)
- Linear Regression via Normal Equation (no sklearn)
- Custom evaluation metrics (Accuracy, Precision, Recall, MAE, RMSE)
- Text vectorization with CountVectorizer
- Train/test splitting and model evaluation
