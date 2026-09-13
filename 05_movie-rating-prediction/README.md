# 🎬 Movie Rating Prediction — Internship Project

A machine learning system that predicts movie ratings and provides recommendations using collaborative filtering and SVD (Singular Value Decomposition), built during my internship at **Arch Technologies**.

## 💡 Problem Statement
Predicting how a user will rate a movie they haven't seen yet — the core problem behind recommendation systems used by Netflix, Amazon, and YouTube.

## 🧠 Approach
- **Multiple models compared:** Linear Regression, Random Forest, SVD
- **Best performer:** SVD with cross-validation
- **Evaluation:** MAE, RMSE across all models
- **Output:** Interactive dashboard with visual comparisons

## 📁 Project Files
| File | Description |
|------|-------------|
| `movie_rating_prediction.py` | Complete ML pipeline — data processing, model training, evaluation |
| `movie_dashboard.html` | Interactive results dashboard with charts |

## 🛠️ Tech Stack
- Python 3.x
- Scikit-learn
- Pandas, NumPy
- Matplotlib, Plotly
- SVD (Singular Value Decomposition)
- HTML/CSS (interactive dashboard)

## ⚙️ How to Run

### 1. Install dependencies
```bash
pip install scikit-learn pandas numpy matplotlib plotly
```

### 2. Run prediction pipeline
```bash
python movie_rating_prediction.py
```

### 3. View dashboard
Open `movie_dashboard.html` in any browser.

## 📊 Model Comparison Output
| Model | MAE | RMSE |
|-------|-----|------|
| Linear Regression | 0.89 | 1.12 |
| Random Forest | 0.76 | 0.98 |
| SVD | 0.71 | 0.91 |

## 🎯 Key Concepts Demonstrated
- Recommendation system fundamentals
- Collaborative filtering
- Matrix factorization with SVD
- Multi-model comparison and selection
- Cross-validation
- Interactive results visualization

## 🏢 Context
Built as part of my internship at **Arch Technologies** (Module 2, Task 4).
