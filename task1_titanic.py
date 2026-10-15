"""
Lab 04 - Task 1
Titanic Survival Prediction using Decision Tree Classifier
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

DATA_FILE = "train.csv"

if not os.path.exists(DATA_FILE):
    print("ERROR: train.csv was not found.")
    print("Download the Titanic train.csv and place it in the same folder.")
    print("Kaggle: https://www.kaggle.com/c/titanic/data")
    raise SystemExit(1)

df = pd.read_csv(DATA_FILE)

print("\n--- Titanic Dataset ---")
print(df.head())
print("\nShape:", df.shape)

# Useful features
features = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]

# Keep only available columns
df = df[features + ["Survived"]].copy()

# Handle missing values
df["Age"] = df["Age"].fillna(df["Age"].median())
df["Fare"] = df["Fare"].fillna(df["Fare"].median())
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

# Convert categorical values to numeric
df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
df["Embarked"] = df["Embarked"].map({"S": 0, "C": 1, "Q": 2})

X = df[features]
y = df["Survived"]

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=1, stratify=y
)

# Build Decision Tree
model = DecisionTreeClassifier(
    criterion="entropy",
    max_depth=4,
    random_state=1
)

model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)

print("\n--- Results ---")
print("Accuracy:", round(accuracy, 4))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Visualize tree
plt.figure(figsize=(20, 10))
plot_tree(
    model,
    feature_names=features,
    class_names=["Not Survived", "Survived"],
    filled=True,
    rounded=True,
    fontsize=8
)
plt.title("Titanic Survival Decision Tree")
plt.tight_layout()
plt.savefig("titanic_decision_tree.png", dpi=200)
plt.show()

print("\nDecision tree saved as: titanic_decision_tree.png")
