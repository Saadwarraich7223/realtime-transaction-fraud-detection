"""
Train the fraud detection model.

Steps (as described in SDD Chapter 6 - Algorithm & Implementation):
1. Load dataset
2. Preprocess: encode categorical variables, scale numeric features
3. Split 80/20 train/test
4. Train Random Forest classifier
5. Evaluate: accuracy, precision, recall, F1-score, confusion matrix
6. Save the trained pipeline to model.pkl
"""
import json
import joblib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report,
                             ConfusionMatrixDisplay)

CATEGORICAL = ["location", "device_type", "payment_method"]
NUMERIC = ["amount", "hour", "txn_last_24h", "is_new_device"]

# 1. Load dataset
df = pd.read_csv("transactions.csv")
X = df[CATEGORICAL + NUMERIC]
y = df["is_fraud"]

# 2-3. Preprocessing pipeline + train/test split (80/20)
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ("num", StandardScaler(), NUMERIC),
])
model = Pipeline([
    ("preprocess", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")),
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# 4. Train
model.fit(X_train, y_train)

# 5. Evaluate
y_pred = model.predict(X_test)
metrics = {
    "accuracy": round(accuracy_score(y_test, y_pred), 4),
    "precision": round(precision_score(y_test, y_pred), 4),
    "recall": round(recall_score(y_test, y_pred), 4),
    "f1_score": round(f1_score(y_test, y_pred), 4),
    "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
}
print(classification_report(y_test, y_pred, target_names=["Legitimate", "Fraud"]))
print("Metrics:", metrics)

with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred, display_labels=["Legitimate", "Fraud"], cmap="Blues")
plt.title("Confusion Matrix - Random Forest")
plt.savefig("confusion_matrix.png", dpi=120, bbox_inches="tight")

# 6. Save model
joblib.dump(model, "model.pkl")
print("Saved model.pkl, metrics.json, confusion_matrix.png")
