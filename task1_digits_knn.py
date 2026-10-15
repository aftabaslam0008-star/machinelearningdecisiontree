"""
Lab 06 - Graded Lab Task 1
Classification of Handwritten Digits (0 to 9) using K-Nearest Neighbors (KNN)
Reference: Lab Manual Page 71
Student: M. Aftab Aslam
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print("=" * 70)
print("  LAB 06 - GRADED TASK 1: DIGITS CLASSIFICATION & K-TUNING (KNN)  ")
print("=" * 70)

# 1. Load Digits Dataset
digits = load_digits()
X = digits.data
y = digits.target
target_names = [str(i) for i in digits.target_names]

print(f"\n[+] Digits Dataset Loaded:")
print(f"    Total Samples:     {X.shape[0]}")
print(f"    Features per sample: {X.shape[1]} (8x8 image pixels)")
print(f"    Classes (Digits):  {target_names}")

# 2. Train / Test Split (80% train, 20% test, stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print(f"\n[+] Data Split:")
print(f"    Training samples:  {len(X_train)}")
print(f"    Testing samples:   {len(X_test)}")

# 3. Hyperparameter Tuning for K (Manual Search & GridSearchCV)
print("\n[+] Evaluating K neighbors from 1 to 20...")
k_values = list(range(1, 21))
train_scores = []
test_scores = []
cv_scores = []

for k in k_values:
    knn_temp = KNeighborsClassifier(n_neighbors=k)
    knn_temp.fit(X_train, y_train)
    train_scores.append(knn_temp.score(X_train, y_train))
    test_scores.append(knn_temp.score(X_test, y_test))
    cv_score = cross_val_score(knn_temp, X_train, y_train, cv=5).mean()
    cv_scores.append(cv_score)

# GridSearchCV for thorough tuning
param_grid = {
    'n_neighbors': list(range(1, 16)),
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan']
}
grid_search = GridSearchCV(
    KNeighborsClassifier(),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

best_k = grid_search.best_params_['n_neighbors']
best_params = grid_search.best_params_
print(f"\n[+] GridSearchCV Best Parameters: {best_params}")
print(f"    Best Cross-Validation Accuracy: {grid_search.best_score_ * 100:.2f}%")

# 4. Train Best Model and Predict on Test Data
best_knn = grid_search.best_estimator_
y_pred = best_knn.predict(X_test)
test_acc = accuracy_score(y_test, y_pred)

print(f"\n[+] Final Test Accuracy with Best Model (K={best_k}): {test_acc * 100:.2f}%")

# 5. Confusion Matrix & Classification Report
cm = confusion_matrix(y_test, y_pred)
cr = classification_report(y_test, y_pred, target_names=target_names)
cr_dict = classification_report(y_test, y_pred, target_names=target_names, output_dict=True)

print("\n--- Confusion Matrix ---")
print(cm)

print("\n--- Classification Report ---")
print(cr)

# 6. Visualization & Plotting (Comprehensive 4-Panel Figure)
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle(
    f"Lab 06 Graded Task 1: Handwritten Digits Classification (Optimal K={best_k}, Test Acc={test_acc*100:.2f}%)",
    fontsize=14,
    fontweight='bold',
    y=0.98
)

# Plot 1: Hyperparameter Tuning (Accuracy vs K Value)
axes[0, 0].plot(k_values, cv_scores, marker='o', color='#2563eb', linewidth=2, label='5-Fold CV Score')
axes[0, 0].plot(k_values, test_scores, marker='s', color='#16a34a', linestyle='--', linewidth=2, label='Test Accuracy')
axes[0, 0].axvline(x=best_k, color='#dc2626', linestyle=':', linewidth=2, label=f'Optimal K = {best_k}')
axes[0, 0].set_title("Hyperparameter Tuning: Accuracy vs K Neighbors", fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel("Value of K (Number of Neighbors)", fontsize=11)
axes[0, 0].set_ylabel("Accuracy Score", fontsize=11)
axes[0, 0].set_xticks(k_values)
axes[0, 0].grid(True, linestyle='--', alpha=0.5)
axes[0, 0].legend(loc='best')

# Plot 2: Confusion Matrix Heatmap
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=target_names,
    yticklabels=target_names,
    ax=axes[0, 1],
    cbar=True
)
axes[0, 1].set_title(f"Confusion Matrix (Test Accuracy: {test_acc*100:.2f}%)", fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel("Predicted Digit", fontsize=11)
axes[0, 1].set_ylabel("True Digit", fontsize=11)

# Plot 3: Precision, Recall, and F1-Score per Digit
digits_list = [str(i) for i in range(10)]
precisions = [cr_dict[d]['precision'] * 100 for d in digits_list]
recalls = [cr_dict[d]['recall'] * 100 for d in digits_list]
f1_scores = [cr_dict[d]['f1-score'] * 100 for d in digits_list]

x_indices = np.arange(len(digits_list))
bar_width = 0.25

axes[1, 0].bar(x_indices - bar_width, precisions, width=bar_width, label='Precision', color='#3b82f6')
axes[1, 0].bar(x_indices, recalls, width=bar_width, label='Recall', color='#10b981')
axes[1, 0].bar(x_indices + bar_width, f1_scores, width=bar_width, label='F1-Score', color='#8b5cf6')
axes[1, 0].set_title("Per-Digit Classification Metrics (%)", fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel("Digit Class", fontsize=11)
axes[1, 0].set_ylabel("Score (%)", fontsize=11)
axes[1, 0].set_xticks(x_indices)
axes[1, 0].set_xticklabels(digits_list)
axes[1, 0].set_ylim([85, 102])
axes[1, 0].grid(True, axis='y', linestyle='--', alpha=0.5)
axes[1, 0].legend(loc='lower right')

# Plot 4: Sample Predictions Display (Digits visualization)
test_images = digits.images[len(X_train):len(X_train) + 12]
test_actual = y_test[:12]
test_pred = y_pred[:12]

# Create a mini grid inside axes[1, 1]
axes[1, 1].axis('off')
subgrid = axes[1, 1].inset_axes([0.05, 0.05, 0.9, 0.9])
subgrid.axis('off')

for i in range(12):
    row, col = divmod(i, 4)
    img_ax = subgrid.inset_axes([col * 0.25, (2 - row) * 0.33, 0.22, 0.28])
    # reshape original 64-feature vector back to 8x8
    img = X_test[i].reshape(8, 8)
    img_ax.imshow(img, cmap='gray_r', interpolation='nearest')
    actual = test_actual[i]
    pred = test_pred[i]
    status_color = 'green' if actual == pred else 'red'
    img_ax.set_title(f"T:{actual} P:{pred}", color=status_color, fontsize=9, fontweight='bold')
    img_ax.set_xticks([])
    img_ax.set_yticks([])

axes[1, 1].set_title("Sample Test Digits (T: True Label, P: Predicted Label)", fontsize=12, fontweight='bold')

plt.tight_layout()
output_img = "task1_digits_results.png"
plt.savefig(output_img, dpi=200, bbox_inches='tight')
plt.close()
print(f"\n[+] Visualization saved successfully as '{output_img}'")
print("=" * 70)
