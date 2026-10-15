"""
Lab 06 - Solved Lab Activity 2
Breast Cancer Classification using K-Nearest Neighbors (KNN) Algorithm
Reference: Lab Manual Page 70-71
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

print("=" * 60)
print("  LAB 06 - ACTIVITY 2: BREAST CANCER CLASSIFICATION (KNN)   ")
print("=" * 60)

# 1. Load Breast Cancer dataset
breast_cancer = load_breast_cancer()
X_full = pd.DataFrame(breast_cancer.data, columns=breast_cancer.feature_names)

print(f"\n[+] Dataset loaded successfully.")
print(f"    Total Samples:  {X_full.shape[0]}")
print(f"    Total Features: {X_full.shape[1]}")
print(f"    Target classes: {list(breast_cancer.target_names)}")

# 2. Select the subset of features specified in the manual: ['mean area', 'mean compactness']
features_selected = ['mean area', 'mean compactness']
X = X_full[features_selected].copy()

# 3. Target encoding: malignant = 0, benign = 1
y_cat = pd.Categorical.from_codes(breast_cancer.target, breast_cancer.target_names)
y = pd.get_dummies(y_cat, drop_first=True, dtype=int)
# Rename dummy column to 'benign' (1: benign, 0: malignant)
y.columns = ['benign']

print(f"\n[+] Selected Features for modeling: {features_selected}")
print(f"    Target variable: 'benign' (1 = Benign, 0 = Malignant)")
print(X.head())

# 4. Split dataset into train and test sets (default 25% test size, random_state=1 as per lab manual)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

print(f"\n[+] Data Split:")
print(f"    Training samples: {len(X_train)}")
print(f"    Testing samples:  {len(X_test)}")

# 5. Build and train KNN model with K=5, metric='euclidean'
knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn.fit(X_train, y_train.values.ravel())
print(f"\n[+] Trained KNeighborsClassifier(n_neighbors=5, metric='euclidean')")

# 6. Make predictions on test set
y_pred = knn.predict(X_test)

# 7. Evaluate model performance
cm = confusion_matrix(y_test['benign'], y_pred)
acc = accuracy_score(y_test['benign'], y_pred)
correct_count = cm.diagonal().sum()
total_count = len(y_test)

print("\n--- Model Evaluation ---")
print(f"Confusion Matrix:")
print(cm)
print(f"\nModel Accuracy: {correct_count}/{total_count} = {acc * 100:.2f}%")
print(f"(Expected from lab manual: 121/143 = 84.6%)")
print("\nClassification Report:")
print(classification_report(y_test['benign'], y_pred, target_names=['Malignant (0)', 'Benign (1)']))

# 8. Visualizations (Matching and extending the lab manual's plots)
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot 1: True Labels Scatter Plot
test_df = X_test.copy()
test_df['benign'] = y_test['benign'].values
sns.scatterplot(
    x='mean area',
    y='mean compactness',
    hue='benign',
    palette={0: 'red', 1: 'green'},
    style='benign',
    data=test_df,
    ax=axes[0],
    s=70,
    alpha=0.85
)
axes[0].set_title("Ground Truth (Test Set)", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Mean Area", fontsize=11)
axes[0].set_ylabel("Mean Compactness", fontsize=11)
axes[0].legend(title='Condition', labels=['Benign (1)', 'Malignant (0)'])
axes[0].grid(True, linestyle='--', alpha=0.4)

# Plot 2: KNN Predicted Labels Scatter Plot
scatter = axes[1].scatter(
    X_test['mean area'],
    X_test['mean compactness'],
    c=y_pred,
    cmap='coolwarm',
    alpha=0.75,
    s=70,
    edgecolors='k',
    linewidths=0.5
)
axes[1].set_title(f"KNN Predicted Labels (K=5)\nAccuracy = {acc*100:.1f}%", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Mean Area", fontsize=11)
axes[1].set_ylabel("Mean Compactness", fontsize=11)
cbar = plt.colorbar(scatter, ax=axes[1], ticks=[0, 1])
cbar.ax.set_yticklabels(['Malignant (0)', 'Benign (1)'])
axes[1].grid(True, linestyle='--', alpha=0.4)

# Plot 3: Confusion Matrix Heatmap
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=['Pred Malignant', 'Pred Benign'],
    yticklabels=['True Malignant', 'True Benign'],
    ax=axes[2],
    cbar=False
)
axes[2].set_title(f"Confusion Matrix ({correct_count}/{total_count} Correct)", fontsize=12, fontweight='bold')
axes[2].set_xlabel("Predicted Label", fontsize=11)
axes[2].set_ylabel("True Label", fontsize=11)

plt.tight_layout()
output_fig = "activity2_breast_cancer_knn.png"
plt.savefig(output_fig, dpi=200)
plt.close()
print(f"\n[+] Visualization successfully saved as '{output_fig}'")
print("=" * 60)
