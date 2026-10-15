"""
Lab 06 - Graded Lab Task 2
Predicting the Age of Sea Slugs (Abalone Dataset) using K-Nearest Neighbors (KNN)
Reference: Lab Manual Page 71-72
Student: M. Aftab Aslam
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, confusion_matrix, classification_report

print("=" * 70)
print("  LAB 06 - GRADED TASK 2: ABALONE SEA SLUGS AGE PREDICTION (KNN)  ")
print("=" * 70)

# 1. Load Dataset
data_path = "abalone.data"
if not os.path.exists(data_path):
    print(f"[-] Error: '{data_path}' not found in current directory!")
    exit(1)

column_names = [
    'Sex', 'Length', 'Diameter', 'Height',
    'Whole_weight', 'Shucked_weight', 'Viscera_weight', 'Shell_weight',
    'Rings'
]

df = pd.read_csv(data_path, names=column_names)
print(f"\n[+] Abalone Dataset Loaded:")
print(f"    Total Records:     {df.shape[0]}")
print(f"    Total Columns:     {df.shape[1]}")
print(f"    Columns:           {list(df.columns)}")

# Calculate Age: in biology, Abalone Age = Rings + 1.5 years
df['Age'] = df['Rings'] + 1.5

print("\n[+] First 5 Rows of Dataset:")
print(df[['Sex', 'Length', 'Diameter', 'Height', 'Whole_weight', 'Rings', 'Age']].head())

# 2. Feature Engineering & Preprocessing
# One-hot encode the categorical 'Sex' column
df_encoded = pd.get_dummies(df, columns=['Sex'], drop_first=True, dtype=int)

# Separate features and target
X = df_encoded.drop(columns=['Rings', 'Age'])
y_age = df_encoded['Age']
y_rings = df_encoded['Rings']

feature_names = list(X.columns)
print(f"\n[+] Features prepared ({len(feature_names)} features): {feature_names}")

# 3. Train / Test Split (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_age, test_size=0.20, random_state=42
)
print(f"\n[+] Train / Test Split:")
print(f"    Training samples:  {len(X_train)}")
print(f"    Testing samples:   {len(X_test)}")

# 4. Feature Scaling (StandardScaler)
# Critical for KNN because distance metrics (Euclidean) are sensitive to feature scales!
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Hyperparameter Tuning for Optimal K (KNeighborsRegressor)
print("\n[+] Tuning K value for KNeighborsRegressor (K = 1 to 30)...")
k_range = list(range(1, 31))
rmse_uniform = []
rmse_distance = []
rmse_unscaled = []

for k in k_range:
    # Scaled with uniform weights
    knn_u = KNeighborsRegressor(n_neighbors=k, weights='uniform')
    knn_u.fit(X_train_scaled, y_train)
    pred_u = knn_u.predict(X_test_scaled)
    rmse_uniform.append(np.sqrt(mean_squared_error(y_test, pred_u)))

    # Scaled with distance weights (closer neighbors have higher influence)
    knn_d = KNeighborsRegressor(n_neighbors=k, weights='distance')
    knn_d.fit(X_train_scaled, y_train)
    pred_d = knn_d.predict(X_test_scaled)
    rmse_distance.append(np.sqrt(mean_squared_error(y_test, pred_d)))

    # Unscaled (to demonstrate the critical importance of scaling in KNN)
    knn_raw = KNeighborsRegressor(n_neighbors=k, weights='distance')
    knn_raw.fit(X_train, y_train)
    pred_raw = knn_raw.predict(X_test)
    rmse_unscaled.append(np.sqrt(mean_squared_error(y_test, pred_raw)))

best_k = k_range[np.argmin(rmse_distance)]
min_rmse = min(rmse_distance)

print(f"\n[+] Optimal Hyperparameters Found:")
print(f"    Best K:            {best_k}")
print(f"    Best Weighting:    'distance'")
print(f"    Lowest Test RMSE:  {min_rmse:.3f} years")

# 6. Final Model Evaluation
final_knn = KNeighborsRegressor(n_neighbors=best_k, weights='distance')
final_knn.fit(X_train_scaled, y_train)
y_pred = final_knn.predict(X_test_scaled)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n--- Final Model Regression Metrics ---")
print(f"Mean Squared Error (MSE):      {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f} years")
print(f"Mean Absolute Error (MAE):     {mae:.4f} years")
print(f"R² Score (Variance Explained): {r2:.4f} ({r2 * 100:.2f}%)")

# 7. Discretized Age Classification Analysis (Bonus depth)
# Age groups: Young (< 9.5 yrs), Mature (9.5 - 13.5 yrs), Old (> 13.5 yrs)
def categorize_age(age):
    if age < 9.5:
        return 'Young (<9.5)'
    elif age <= 13.5:
        return 'Mature (9.5-13.5)'
    else:
        return 'Old (>13.5)'

y_test_cat = [categorize_age(a) for a in y_test]
y_pred_cat = [categorize_age(a) for a in y_pred]
tier_labels = ['Young (<9.5)', 'Mature (9.5-13.5)', 'Old (>13.5)']
cat_cm = confusion_matrix(y_test_cat, y_pred_cat, labels=tier_labels)
cat_acc = accuracy_score(y_test_cat, y_pred_cat)

print("\n--- Age Group Tier Classification (from KNN Predictions) ---")
print(f"Tier Classification Accuracy: {cat_acc * 100:.2f}%")
print("Confusion Matrix:")
print(cat_cm)

# 8. Visualizations (Comprehensive 4-Panel Figure)
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle(
    f"Lab 06 Graded Task 2: Sea Slugs Age Prediction using KNN (Optimal K={best_k}, RMSE={rmse:.2f} yrs, R²={r2:.2f})",
    fontsize=14,
    fontweight='bold',
    y=0.98
)

# Panel 1: Hyperparameter Tuning Curve (RMSE vs K)
axes[0, 0].plot(k_range, rmse_distance, marker='o', color='#2563eb', linewidth=2, label='Scaled + Distance Weights')
axes[0, 0].plot(k_range, rmse_uniform, marker='s', color='#16a34a', linestyle='--', linewidth=2, label='Scaled + Uniform Weights')
axes[0, 0].plot(k_range, rmse_unscaled, marker='^', color='#dc2626', linestyle=':', linewidth=2, label='Unscaled (Without StandardScaler)')
axes[0, 0].axvline(x=best_k, color='#9333ea', linestyle='-.', linewidth=2, label=f'Optimal K = {best_k}')
axes[0, 0].set_title("Hyperparameter Tuning: RMSE vs K Neighbors", fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel("Value of K (Neighbors)", fontsize=11)
axes[0, 0].set_ylabel("Root Mean Squared Error (Years)", fontsize=11)
axes[0, 0].grid(True, linestyle='--', alpha=0.5)
axes[0, 0].legend(loc='best')

# Panel 2: Actual vs Predicted Age Scatter Plot
axes[0, 1].scatter(y_test, y_pred, alpha=0.4, color='#0284c7', edgecolors='none', s=40, label='Test Samples')
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())
axes[0, 1].plot([min_val, max_val], [min_val, max_val], color='#dc2626', linestyle='--', linewidth=2.5, label='Ideal 1:1 Prediction Line')
axes[0, 1].set_title(f"Actual vs Predicted Age (R² = {r2:.3f}, MAE = {mae:.2f} yrs)", fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel("Actual Age (Years = Rings + 1.5)", fontsize=11)
axes[0, 1].set_ylabel("Predicted Age (Years)", fontsize=11)
axes[0, 1].grid(True, linestyle='--', alpha=0.5)
axes[0, 1].legend(loc='upper left')

# Panel 3: Residuals Distribution (Prediction Error)
residuals = y_test - y_pred
sns.histplot(residuals, kde=True, color='#059669', ax=axes[1, 0], bins=35)
axes[1, 0].axvline(x=0, color='#dc2626', linestyle='--', linewidth=2, label='Zero Error')
axes[1, 0].set_title(f"Residuals Distribution (Mean Error: {residuals.mean():.2f}, Std: {residuals.std():.2f})", fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel("Residual (Actual Age - Predicted Age)", fontsize=11)
axes[1, 0].set_ylabel("Frequency", fontsize=11)
axes[1, 0].grid(True, linestyle='--', alpha=0.5)
axes[1, 0].legend(loc='upper right')

# Panel 4: Feature Correlation Heatmap with Target Age
corr = df.select_dtypes(include=[np.number]).corr()
sns.heatmap(
    corr[['Age', 'Rings']].sort_values(by='Age', ascending=False),
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    ax=axes[1, 1],
    cbar=True
)
axes[1, 1].set_title("Correlation of Physical Measurements with Age/Rings", fontsize=12, fontweight='bold')

plt.tight_layout()
output_img = "task2_abalone_results.png"
plt.savefig(output_img, dpi=200, bbox_inches='tight')
plt.close()
print(f"\n[+] Visualization saved successfully as '{output_img}'")
print("=" * 70)
