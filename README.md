# Lab 04 — Decision Tree

## Objective
Implement Decision Tree Classification for:
1. Titanic Survival Prediction
2. Car Safety Prediction

## Requirements
- Python 3.9+
- pandas
- scikit-learn
- matplotlib
- seaborn

Install:
```bash
pip install -r requirements.txt
```

## Task 1 — Titanic
File: `task1_titanic.py`

The program:
- loads Titanic data
- selects useful features
- handles missing values
- converts categorical data to numeric values
- splits data into training/testing sets
- trains a Decision Tree Classifier
- calculates accuracy
- prints a classification report
- saves the decision tree visualization as `titanic_decision_tree.png`

### Dataset
Place `train.csv` from the Kaggle Titanic dataset in this folder.

Expected file:
`train.csv`

The official Kaggle competition page is:
https://www.kaggle.com/c/titanic/data

## Task 2 — Car Evaluation
File: `task2_car_safety.py`

The program:
- downloads the UCI Car Evaluation dataset automatically
- assigns column names
- converts categorical values to numbers
- splits the data
- trains a Decision Tree Classifier
- calculates accuracy
- prints a classification report
- saves the tree as `car_decision_tree.png`

If automatic download does not work, download `car.data` from:
https://archive.ics.uci.edu/dataset/19/car+evaluation

## Run
Task 1:
```bash
python task1_titanic.py
```

Task 2:
```bash
python task2_car_safety.py
```

## Important Concepts
- Root Node: top node of the tree.
- Decision Node: node used to make a decision/split.
- Leaf Node: final prediction node.
- Gini Index: measures impurity.
- Entropy: measures uncertainty.
- Information Gain: reduction in entropy after splitting.
- Overfitting: when the tree memorizes training data.
- Pre-pruning: limiting tree growth, e.g. `max_depth=4`.

## Note
Accuracy can change slightly depending on the dataset version and train/test split.
