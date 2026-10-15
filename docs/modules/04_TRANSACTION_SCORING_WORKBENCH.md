# Module 04: Single Transaction Analysis & Risk Evaluation

## 1. Quick Reference & Specifications
- **URL Route:** `/analyze` (GET, POST)
- **Template File:** `templates/analyze.html`
- **Controller Function:** `analyze()` in `app.py`
- **Primary Objective:** Provide fraud investigation officers with an interactive manual inspection workbench to input suspect transaction parameters and receive instantaneous inference, confidence calibration, and database audit recording.

---

## 2. Visual Layout & On-Page Elements

### A. Quick Pre-Fill Scenario Bench (Top)
- **"Legitimate Retail Purchase" Preset Button:** 1-clicks realistic safe inputs (PKR 45.00, 2:00 PM, Local, Debit Card, 1 txn/24h, Known Device).
- **"Card-Not-Present Fraud Spike" Preset Button:** 1-clicks high-risk anomaly inputs (PKR 9,500.00, 3:00 AM, Foreign, Credit Card, 12 txns/24h, Unrecognized Device).
- Allows effortless live demonstration without manual typing during technical demonstration.

### B. The 7-Feature Vector Input Form
1. **Transaction Amount (`amount`):** Float value in PKR. Validated strictly $> 0$.
2. **Transaction Hour (`hour`):** 0 to 23 (24-hour military clock).
3. **Geographical Location (`location`):** Dropdown (`local`, `domestic`, `foreign`).
4. **Device Client Type (`device_type`):** Dropdown (`mobile`, `desktop`, `tablet`).
5. **Payment Instrument (`payment_method`):** Dropdown (`credit_card`, `debit_card`, `wallet`).
6. **Rolling 24-Hour Velocity (`txn_last_24h`):** Integer count of transaction attempts by user within 24 hours. Validated $\ge 0$.
7. **New Hardware Fingerprint (`is_new_device`):** Boolean toggle (0 = Known Authenticated Hardware, 1 = Unrecognized New Device).

### C. Real-Time Inference Results Card (Post-Evaluation)
- **Decision Verdict Badge:** Prominent `🔴 FRAUDULENT TRANSACTION DETECTED` or `🟢 LEGITIMATE TRANSACTION APPROVED`.
- **Confidence Risk Score Meter:** Visual percentage gauge (e.g. `98.4% Confidence`).
- **Database Confirmation Alert:** Displays generated `#TXN-XXX` ID and SQLite commit confirmation.
- **Investigate Button:** Direct link navigating to the Single Transaction Forensic Dossier (`/transaction/<id>`).

---

## 3. Underlying Technical Architecture & ML Pipeline

```python
# 1. Validation & Parsing
amount = float(request.form.get("amount"))
hour = int(request.form.get("hour"))
if amount <= 0 or not (0 <= hour <= 23):
    raise ValueError("Invalid transaction parameters")

# 2. Scikit-Learn Model Prediction
df = pd.DataFrame([{
    "location": location,
    "device_type": device_type,
    "payment_method": payment_method,
    "amount": amount,
    "hour": hour,
    "txn_last_24h": txn_last_24h,
    "is_new_device": is_new_device
}])

# Pipeline performs One-Hot Encoding + Standard Scaling + Random Forest Trees Voting
proba = model.predict_proba(df)[0][1] # Probability of Class 1 (Fraud)
pred_class = "Fraud" if proba >= 0.5 else "Legitimate"

# 3. Persistent Storage in SQLite:
# Writes to 'transactions', 'predictions', and optionally 'alerts' if proba >= 0.5
```

---

## 4. Live Interactive Demonstration Walkthrough

1. **Step 1:** Click the **"Card-Not-Present Fraud Spike"** preset button.
2. **Step 2:** Point out how the 7 fields are populated with suspicious attributes (PKR 9,500, Hour 3:00 AM, Foreign, 12 transactions/24h, New Device).
3. **Step 3:** Click **"Evaluate Transaction Risk"**.
4. **Step 4:** Show the reviewer or interviewer the instant `🔴 FRAUDULENT TRANSACTION DETECTED` banner with ~100% Risk Score.
5. **Step 5:** Now click **"Legitimate Retail Purchase"** preset and re-run. Show how the model immediately drops the risk score to <5% and displays `🟢 LEGITIMATE TRANSACTION APPROVED`.

---

## 5. Architecture & Engineering Deep Dive Q&A

### Q1: "Why do you standard scale numeric inputs and one-hot encode categoricals inside the pipeline?"
> **Answer:** "Random Forest handles categorical indices, but standardizing via an explicit `ColumnTransformer` pipeline guarantees zero data leakage during evaluation. The `OneHotEncoder(handle_unknown='ignore')` ensures that if a new payment method appears in production, the application will not crash with an unhandled exception."

### Q2: "What happens when a transaction is scored as Fraud?"
> **Answer:** "The system executes a transactional multi-table write: first saving the raw payload into `transactions`, then recording the ML confidence score in `predictions`, and finally creating an operational alert in the `alerts` table for immediate analyst triage."
