"""
Lab 04 - Task 2
Car Safety Prediction using Decision Tree Classifier
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

DATA_FILE = "car.data"
URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/car/car.data"

columns = [
    "buying", "maint", "doors", "persons",
    "lug_boot", "safety", "class"
]

# Download dataset if it is not already present
if not os.path.exists(DATA_FILE):
    print("Downloading Car Evaluation dataset...")
    try:
        df = pd.read_csv(URL, header=None, names=columns)
        df.to_csv(DATA_FILE, index=False, header=False)
    except Exception as e:
        print("Automatic download failed:", e)
        print("Download car.data manually from:")
        print("https://archive.ics.uci.edu/dataset/19/car+evaluation")
        raise SystemExit(1)
else:
    df = pd.read_csv(DATA_FILE, header=None, names=columns)

print("\n--- Car Evaluation Dataset ---")
print(df.head())
print("\nShape:", df.shape)

# Encode categorical columns
encoded = df.copy()
encoders = {}

for column in encoded.columns:
    encoder = LabelEncoder()
    encoded[column] = encoder.fit_transform(encoded[column])
    encoders[column] = encoder

X = encoded.drop("class", axis=1)
y = encoded["class"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=1, stratify=y
)

# Build Decision Tree
model = DecisionTreeClassifier(
    criterion="entropy",
    max_depth=5,
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
plt.figure(figsize=(24, 12))
plot_tree(
    model,
    feature_names=X.columns,
    class_names=encoders["class"].classes_,
    filled=True,
    rounded=True,
    fontsize=7
)
plt.title("Car Safety Decision Tree")
plt.tight_layout()
plt.savefig("car_decision_tree.png", dpi=200)
plt.show()

print("\nDecision tree saved as: car_decision_tree.png")
