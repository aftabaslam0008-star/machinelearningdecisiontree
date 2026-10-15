"""
Lab 06 - Solved Lab Activity 1
Classification of Iris flower dataset using K-Nearest Neighbors (KNN) Algorithm
Reference: Lab Manual Page 69
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print("=" * 60)
print("  LAB 06 - ACTIVITY 1: IRIS DATASET CLASSIFICATION (KNN)  ")
print("=" * 60)

# 1. Load Iris dataset
iris = datasets.load_iris()
x = iris.data
y = iris.target
target_names = iris.target_names
feature_names = iris.feature_names

print(f"\n[+] Dataset loaded successfully.")
print(f"    Total Samples: {x.shape[0]}")
print(f"    Total Features: {x.shape[1]} -> {feature_names}")
print(f"    Classes: {list(target_names)}")

# 2. Split x and y into training and testing sets (70% train, 30% test)
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=0
)
print(f"\n[+] Data Split:")
print(f"    Training samples: {len(x_train)}")
print(f"    Testing samples:  {len(x_test)}")

# 3. Train KNN Classifier with K=5 (as specified in lab manual)
classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(x_train, y_train)
print(f"\n[+] Trained KNeighborsClassifier with K=5.")

# 4. Make predictions on test data
y_pred = classifier.predict(x_test)

# 5. Evaluate Model
cm = confusion_matrix(y_test, y_pred)
acc = accuracy_score(y_test, y_pred)
cr = classification_report(y_test, y_pred, target_names=target_names)

print("\n--- Model Evaluation ---")
print(f"Accuracy: {acc * 100:.2f}%\n")
print("Confusion Matrix:")
print(cm)
print("\nClassification Report:")
print(cr)

# 6. Save visualization plots
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Confusion Matrix Heatmap
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=target_names,
    yticklabels=target_names,
    ax=axes[0],
    cbar=False
)
axes[0].set_title(f"Activity 1: Iris Confusion Matrix (Accuracy: {acc*100:.1f}%)", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Predicted Label", fontsize=11)
axes[0].set_ylabel("True Label", fontsize=11)

# Plot 2: Scatter plot of test predictions (Petal length vs Petal width)
petal_len_idx = 2
petal_wid_idx = 3
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
markers = ['o', 's', '^']

for class_idx, class_name in enumerate(target_names):
    mask = (y_test == class_idx)
    axes[1].scatter(
        x_test[mask, petal_len_idx],
        x_test[mask, petal_wid_idx],
        label=f"True {class_name}",
        alpha=0.6,
        s=80,
        c=colors[class_idx],
        marker=markers[class_idx]
    )

# Highlight misclassified points if any
misclassified = (y_test != y_pred)
if np.any(misclassified):
    axes[1].scatter(
        x_test[misclassified, petal_len_idx],
        x_test[misclassified, petal_wid_idx],
        facecolors='none',
        edgecolors='red',
        s=150,
        linewidths=2,
        label='Misclassified'
    )

axes[1].set_title("Iris Test Set: True vs Predicted", fontsize=12, fontweight='bold')
axes[1].set_xlabel(feature_names[petal_len_idx], fontsize=11)
axes[1].set_ylabel(feature_names[petal_wid_idx], fontsize=11)
axes[1].legend(loc='best')
axes[1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
output_fig = "activity1_iris_results.png"
plt.savefig(output_fig, dpi=200)
plt.close()
print(f"\n[+] Visualization successfully saved as '{output_fig}'")
print("=" * 60)
