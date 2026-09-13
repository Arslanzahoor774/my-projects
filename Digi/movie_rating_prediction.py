"""
╔══════════════════════════════════════════════════════════════╗
║       MOVIE RATING PREDICTION — FULL ML PIPELINE            ║
║       Dataset  : MovieLens Small (Simulated)                ║
║       Models   : Baseline, SVD, Matrix Factorization,       ║
║                  Random Forest Regressor                    ║
║       Metrics  : RMSE, MAE, R²                              ║
╚══════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────────
# STEP 1: IMPORTS & SETUP
# ─────────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "movie_outputs")
os.makedirs(OUT, exist_ok=True)

COLORS = ['#E74C3C','#3498DB','#2ECC71','#F39C12','#9B59B6','#1ABC9C','#E67E22']
sns.set_style("whitegrid")

print("="*65)
print("   MOVIE RATING PREDICTION PIPELINE")
print("="*65)

# ─────────────────────────────────────────────────────────────
# STEP 2: GENERATE MOVIELENS-STYLE DATASET
# ─────────────────────────────────────────────────────────────
print("\n[STEP 1] Generating MovieLens-style Dataset...")

np.random.seed(42)

# --- Movies ---
genres_list = ['Action','Comedy','Drama','Thriller','Romance',
               'Sci-Fi','Horror','Animation','Documentary','Adventure']

movie_titles = [
    "The Dark Knight","Inception","Forrest Gump","The Matrix","Interstellar",
    "Pulp Fiction","The Shawshank Redemption","Goodfellas","Fight Club","The Silence of the Lambs",
    "Schindler's List","The Godfather","Avengers: Endgame","Toy Story","Finding Nemo",
    "The Lion King","Titanic","Avatar","Jurassic Park","Star Wars",
    "Harry Potter","Lord of the Rings","The Hobbit","Iron Man","Spider-Man",
    "Batman Begins","The Joker","Parasite","Get Out","A Beautiful Mind",
    "Whiplash","La La Land","The Grand Budapest Hotel","Mad Max: Fury Road","Dunkirk",
    "1917","Bohemian Rhapsody","Rocketman","The Social Network","Moneyball",
    "The Wolf of Wall Street","Catch Me If You Can","The Departed","No Country for Old Men",
    "There Will Be Blood","Blade Runner 2049","Ex Machina","Annihilation","Arrival","Gravity"
]

n_movies = len(movie_titles)
movies_df = pd.DataFrame({
    'movieId': range(1, n_movies+1),
    'title': movie_titles,
    'genres': [np.random.choice(genres_list) for _ in range(n_movies)],
    'year': np.random.randint(1990, 2024, n_movies),
    'avg_budget_m': np.random.randint(10, 300, n_movies),
})

# Assign realistic base ratings per genre
genre_base = {'Action':3.7,'Comedy':3.4,'Drama':4.0,'Thriller':3.8,'Romance':3.3,
              'Sci-Fi':3.9,'Horror':3.2,'Animation':4.1,'Documentary':3.6,'Adventure':3.7}
movies_df['genre_base_rating'] = movies_df['genres'].map(genre_base)

# --- Users ---
n_users = 200
users_df = pd.DataFrame({
    'userId': range(1, n_users+1),
    'age_group': np.random.choice(['18-25','26-35','36-45','46+'], n_users, p=[0.3,0.35,0.2,0.15]),
    'activity': np.random.choice(['casual','regular','power'], n_users, p=[0.4,0.4,0.2]),
})

# User rating bias (some users rate high, some low)
users_df['rating_bias'] = np.random.normal(0, 0.5, n_users)

# --- Ratings ---
ratings_records = []
for _, user in users_df.iterrows():
    # Each user rates between 5-30 movies
    n_ratings = np.random.randint(5, 31)
    movie_sample = movies_df.sample(n=min(n_ratings, n_movies), replace=False)
    for _, movie in movie_sample.iterrows():
        base  = movie['genre_base_rating']
        bias  = user['rating_bias']
        noise = np.random.normal(0, 0.4)
        raw   = base + bias + noise
        rating = np.clip(round(raw * 2) / 2, 0.5, 5.0)  # round to nearest 0.5
        ratings_records.append({
            'userId':  user['userId'],
            'movieId': movie['movieId'],
            'rating':  rating,
            'title':   movie['title'],
            'genres':  movie['genres'],
            'year':    movie['year'],
        })

ratings_df = pd.DataFrame(ratings_records)
print(f"  ✔ Movies          : {n_movies}")
print(f"  ✔ Users           : {n_users}")
print(f"  ✔ Total Ratings   : {len(ratings_df)}")
print(f"  ✔ Rating Range    : {ratings_df['rating'].min()} – {ratings_df['rating'].max()}")
print(f"  ✔ Avg Rating      : {ratings_df['rating'].mean():.3f}")
print(f"  ✔ Missing Values  : {ratings_df.isnull().sum().sum()}")
print(f"\n{ratings_df.head(6).to_string(index=False)}")

# ─────────────────────────────────────────────────────────────
# STEP 3: EDA — FIGURE 1
# ─────────────────────────────────────────────────────────────
print("\n[STEP 2] Exploratory Data Analysis...")

fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle('Movie Ratings Dataset — Exploratory Data Analysis',
             fontsize=18, fontweight='bold', y=1.01)

# 1. Rating distribution
rating_counts = ratings_df['rating'].value_counts().sort_index()
axes[0,0].bar(rating_counts.index, rating_counts.values,
              color=COLORS[1], edgecolor='white', width=0.4, alpha=0.9)
axes[0,0].axvline(ratings_df['rating'].mean(), color='red', linestyle='--',
                  linewidth=2, label=f"Mean: {ratings_df['rating'].mean():.2f}")
axes[0,0].set_title('Rating Distribution', fontweight='bold', fontsize=13)
axes[0,0].set_xlabel('Rating (0.5 – 5.0)'); axes[0,0].set_ylabel('Count')
axes[0,0].legend(); axes[0,0].grid(alpha=0.3)

# 2. Ratings per user
ratings_per_user = ratings_df.groupby('userId').size()
axes[0,1].hist(ratings_per_user, bins=20, color=COLORS[0], edgecolor='white', alpha=0.9)
axes[0,1].axvline(ratings_per_user.mean(), color='navy', linestyle='--',
                  linewidth=2, label=f"Mean: {ratings_per_user.mean():.1f}")
axes[0,1].set_title('Ratings per User', fontweight='bold', fontsize=13)
axes[0,1].set_xlabel('Number of Ratings'); axes[0,1].set_ylabel('Number of Users')
axes[0,1].legend(); axes[0,1].grid(alpha=0.3)

# 3. Ratings per movie
ratings_per_movie = ratings_df.groupby('title').size().sort_values(ascending=False).head(15)
axes[0,2].barh(range(len(ratings_per_movie)), ratings_per_movie.values,
               color=COLORS[2], edgecolor='white', alpha=0.9)
axes[0,2].set_yticks(range(len(ratings_per_movie)))
axes[0,2].set_yticklabels([t[:20]+'...' if len(t)>20 else t
                            for t in ratings_per_movie.index], fontsize=8)
axes[0,2].set_title('Top 15 Most Rated Movies', fontweight='bold', fontsize=13)
axes[0,2].set_xlabel('Number of Ratings'); axes[0,2].grid(alpha=0.3)

# 4. Average rating by genre
genre_avg = ratings_df.groupby('genres')['rating'].mean().sort_values(ascending=False)
bars = axes[1,0].bar(range(len(genre_avg)), genre_avg.values,
                      color=COLORS[:len(genre_avg)], edgecolor='white', alpha=0.9)
axes[1,0].set_xticks(range(len(genre_avg)))
axes[1,0].set_xticklabels(genre_avg.index, rotation=35, ha='right', fontsize=9)
axes[1,0].set_title('Average Rating by Genre', fontweight='bold', fontsize=13)
axes[1,0].set_ylabel('Average Rating')
axes[1,0].set_ylim(0, 5.5)
for bar, val in zip(bars, genre_avg.values):
    axes[1,0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05,
                   f'{val:.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
axes[1,0].grid(alpha=0.3, axis='y')

# 5. Top 10 highest rated movies (min 5 ratings)
movie_stats = ratings_df.groupby('title')['rating'].agg(['mean','count'])
top_movies  = movie_stats[movie_stats['count']>=5].sort_values('mean',ascending=False).head(10)
axes[1,1].barh(range(len(top_movies)), top_movies['mean'].values,
               color=COLORS[4], edgecolor='white', alpha=0.9)
axes[1,1].set_yticks(range(len(top_movies)))
axes[1,1].set_yticklabels([t[:22]+'...' if len(t)>22 else t
                            for t in top_movies.index], fontsize=8)
axes[1,1].set_title('Top 10 Highest Rated Movies\n(min. 5 ratings)', fontweight='bold', fontsize=13)
axes[1,1].set_xlabel('Average Rating')
axes[1,1].set_xlim(0, 5.5)
for i, val in enumerate(top_movies['mean'].values):
    axes[1,1].text(val+0.05, i, f'{val:.2f}', va='center', fontsize=8, fontweight='bold')
axes[1,1].grid(alpha=0.3, axis='x')

# 6. Rating heatmap by genre and year bucket
ratings_df['year_bucket'] = pd.cut(ratings_df['year'],
                                    bins=[1989,1999,2009,2019,2024],
                                    labels=['1990s','2000s','2010s','2020s'])
heatmap_data = ratings_df.groupby(['genres','year_bucket'])['rating'].mean().unstack(fill_value=0)
sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='YlOrRd',
            ax=axes[1,2], linewidths=0.5, cbar_kws={'label':'Avg Rating'})
axes[1,2].set_title('Avg Rating: Genre × Era', fontweight='bold', fontsize=13)
axes[1,2].set_xlabel('Era'); axes[1,2].set_ylabel('')

plt.tight_layout()
plt.savefig(f'{OUT}/fig1_eda.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✔ EDA plot saved → fig1_eda.png")

# ─────────────────────────────────────────────────────────────
# STEP 4: PREPROCESSING & FEATURE ENGINEERING
# ─────────────────────────────────────────────────────────────
print("\n[STEP 3] Preprocessing & Feature Engineering...")

df = ratings_df.copy()

# Encode categorical features
le_genre = LabelEncoder()
le_title = LabelEncoder()
df['genre_enc']  = le_genre.fit_transform(df['genres'])
df['movie_enc']  = le_title.fit_transform(df['title'])

# User-level features
user_stats = df.groupby('userId')['rating'].agg(
    user_mean='mean', user_std='std', user_count='count'
).fillna(0).reset_index()

# Movie-level features
movie_stats_feat = df.groupby('movieId')['rating'].agg(
    movie_mean='mean', movie_std='std', movie_count='count'
).fillna(0).reset_index()

df = df.merge(user_stats,       on='userId',  how='left')
df = df.merge(movie_stats_feat, on='movieId', how='left')

# Global mean
global_mean = df['rating'].mean()
df['global_mean'] = global_mean

# Year feature
df['year_norm'] = (df['year'] - df['year'].min()) / (df['year'].max() - df['year'].min())

# Final features
FEATURES = ['userId','movieId','genre_enc','movie_enc',
            'user_mean','user_std','user_count',
            'movie_mean','movie_std','movie_count',
            'year_norm','global_mean']

X = df[FEATURES].fillna(0)
y = df['rating']

# Train / Test Split (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Scale
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

print(f"  ✔ Features engineered : {len(FEATURES)}")
print(f"  ✔ Train size          : {len(X_train)} samples")
print(f"  ✔ Test size           : {len(X_test)}  samples")
print(f"  ✔ Global mean rating  : {global_mean:.4f}")

# ─────────────────────────────────────────────────────────────
# STEP 5: COLLABORATIVE FILTERING — SVD
# ─────────────────────────────────────────────────────────────
print("\n[STEP 4] Collaborative Filtering — SVD Matrix Factorization...")

# Build user-movie matrix
user_movie_matrix = ratings_df.pivot_table(
    index='userId', columns='movieId', values='rating'
).fillna(global_mean)

# Normalize (subtract user mean)
user_means_cf = user_movie_matrix.mean(axis=1)
matrix_norm   = user_movie_matrix.sub(user_means_cf, axis=0)
sparse_matrix  = csr_matrix(matrix_norm.values)

# SVD decomposition
n_components = 15
svd = TruncatedSVD(n_components=n_components, random_state=42)
U   = svd.fit_transform(sparse_matrix)
Vt  = svd.components_

# Reconstruct predictions
matrix_pred = np.dot(U, Vt) + user_means_cf.values.reshape(-1, 1)
matrix_pred = np.clip(matrix_pred, 0.5, 5.0)

# Evaluate SVD on test set
svd_preds = []
for _, row in X_test.iterrows():
    uid = int(row['userId']) - 1
    mid = int(row['movieId']) - 1
    if uid < matrix_pred.shape[0] and mid < matrix_pred.shape[1]:
        svd_preds.append(matrix_pred[uid, mid])
    else:
        svd_preds.append(global_mean)

svd_preds  = np.array(svd_preds)
svd_rmse   = np.sqrt(mean_squared_error(y_test, svd_preds))
svd_mae    = mean_absolute_error(y_test, svd_preds)
svd_r2     = r2_score(y_test, svd_preds)
print(f"  ✔ SVD RMSE : {svd_rmse:.4f}")
print(f"  ✔ SVD MAE  : {svd_mae:.4f}")
print(f"  ✔ SVD R²   : {svd_r2:.4f}")

# ─────────────────────────────────────────────────────────────
# STEP 6: BASELINE MODEL
# ─────────────────────────────────────────────────────────────
print("\n[STEP 5] Baseline Model (Global Mean)...")

baseline_preds = np.full(len(y_test), global_mean)
base_rmse = np.sqrt(mean_squared_error(y_test, baseline_preds))
base_mae  = mean_absolute_error(y_test, baseline_preds)
base_r2   = r2_score(y_test, baseline_preds)
print(f"  ✔ Baseline RMSE : {base_rmse:.4f}")
print(f"  ✔ Baseline MAE  : {base_mae:.4f}")
print(f"  ✔ Baseline R²   : {base_r2:.4f}")

# ─────────────────────────────────────────────────────────────
# STEP 7: RIDGE REGRESSION
# ─────────────────────────────────────────────────────────────
print("\n[STEP 6] Ridge Regression...")

ridge = Ridge(alpha=1.0)
ridge.fit(X_train_sc, y_train)
ridge_preds = np.clip(ridge.predict(X_test_sc), 0.5, 5.0)
ridge_rmse  = np.sqrt(mean_squared_error(y_test, ridge_preds))
ridge_mae   = mean_absolute_error(y_test, ridge_preds)
ridge_r2    = r2_score(y_test, ridge_preds)
print(f"  ✔ Ridge RMSE : {ridge_rmse:.4f}")
print(f"  ✔ Ridge MAE  : {ridge_mae:.4f}")
print(f"  ✔ Ridge R²   : {ridge_r2:.4f}")

# ─────────────────────────────────────────────────────────────
# STEP 8: RANDOM FOREST REGRESSOR
# ─────────────────────────────────────────────────────────────
print("\n[STEP 7] Random Forest Regressor...")

rf = RandomForestRegressor(n_estimators=200, max_depth=12,
                            min_samples_split=4, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
rf_preds = np.clip(rf.predict(X_test), 0.5, 5.0)
rf_rmse  = np.sqrt(mean_squared_error(y_test, rf_preds))
rf_mae   = mean_absolute_error(y_test, rf_preds)
rf_r2    = r2_score(y_test, rf_preds)
print(f"  ✔ RF RMSE : {rf_rmse:.4f}")
print(f"  ✔ RF MAE  : {rf_mae:.4f}")
print(f"  ✔ RF R²   : {rf_r2:.4f}")

# ─────────────────────────────────────────────────────────────
# STEP 9: GRADIENT BOOSTING
# ─────────────────────────────────────────────────────────────
print("\n[STEP 8] Gradient Boosting Regressor...")

gb = GradientBoostingRegressor(n_estimators=200, max_depth=5,
                                learning_rate=0.05, random_state=42)
gb.fit(X_train, y_train)
gb_preds = np.clip(gb.predict(X_test), 0.5, 5.0)
gb_rmse  = np.sqrt(mean_squared_error(y_test, gb_preds))
gb_mae   = mean_absolute_error(y_test, gb_preds)
gb_r2    = r2_score(y_test, gb_preds)
print(f"  ✔ GB RMSE : {gb_rmse:.4f}")
print(f"  ✔ GB MAE  : {gb_mae:.4f}")
print(f"  ✔ GB R²   : {gb_r2:.4f}")

# ─────────────────────────────────────────────────────────────
# STEP 10: MODEL COMPARISON SUMMARY
# ─────────────────────────────────────────────────────────────
print("\n[STEP 9] Model Comparison...")

results = pd.DataFrame({
    'Model':  ['Baseline','SVD (CF)','Ridge Regression','Random Forest','Gradient Boosting'],
    'RMSE':   [base_rmse, svd_rmse, ridge_rmse, rf_rmse, gb_rmse],
    'MAE':    [base_mae,  svd_mae,  ridge_mae,  rf_mae,  gb_mae],
    'R2':     [base_r2,   svd_r2,   ridge_r2,   rf_r2,   gb_r2],
})
results = results.sort_values('RMSE').reset_index(drop=True)
results['Rank'] = range(1, len(results)+1)

print(f"\n  {'Rank':<5} {'Model':<22} {'RMSE':<10} {'MAE':<10} {'R²':<10}")
print("  " + "-"*57)
for _, row in results.iterrows():
    star = " ★ BEST" if row['Rank']==1 else ""
    print(f"  {int(row['Rank']):<5} {row['Model']:<22} {row['RMSE']:<10.4f} {row['MAE']:<10.4f} {row['R2']:<10.4f}{star}")

best_model_name = results.iloc[0]['Model']
best_rmse       = results.iloc[0]['RMSE']
print(f"\n  ✔ Best Model : {best_model_name} (RMSE={best_rmse:.4f})")

# ─────────────────────────────────────────────────────────────
# STEP 11: VISUALIZATIONS
# ─────────────────────────────────────────────────────────────
print("\n[STEP 10] Generating Visualizations...")

model_colors = {
    'Baseline':           '#95A5A6',
    'SVD (CF)':           '#3498DB',
    'Ridge Regression':   '#F39C12',
    'Random Forest':      '#2ECC71',
    'Gradient Boosting':  '#E74C3C',
}
bar_colors = [model_colors[m] for m in results['Model']]

# ── Figure 2: Model Comparison ───────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')

for ax, metric, label, best_is in zip(
    axes, ['RMSE','MAE','R2'],
    ['RMSE (lower is better)','MAE (lower is better)','R² Score (higher is better)'],
    ['min','min','max']
):
    vals   = results[metric]
    best_v = vals.min() if best_is=='min' else vals.max()
    cols   = ['#E74C3C' if v==best_v else '#95A5A6' for v in vals]
    bars   = ax.bar(results['Model'], vals, color=cols, edgecolor='white', linewidth=0.8)
    ax.set_title(label, fontweight='bold', fontsize=12)
    ax.set_xticklabels(results['Model'], rotation=30, ha='right', fontsize=9)
    ax.grid(alpha=0.3, axis='y')
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x()+bar.get_width()/2,
                bar.get_height() + (0.003 if best_is=='min' else 0.003),
                f'{val:.4f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{OUT}/fig2_model_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✔ Model comparison saved → fig2_model_comparison.png")

# ── Figure 3: Predicted vs Actual ────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Best Model — Predicted vs Actual Ratings', fontsize=15, fontweight='bold')

# Best model predictions
best_preds_map = {
    'Baseline':          baseline_preds,
    'SVD (CF)':          svd_preds,
    'Ridge Regression':  ridge_preds,
    'Random Forest':     rf_preds,
    'Gradient Boosting': gb_preds,
}
best_preds = best_preds_map[best_model_name]

# Scatter: predicted vs actual
axes[0].scatter(y_test, best_preds, alpha=0.4, s=25,
                color=model_colors[best_model_name], edgecolors='white', linewidth=0.3)
axes[0].plot([0.5,5],[0.5,5], 'r--', linewidth=2, label='Perfect Prediction')
axes[0].set_xlabel('Actual Rating', fontsize=11)
axes[0].set_ylabel('Predicted Rating', fontsize=11)
axes[0].set_title(f'{best_model_name}\nPredicted vs Actual', fontweight='bold')
axes[0].legend(); axes[0].grid(alpha=0.3)
axes[0].set_xlim(0,5.5); axes[0].set_ylim(0,5.5)

# Residuals distribution
residuals = y_test.values - best_preds
axes[1].hist(residuals, bins=30, color=model_colors[best_model_name],
             edgecolor='white', alpha=0.85)
axes[1].axvline(0, color='red', linestyle='--', linewidth=2, label='Zero Error')
axes[1].axvline(residuals.mean(), color='navy', linestyle='--', linewidth=2,
                label=f'Mean: {residuals.mean():.3f}')
axes[1].set_xlabel('Residual (Actual − Predicted)', fontsize=11)
axes[1].set_ylabel('Count', fontsize=11)
axes[1].set_title('Residuals Distribution', fontweight='bold')
axes[1].legend(); axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUT}/fig3_predicted_vs_actual.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✔ Predicted vs actual saved → fig3_predicted_vs_actual.png")

# ── Figure 4: Feature Importance ─────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Feature Importance & Error Analysis', fontsize=15, fontweight='bold')

# RF Feature importance
feat_imp = pd.Series(rf.feature_importances_, index=FEATURES).sort_values(ascending=True)
colors_fi = ['#E74C3C' if v == feat_imp.max() else '#3498DB' for v in feat_imp.values]
axes[0].barh(feat_imp.index, feat_imp.values, color=colors_fi, edgecolor='white')
axes[0].set_title('Random Forest — Feature Importance', fontweight='bold')
axes[0].set_xlabel('Importance Score')
axes[0].grid(alpha=0.3, axis='x')
for i, val in enumerate(feat_imp.values):
    axes[0].text(val+0.001, i, f'{val:.3f}', va='center', fontsize=8)

# Error by rating value (all models)
error_by_rating = {}
actual_vals = y_test.values
for name, preds in best_preds_map.items():
    errors_df = pd.DataFrame({'actual': actual_vals, 'pred': preds})
    errors_df['error'] = np.abs(errors_df['actual'] - errors_df['pred'])
    error_by_rating[name] = errors_df.groupby('actual')['error'].mean()

for name, errs in error_by_rating.items():
    axes[1].plot(errs.index, errs.values, 'o-', label=name,
                 color=model_colors[name], linewidth=2, markersize=5)
axes[1].set_title('Mean Absolute Error by Rating Value', fontweight='bold')
axes[1].set_xlabel('Actual Rating'); axes[1].set_ylabel('Mean Absolute Error')
axes[1].legend(fontsize=9); axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUT}/fig4_feature_importance.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✔ Feature importance saved → fig4_feature_importance.png")

# ── Figure 5: User & Movie Insights ──────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('User Behaviour & Movie Insights', fontsize=15, fontweight='bold')

# Top 10 movies by predicted rating (RF)
all_preds_rf = np.clip(rf.predict(X), 0.5, 5.0)
df['rf_pred'] = all_preds_rf
movie_pred_avg = df.groupby('title')['rf_pred'].mean().sort_values(ascending=False).head(10)
axes[0].barh(range(len(movie_pred_avg)), movie_pred_avg.values,
             color=COLORS[2], edgecolor='white', alpha=0.9)
axes[0].set_yticks(range(len(movie_pred_avg)))
axes[0].set_yticklabels([t[:22]+'...' if len(t)>22 else t
                          for t in movie_pred_avg.index], fontsize=8)
axes[0].set_title('Top 10 Movies\n(by Predicted Rating)', fontweight='bold')
axes[0].set_xlabel('Avg Predicted Rating')
axes[0].set_xlim(0, 5.5)
axes[0].grid(alpha=0.3, axis='x')

# Rating distribution comparison: actual vs predicted (best model)
axes[1].hist(y_test, bins=18, alpha=0.6, color='#3498DB', edgecolor='white', label='Actual', density=True)
axes[1].hist(best_preds, bins=18, alpha=0.6, color='#E74C3C', edgecolor='white', label='Predicted', density=True)
axes[1].set_title('Actual vs Predicted\nRating Distributions', fontweight='bold')
axes[1].set_xlabel('Rating'); axes[1].set_ylabel('Density')
axes[1].legend(); axes[1].grid(alpha=0.3)

# Genre prediction accuracy
genre_errors = df.copy()
genre_errors['pred'] = all_preds_rf
genre_errors['abs_err'] = np.abs(genre_errors['rating'] - genre_errors['pred'])
genre_err_avg = genre_errors.groupby('genres')['abs_err'].mean().sort_values()
bars = axes[2].bar(range(len(genre_err_avg)), genre_err_avg.values,
                   color=COLORS[:len(genre_err_avg)], edgecolor='white', alpha=0.9)
axes[2].set_xticks(range(len(genre_err_avg)))
axes[2].set_xticklabels(genre_err_avg.index, rotation=35, ha='right', fontsize=9)
axes[2].set_title('Prediction Error by Genre\n(lower = better)', fontweight='bold')
axes[2].set_ylabel('Mean Absolute Error')
axes[2].grid(alpha=0.3, axis='y')
for bar, val in zip(bars, genre_err_avg.values):
    axes[2].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.002,
                 f'{val:.3f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{OUT}/fig5_insights.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✔ Insights saved → fig5_insights.png")

# ── Figure 6: SVD Heatmap + Cross Validation ─────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('SVD Matrix & Cross-Validation Analysis', fontsize=15, fontweight='bold')

# SVD heatmap (sample)
sample_matrix = user_movie_matrix.iloc[:20, :20]
sns.heatmap(sample_matrix, cmap='coolwarm', ax=axes[0],
            cbar_kws={'label':'Rating'}, linewidths=0.1)
axes[0].set_title('User-Movie Rating Matrix\n(Sample: 20×20)', fontweight='bold')
axes[0].set_xlabel('Movie ID'); axes[0].set_ylabel('User ID')
axes[0].set_xticklabels(axes[0].get_xticklabels(), fontsize=7)
axes[0].set_yticklabels(axes[0].get_yticklabels(), fontsize=7)

# Cross-validation scores (RF & GB)
cv_models = {'Random Forest': rf, 'Gradient Boosting': gb}
cv_results = {}
for name, model in cv_models.items():
    scores = cross_val_score(model, X, y, cv=5,
                             scoring='neg_root_mean_squared_error', n_jobs=-1)
    cv_results[name] = -scores

positions = [1, 2]
bp = axes[1].boxplot([cv_results['Random Forest'], cv_results['Gradient Boosting']],
                      positions=positions, patch_artist=True,
                      boxprops=dict(facecolor='#3498DB', alpha=0.7),
                      medianprops=dict(color='red', linewidth=2))
for patch, color in zip(bp['boxes'], ['#2ECC71','#E74C3C']):
    patch.set_facecolor(color)
axes[1].set_xticks(positions)
axes[1].set_xticklabels(['Random Forest','Gradient Boosting'], fontsize=11)
axes[1].set_title('5-Fold Cross Validation\nRMSE Distribution', fontweight='bold')
axes[1].set_ylabel('RMSE'); axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{OUT}/fig6_svd_cv.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✔ SVD & CV saved → fig6_svd_cv.png")

# ─────────────────────────────────────────────────────────────
# STEP 12: SAVE RESULTS
# ─────────────────────────────────────────────────────────────
print("\n[STEP 11] Saving Results...")
results.to_csv(f'{OUT}/model_results.csv', index=False)
ratings_df.to_csv(f'{OUT}/processed_ratings.csv', index=False)

# ─────────────────────────────────────────────────────────────
# STEP 13: FINAL SUMMARY
# ─────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("   FINAL RESULTS SUMMARY")
print("="*65)
print(f"\n  Dataset       : {len(ratings_df)} ratings | {n_movies} movies | {n_users} users")
print(f"  Best Model    : {best_model_name}")
print(f"  Best RMSE     : {best_rmse:.4f}  (avg error of {best_rmse:.2f} stars)")
print(f"  Best MAE      : {results.iloc[0]['MAE']:.4f}")
print(f"  Best R²       : {results.iloc[0]['R2']:.4f}")

print(f"\n  {'Model':<22} {'RMSE':<10} {'MAE':<10} {'R²'}")
print("  " + "-"*52)
for _, row in results.iterrows():
    tag = " ← BEST" if row['Rank']==1 else ""
    print(f"  {row['Model']:<22} {row['RMSE']:<10.4f} {row['MAE']:<10.4f} {row['R2']:.4f}{tag}")

print(f"\n  Top Genre by Avg Rating : {genre_avg.index[0]} ({genre_avg.iloc[0]:.2f}★)")
print(f"  Most Active Users       : {ratings_per_user.idxmax()} ({ratings_per_user.max()} ratings)")
print(f"\n  All outputs saved to    : {OUT}/")
print("="*65)
print("\n  ✅ PIPELINE COMPLETE!")
