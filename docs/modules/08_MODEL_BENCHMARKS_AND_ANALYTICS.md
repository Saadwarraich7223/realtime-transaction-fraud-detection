# Module 08: Model Performance & Algorithmic Governance

## 1. Quick Reference & Specifications
- **URL Route:** `/model-insights` (GET)
- **Template File:** `templates/model_insights.html`
- **Controller Function:** `model_insights()` in `app.py`
- **Data Source:** `metrics.json` and internal feature importances from `model.pkl`.
- **Primary Objective:** Provide full algorithmic transparency and evaluation metrics (Accuracy, Precision, Recall, F1-Score, ROC-AUC, Confusion Matrix, and Gini Feature Importance rankings) to defend model performance in academic and production audits.

---

## 2. Visual Layout & On-Page Elements

### A. Algorithmic Overview Header
- **Model Architecture Badge:** `Random Forest Classifier (Ensemble of 100 Estimators)`.
- **Training Dataset:** 10,000 synthetic transactions split 80% train / 20% test (stratified).
- **Class Balancing:** `class_weight='balanced'` to counter the 95:5 class imbalance ratio.

### B. The Core Evaluation Metric Cards (4 Pillars)
1. **Accuracy (98.6%):** Overall correct classifications across test set.
2. **Precision (86.0%):** Out of all transactions flagged as fraud, 86% were true fraud (low false positive rate).
3. **Recall / Sensitivity (86.0%):** Out of all actual fraud in the test set, 86% was caught (low false negative rate).
4. **F1-Score (86.0%):** The harmonic mean of Precision and Recall.
5. **ROC-AUC (0.982 / 98.2%):** Area Under the Receiver Operating Characteristic curve, demonstrating exceptional discriminatory power.

### C. The Confusion Matrix Table
- **Layout:**
  - **True Negatives (TN = 943):** Legitimate transactions correctly allowed.
  - **False Positives (FP = 7):** Legitimate transactions incorrectly flagged (0.7% False Alarm Rate).
  - **False Negatives (FN = 7):** Fraud transactions missed by the model.
  - **True Positives (TP = 43):** Fraud transactions successfully caught.

### D. Feature Importance Rankings (Gini Impurity Bar Chart)
- Ranked horizontal bar chart detailing how much each feature contributed to reducing entropy:
  1. `Location Local` (~25.55%)
  2. `Transaction Amount` (~18.80%)
  3. `24h Velocity` (~15.44%)
  4. `New Device Flag` (~14.62%)
  5. `Hour Of Day` (~8.55%)
  6. `Location Foreign` (~8.01%)
  7. `Location Domestic` (~5.46%)
  8. `Payment Methods & Client Device Types` (<2% each)

---

## 3. Underlying Technical Architecture & ML Mathematical Defense

1. **Why Random Forest over Logistic Regression or Deep Learning?**
   - **Vs. Logistic Regression:** Logistic regression assumes linear decision boundaries. Financial fraud features exhibit non-linear interactions (e.g., high amount *is safe* during day at local store, but *fraudulent* at 3 AM from a foreign IP). Random forest tree ensembles capture complex multi-feature threshold splits naturally.
   - **Vs. Deep Learning (Neural Networks):** Neural networks require massive labeled datasets (millions of rows) to avoid overfitting and operate as uninterpretable black boxes. Random Forest trains in seconds, handles tabular mixed-type data (categorical + numeric) effortlessly, and provides native feature importance extraction.

2. **Handling Class Imbalance:**
   - In raw banking data, fraud represents only 1% to 5% of volume.
   - We applied `class_weight='balanced'`, which automatically calculates tree loss penalties inversely proportional to class frequencies:
     $$w_j = \frac{n}{k \cdot n_j}$$
   - This ensures the model does not become lazy by predicting all transactions as legitimate.

---

## 4. Live Interactive Demonstration Walkthrough

1. **Step 1:** Navigate to **"Model Insights"** from the sidebar.
2. **Step 2:** Walk the reviewer or interviewer through the **4 Metric Cards**: explain that in fraud detection, **Recall** and **F1-Score** matter far more than raw accuracy.
3. **Step 3:** Point to the **Confusion Matrix**: show that False Positives (customer annoyance) are only 7 out of 950 legitimate transactions (<1%), while True Positives caught 43 out of 50 fraud cases.
4. **Step 4:** Highlight the **Feature Importance Chart**: show how `Location`, `Amount`, and `Velocity` carry over 60% of the predictive weight.

---

## 5. Architecture & Engineering Deep Dive Q&A

### Q1: "Why is F1-Score more important than Accuracy for fraud detection?"
> **Answer:** "If 95% of data is legitimate and 5% is fraud, a naive dummy model that always predicts 'Legitimate' has 95% accuracy but is completely useless. F1-score balances Precision (preventing customer harassment) and Recall (catching actual thieves), providing the true measure of fraud detection efficacy."

### Q2: "What does the ROC-AUC score of 0.982 indicate?"
> **Answer:** "ROC-AUC measures the probability that our model will rank a randomly chosen fraudulent transaction higher than a randomly chosen legitimate transaction across all possible classification thresholds. A score of 0.982 indicates near-optimal discrimination."
