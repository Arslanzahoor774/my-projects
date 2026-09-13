"""
╔══════════════════════════════════════════════════════════════╗
║       CUSTOMER SEGMENTATION — FULL ML PIPELINE              ║
║       Dataset  : Mall Customers                             ║
║       Method   : KMeans Clustering + Elbow + Silhouette     ║
║       Output   : Segments + Business Insights + Charts      ║
╚══════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────────
# STEP 1 : IMPORTS & SETUP
# ─────────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns
import warnings, os
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# Output directory
OUT = "/home/claude/outputs"
os.makedirs(OUT, exist_ok=True)

# Color palette for segments
COLORS   = ['#E74C3C','#3498DB','#2ECC71','#F39C12','#9B59B6']
PALETTE  = dict(enumerate(COLORS))

print("="*60)
print("  CUSTOMER SEGMENTATION PIPELINE")
print("="*60)

# ─────────────────────────────────────────────────────────────
# STEP 2 : CREATE / LOAD DATASET (Mall Customers)
# ─────────────────────────────────────────────────────────────
print("\n[STEP 1] Loading Dataset...")

np.random.seed(42)
n = 200

# Simulate realistic Mall Customers dataset
data = {
    'CustomerID': range(1, n+1),
    'Gender': np.random.choice(['Male', 'Female'], n, p=[0.44, 0.56]),
    'Age': np.concatenate([
        np.random.randint(18, 35, 60),   # young
        np.random.randint(30, 50, 80),   # middle
        np.random.randint(45, 70, 60),   # senior
    ]),
    'Annual_Income_k': np.concatenate([
        np.random.randint(15, 40,  40),  # low income
        np.random.randint(40, 75,  80),  # mid income
        np.random.randint(70, 140, 80),  # high income
    ]),
    'Spending_Score': np.concatenate([
        np.random.randint(60, 100, 50),  # high spenders
        np.random.randint(40, 60,  60),  # mid spenders
        np.random.randint(1,  40,  90),  # low spenders
    ]),
}

df = pd.DataFrame(data)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"  ✔ Dataset shape   : {df.shape}")
print(f"  ✔ Features        : {list(df.columns)}")
print(f"  ✔ Missing values  : {df.isnull().sum().sum()}")
print(f"\n{df.head(8).to_string(index=False)}")

# ─────────────────────────────────────────────────────────────
# STEP 3 : EDA — FIGURE 1
# ─────────────────────────────────────────────────────────────
print("\n[STEP 2] Exploratory Data Analysis...")

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Customer Dataset — Exploratory Data Analysis',
             fontsize=18, fontweight='bold', y=1.01)

# 1. Gender distribution
gender_counts = df['Gender'].value_counts()
axes[0,0].pie(gender_counts, labels=gender_counts.index,
              autopct='%1.1f%%', colors=['#3498DB','#E74C3C'],
              startangle=90, wedgeprops={'edgecolor':'white','linewidth':2})
axes[0,0].set_title('Gender Distribution', fontweight='bold')

# 2. Age distribution
axes[0,1].hist(df['Age'], bins=20, color='#3498DB', edgecolor='white', alpha=0.85)
axes[0,1].axvline(df['Age'].mean(), color='red', linestyle='--', linewidth=2,
                  label=f"Mean: {df['Age'].mean():.1f}")
axes[0,1].set_title('Age Distribution', fontweight='bold')
axes[0,1].set_xlabel('Age'); axes[0,1].set_ylabel('Count')
axes[0,1].legend()

# 3. Annual Income distribution
axes[0,2].hist(df['Annual_Income_k'], bins=20, color='#2ECC71', edgecolor='white', alpha=0.85)
axes[0,2].axvline(df['Annual_Income_k'].mean(), color='red', linestyle='--', linewidth=2,
                  label=f"Mean: {df['Annual_Income_k'].mean():.1f}k")
axes[0,2].set_title('Annual Income Distribution', fontweight='bold')
axes[0,2].set_xlabel('Annual Income (k$)'); axes[0,2].set_ylabel('Count')
axes[0,2].legend()

# 4. Spending Score distribution
axes[1,0].hist(df['Spending_Score'], bins=20, color='#F39C12', edgecolor='white', alpha=0.85)
axes[1,0].axvline(df['Spending_Score'].mean(), color='red', linestyle='--', linewidth=2,
                  label=f"Mean: {df['Spending_Score'].mean():.1f}")
axes[1,0].set_title('Spending Score Distribution', fontweight='bold')
axes[1,0].set_xlabel('Spending Score (1-100)'); axes[1,0].set_ylabel('Count')
axes[1,0].legend()

# 5. Income vs Spending scatter
scatter = axes[1,1].scatter(df['Annual_Income_k'], df['Spending_Score'],
                             c=df['Age'], cmap='viridis', alpha=0.7, s=50, edgecolors='white')
plt.colorbar(scatter, ax=axes[1,1], label='Age')
axes[1,1].set_title('Income vs Spending Score (colored by Age)', fontweight='bold')
axes[1,1].set_xlabel('Annual Income (k$)'); axes[1,1].set_ylabel('Spending Score')

# 6. Correlation heatmap
corr = df[['Age','Annual_Income_k','Spending_Score']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
            ax=axes[1,2], square=True, linewidths=0.5,
            cbar_kws={'shrink': 0.8})
axes[1,2].set_title('Correlation Heatmap', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{OUT}/fig1_eda.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✔ EDA plot saved → fig1_eda.png")

# ─────────────────────────────────────────────────────────────
# STEP 4 : PREPROCESSING
# ─────────────────────────────────────────────────────────────
print("\n[STEP 3] Preprocessing...")

# Encode Gender
le = LabelEncoder()
df['Gender_Enc'] = le.fit_transform(df['Gender'])

# Features for clustering
features = ['Age', 'Annual_Income_k', 'Spending_Score', 'Gender_Enc']
X = df[features].copy()

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"  ✔ Features used   : {features}")
print(f"  ✔ Scaling method  : StandardScaler (mean=0, std=1)")
print(f"  ✔ Scaled shape    : {X_scaled.shape}")

# Print stats
stats = df[['Age','Annual_Income_k','Spending_Score']].describe().round(2)
print(f"\n  Descriptive Statistics:\n{stats.to_string()}")

# ─────────────────────────────────────────────────────────────
# STEP 5 : FIND OPTIMAL K — ELBOW + SILHOUETTE — FIGURE 2
# ─────────────────────────────────────────────────────────────
print("\n[STEP 4] Finding Optimal Number of Clusters...")

inertias, silhouettes = [], []
K_range = range(2, 11)

for k in K_range:
    km = KMeans(n_clusters=k, init='k-means++', n_init=20, random_state=42)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(X_scaled, labels))
    print(f"  K={k}  |  Inertia: {km.inertia_:>10.2f}  |  Silhouette: {silhouette_score(X_scaled, labels):.4f}")

# Best K by silhouette
best_k = K_range.start + np.argmax(silhouettes)
print(f"\n  ✔ Best K (Silhouette) : {best_k}")

# Plot Elbow + Silhouette
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Optimal K Selection — Elbow Method & Silhouette Score',
             fontsize=15, fontweight='bold')

# Elbow
ax1.plot(K_range, inertias, 'o-', color='#3498DB', linewidth=2.5, markersize=8)
ax1.axvline(best_k, color='red', linestyle='--', linewidth=2, label=f'Optimal K={best_k}')
ax1.fill_between(K_range, inertias, alpha=0.1, color='#3498DB')
ax1.set_title('Elbow Method', fontweight='bold', fontsize=13)
ax1.set_xlabel('Number of Clusters (K)', fontsize=11)
ax1.set_ylabel('Inertia (Within-Cluster SSE)', fontsize=11)
ax1.legend(); ax1.grid(alpha=0.3)

# Silhouette
colors_bar = ['#E74C3C' if k==best_k else '#95A5A6' for k in K_range]
bars = ax2.bar(K_range, silhouettes, color=colors_bar, edgecolor='white', linewidth=0.5)
ax2.set_title('Silhouette Score', fontweight='bold', fontsize=13)
ax2.set_xlabel('Number of Clusters (K)', fontsize=11)
ax2.set_ylabel('Silhouette Score', fontsize=11)
ax2.set_xticks(list(K_range))
for bar, val in zip(bars, silhouettes):
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.003,
             f'{val:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax2.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{OUT}/fig2_optimal_k.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✔ Optimal K plot saved → fig2_optimal_k.png")

# ─────────────────────────────────────────────────────────────
# STEP 6 : TRAIN FINAL KMEANS MODEL
# ─────────────────────────────────────────────────────────────
print(f"\n[STEP 5] Training KMeans with K={best_k}...")

kmeans = KMeans(n_clusters=best_k, init='k-means++', n_init=50,
                max_iter=500, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

final_silhouette = silhouette_score(X_scaled, df['Cluster'])
print(f"  ✔ Model trained successfully")
print(f"  ✔ Final Inertia      : {kmeans.inertia_:.2f}")
print(f"  ✔ Silhouette Score   : {final_silhouette:.4f}")

# ─────────────────────────────────────────────────────────────
# STEP 7 : CLUSTER ANALYSIS & BUSINESS INSIGHTS
# ─────────────────────────────────────────────────────────────
print("\n[STEP 6] Cluster Analysis & Business Insights...")

cluster_stats = df.groupby('Cluster').agg(
    Count=('CustomerID','count'),
    Avg_Age=('Age','mean'),
    Avg_Income=('Annual_Income_k','mean'),
    Avg_Spending=('Spending_Score','mean'),
    Male_Pct=('Gender_Enc', lambda x: (x==1).mean()*100),
    Female_Pct=('Gender_Enc', lambda x: (x==0).mean()*100),
).round(1)

print(f"\n  Cluster Summary:\n{cluster_stats.to_string()}")

# Assign business labels
def assign_label(row):
    inc, spd = row['Avg_Income'], row['Avg_Spending']
    if inc >= 75 and spd >= 60:  return "💎 Premium Buyers"
    if inc >= 75 and spd <  50:  return "🎯 High-Income Savers"
    if inc <  50 and spd >= 60:  return "🛍️  Impulsive Spenders"
    if inc <  50 and spd <  40:  return "💰 Budget Conscious"
    return                               "📊 Mainstream Segment"

cluster_stats['Segment_Label'] = cluster_stats.apply(assign_label, axis=1)
label_map = cluster_stats['Segment_Label'].to_dict()
df['Segment'] = df['Cluster'].map(label_map)

print("\n  Segment Labels Assigned:")
for c, row in cluster_stats.iterrows():
    print(f"  Cluster {c} → {row['Segment_Label']}  "
          f"(n={int(row['Count'])}, Income={row['Avg_Income']}k, Spending={row['Avg_Spending']})")

# ─────────────────────────────────────────────────────────────
# STEP 8 : VISUALIZATIONS — FIGURES 3, 4, 5
# ─────────────────────────────────────────────────────────────
print("\n[STEP 7] Generating Visualizations...")

# ── Figure 3: Main Cluster Scatter (Income vs Spending) ──────
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('KMeans Customer Segmentation Results',
             fontsize=16, fontweight='bold')

segment_colors = {label: COLORS[i] for i, label in enumerate(cluster_stats['Segment_Label'])}

# Plot 1: Income vs Spending
for cluster_id, group in df.groupby('Cluster'):
    label = label_map[cluster_id]
    axes[0].scatter(group['Annual_Income_k'], group['Spending_Score'],
                    c=COLORS[cluster_id], label=label, alpha=0.75, s=70,
                    edgecolors='white', linewidth=0.5)

# Plot centroids (inverse transform)
centroids_orig = scaler.inverse_transform(kmeans.cluster_centers_)
for i, c in enumerate(centroids_orig):
    axes[0].scatter(c[1], c[2], c='black', marker='X', s=250, zorder=5,
                    edgecolors='white', linewidth=1.5)

axes[0].set_title('Annual Income vs Spending Score', fontweight='bold', fontsize=13)
axes[0].set_xlabel('Annual Income (k$)', fontsize=11)
axes[0].set_ylabel('Spending Score (1-100)', fontsize=11)
axes[0].legend(fontsize=9, framealpha=0.9)
axes[0].grid(alpha=0.3)

# Plot 2: Age vs Spending
for cluster_id, group in df.groupby('Cluster'):
    label = label_map[cluster_id]
    axes[1].scatter(group['Age'], group['Spending_Score'],
                    c=COLORS[cluster_id], label=label, alpha=0.75, s=70,
                    edgecolors='white', linewidth=0.5)

axes[1].set_title('Age vs Spending Score', fontweight='bold', fontsize=13)
axes[1].set_xlabel('Age', fontsize=11)
axes[1].set_ylabel('Spending Score (1-100)', fontsize=11)
axes[1].legend(fontsize=9, framealpha=0.9)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUT}/fig3_clusters_scatter.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✔ Cluster scatter saved → fig3_clusters_scatter.png")

# ── Figure 4: Segment Profile Radar / Bar Charts ────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Segment Profile Analysis', fontsize=16, fontweight='bold')

labels_list = cluster_stats['Segment_Label'].tolist()
x = np.arange(len(labels_list))
w = 0.6

# Avg Age per segment
bars1 = axes[0].bar(x, cluster_stats['Avg_Age'], color=COLORS[:len(labels_list)],
                    edgecolor='white', width=w)
axes[0].set_title('Average Age by Segment', fontweight='bold')
axes[0].set_xticks(x); axes[0].set_xticklabels(labels_list, rotation=30, ha='right', fontsize=8)
axes[0].set_ylabel('Average Age')
for bar, val in zip(bars1, cluster_stats['Avg_Age']):
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                 f'{val:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
axes[0].grid(alpha=0.3, axis='y')

# Avg Income per segment
bars2 = axes[1].bar(x, cluster_stats['Avg_Income'], color=COLORS[:len(labels_list)],
                    edgecolor='white', width=w)
axes[1].set_title('Average Annual Income by Segment', fontweight='bold')
axes[1].set_xticks(x); axes[1].set_xticklabels(labels_list, rotation=30, ha='right', fontsize=8)
axes[1].set_ylabel('Average Income (k$)')
for bar, val in zip(bars2, cluster_stats['Avg_Income']):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                 f'${val:.0f}k', ha='center', va='bottom', fontweight='bold', fontsize=9)
axes[1].grid(alpha=0.3, axis='y')

# Avg Spending per segment
bars3 = axes[2].bar(x, cluster_stats['Avg_Spending'], color=COLORS[:len(labels_list)],
                    edgecolor='white', width=w)
axes[2].set_title('Average Spending Score by Segment', fontweight='bold')
axes[2].set_xticks(x); axes[2].set_xticklabels(labels_list, rotation=30, ha='right', fontsize=8)
axes[2].set_ylabel('Average Spending Score')
for bar, val in zip(bars3, cluster_stats['Avg_Spending']):
    axes[2].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                 f'{val:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
axes[2].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{OUT}/fig4_segment_profiles.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✔ Segment profiles saved → fig4_segment_profiles.png")

# ── Figure 5: PCA 2D + Gender split + Heatmap ───────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Advanced Cluster Analysis', fontsize=16, fontweight='bold')

# PCA 2D
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)
df['PCA1'] = X_pca[:,0]; df['PCA2'] = X_pca[:,1]

for cluster_id, group in df.groupby('Cluster'):
    label = label_map[cluster_id]
    axes[0].scatter(group['PCA1'], group['PCA2'], c=COLORS[cluster_id],
                    label=label, alpha=0.75, s=60, edgecolors='white', linewidth=0.5)

axes[0].set_title(f'PCA 2D Projection\n(Variance explained: {pca.explained_variance_ratio_.sum()*100:.1f}%)',
                  fontweight='bold')
axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
axes[0].legend(fontsize=8); axes[0].grid(alpha=0.3)

# Gender by segment (stacked bar)
gender_seg = df.groupby(['Segment','Gender']).size().unstack(fill_value=0)
gender_seg_pct = gender_seg.div(gender_seg.sum(axis=1), axis=0) * 100
gender_seg_pct.plot(kind='bar', ax=axes[1], color=['#E74C3C','#3498DB'],
                    edgecolor='white', stacked=True)
axes[1].set_title('Gender Distribution by Segment', fontweight='bold')
axes[1].set_xlabel(''); axes[1].set_ylabel('Percentage (%)')
axes[1].set_xticklabels(gender_seg_pct.index, rotation=30, ha='right', fontsize=8)
axes[1].legend(title='Gender', fontsize=9)
axes[1].grid(alpha=0.3, axis='y')

# Cluster heatmap (mean features)
heatmap_data = cluster_stats[['Avg_Age','Avg_Income','Avg_Spending']].copy()
heatmap_data.index = cluster_stats['Segment_Label']
heatmap_norm = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min())
sns.heatmap(heatmap_norm.T, annot=heatmap_data.T.round(1), fmt='g',
            cmap='YlOrRd', ax=axes[2], linewidths=0.5,
            xticklabels=heatmap_norm.index, yticklabels=['Avg Age','Avg Income (k$)','Avg Spending'],
            cbar_kws={'label':'Normalized Value'})
axes[2].set_title('Segment Feature Heatmap\n(annotated with actual values)', fontweight='bold')
axes[2].set_xticklabels(axes[2].get_xticklabels(), rotation=30, ha='right', fontsize=8)

plt.tight_layout()
plt.savefig(f'{OUT}/fig5_advanced_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✔ Advanced analysis saved → fig5_advanced_analysis.png")

# ── Figure 6: Customer Size Distribution ────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
fig.suptitle('Segment Size & Composition', fontsize=15, fontweight='bold')

seg_counts = cluster_stats.set_index('Segment_Label')['Count']
ax1.pie(seg_counts, labels=seg_counts.index, autopct='%1.1f%%',
        colors=COLORS[:len(seg_counts)], startangle=90,
        wedgeprops={'edgecolor':'white','linewidth':2},
        textprops={'fontsize':9})
ax1.set_title('Customer Distribution by Segment', fontweight='bold')

# Box plots
melted = df.melt(id_vars=['Segment'], value_vars=['Age','Annual_Income_k','Spending_Score'],
                 var_name='Feature', value_name='Value')
unique_segs = df['Segment'].unique()
seg_color_map = {seg: COLORS[i] for i, seg in enumerate(sorted(unique_segs))}
sns.boxplot(data=df, x='Segment', y='Spending_Score', ax=ax2,
            palette={seg: COLORS[i] for i, seg in enumerate(cluster_stats['Segment_Label'])},
            order=cluster_stats['Segment_Label'])
ax2.set_title('Spending Score Distribution by Segment', fontweight='bold')
ax2.set_xlabel('')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=30, ha='right', fontsize=8)
ax2.set_ylabel('Spending Score')
ax2.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{OUT}/fig6_size_composition.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✔ Size & composition saved → fig6_size_composition.png")

# ─────────────────────────────────────────────────────────────
# STEP 9 : SAVE RESULTS
# ─────────────────────────────────────────────────────────────
print("\n[STEP 8] Saving Results...")

df.to_csv(f'{OUT}/segmented_customers.csv', index=False)
cluster_stats.to_csv(f'{OUT}/segment_summary.csv')

# Business recommendations
recommendations = {
    "💎 Premium Buyers":      "Deploy VIP loyalty programs, exclusive events, premium product launches, and personalized concierge service.",
    "🎯 High-Income Savers":  "Target with aspirational campaigns, limited-edition offers, and value-for-money premium bundles to unlock spending.",
    "🛍️  Impulsive Spenders":  "Focus on flash sales, impulse-friendly product displays, BNPL options, and social-proof marketing.",
    "💰 Budget Conscious":    "Engage with discount programs, value packs, loyalty point accumulation, and affordable product lines.",
    "📊 Mainstream Segment":  "Use broad engagement strategies: seasonal promotions, referral programs, and cross-sell opportunities.",
}

print("\n" + "="*60)
print("  BUSINESS RECOMMENDATIONS")
print("="*60)
for seg, rec in recommendations.items():
    if seg in label_map.values():
        count = cluster_stats[cluster_stats['Segment_Label']==seg]['Count'].values
        cnt = int(count[0]) if len(count)>0 else 0
        print(f"\n  {seg}  ({cnt} customers)")
        print(f"  → {rec}")

print("\n" + "="*60)
print(f"  MODEL PERFORMANCE")
print("="*60)
print(f"  Algorithm         : KMeans (k-means++ init)")
print(f"  Optimal Clusters  : {best_k}")
print(f"  Silhouette Score  : {final_silhouette:.4f}  {'★ Excellent' if final_silhouette>0.5 else '✔ Good'}")
print(f"  Inertia           : {kmeans.inertia_:.2f}")
print(f"  Total Customers   : {len(df)}")
print(f"\n  All outputs saved to: {OUT}/")
print("="*60)
print("\n  ✅ PIPELINE COMPLETE!")
