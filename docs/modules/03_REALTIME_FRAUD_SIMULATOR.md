# Module 03: Live Transaction Traffic Simulator & Explainable AI (XAI)

## 1. Quick Reference & Specifications
- **URL Route:** `/simulator` (GET) and API endpoints:
  - `/api/simulate-stream` (GET, returns generated JSON transaction)
  - `/api/explain-transaction` (POST, returns real-time feature contribution weights)
- **Template File:** `templates/simulator.html`
- **Controller Functions:** `simulator()`, `simulate_stream()`, `explain_transaction()` in `app.py`
- **Primary Objective:** Provide interactive, real-time stress testing of the Machine Learning pipeline by synthesizing live transaction traffic, scoring each incoming payload instantly, and explaining fraud rationale on-the-fly without navigating away.

---

## 2. Visual Layout & On-Page Elements

### A. Simulator Control Panel (Top Header)
- **Engine Status Indicator:** Real-time pulse light (`Idle`, `Running Engine`, `Throttled`).
- **Generation Frequency Selector:** Adjustable simulation speed (1 sec, 2 sec, 5 sec intervals).
- **Fraud Injector Toggle:** Allows setting the injected fraud probability (e.g., 20% random attack frequency vs 80% realistic commerce).
- **Action Buttons:**
  - `Play / Start Stream`: Initiates continuous background stream generation.
  - `Pause Stream`: Temporarily halts the traffic flow.
  - `Clear Stream Log`: Cleans the visual log table.

### B. Live Stream Telemetry & Ticker
- **Streaming Stats Banner:** Shows live counts of:
  - Total Ingested Transactions in session.
  - Number of Intercepted Threats.
  - Total Scored PKR Volume.
  - Average ML Inference Latency (typically <12ms).

### C. Live Real-Time Transaction Feed (Stream Table)
- As transactions arrive, they slide dynamically into the top of the feed:
  - **Timestamp:** High-precision time format (`HH:MM:SS`).
  - **Transaction Identifier:** Clickable `#TXN-XXX` link.
  - **Amount:** PKR formatted with currency symbol.
  - **Behavioral Vectors:** Location pill (`foreign`, `domestic`, `local`), Hardware Client (`mobile`, `desktop`), Payment Method (`credit_card`, `debit_card`, `wallet`), 24h Velocity.
  - **Verdict Badge:** High-contrast `🔴 FRAUD` or `🟢 LEGITIMATE`.
  - **Risk Probability Meter:** Visual mini-bar showing confidence score (0% to 100%).
  - **Actions:**
    - **"Why Fraud?" (Crisis Alert Button):** Dedicated Explainable AI button present on every flagged transaction.
    - **"Investigate Dossier":** Opens full forensic dossier in a new tab.

### D. On-Page Explainable AI (XAI) Modal ("Why Was This Flagged?")
- Clicking **"Why Fraud?"** triggers an instant slide-in modal without refreshing or losing the live stream:
  - **Primary Trigger Factors:** Identifies the exact behavioral anomalies that pushed the Random Forest model over the fraud threshold (e.g., *Foreign location combined with 3:00 AM off-peak hour and 10 repeat attempts in 24h*).
  - **Feature Weight Cards:** Visual cards detailing each vector's mathematical influence on the verdict.
  - **Direct Dossier Link:** Allows jumping directly to `/transaction/<id>` if deeper forensic audit is required.

---

## 3. Underlying Technical Architecture & ML Pipeline

1. **Synthetic Data Generation Engine:**
   - Samples realistic distributions derived from empirical Pakistani e-commerce banking patterns.
   - For legitimate traffic: Low amounts (PKR 50 - 5,000), local/domestic origin, daytime hours (08:00 - 22:00), low 24h velocity (1-3 attempts), authenticated hardware.
   - For simulated attacks: High amounts (PKR 8,000 - 50,000+), foreign IP routing, nocturnal hours (01:00 - 05:00), velocity spikes (>8 attempts), unrecognized hardware fingerprints.

2. **Real-Time Scoring via Scikit-Learn Pipeline:**
   ```python
   # Raw dictionary payload is structured into pandas DataFrame
   input_df = pd.DataFrame([data])
   # Inference through preprocessor and classifier pipeline
   proba = model.predict_proba(input_df)[0][1]
   pred_class = "Fraud" if proba >= 0.5 else "Legitimate"
   ```

3. **Heuristic Explainability Algorithm (XAI):**
   - Computes deviation from baseline feature means and combines with global Random Forest feature importances:
     - `amount > 5000` (+25% risk contribution)
     - `location == 'foreign'` (+35% risk contribution)
     - `hour in [0, 1, 2, 3, 4, 5]` (+15% risk contribution)
     - `txn_last_24h >= 8` (+20% risk contribution)
     - `is_new_device == 1` (+15% risk contribution)

---

## 4. Live Interactive Demonstration Walkthrough

1. **Step 1:** Navigate to **Simulator** from the sidebar.
2. **Step 2:** Click **"Start Live Stream"**. Show the reviewer or interviewer the live transactions appearing automatically every 2 seconds with sub-15ms ML scoring latency.
3. **Step 3:** When a `🔴 FRAUD` transaction appears, click **"Pause Stream"**.
4. **Step 4:** Click the **"Why Fraud?"** button next to that transaction. Show the on-page XAI modal breaking down the exact reasons (e.g., high velocity + foreign location + nocturnal hour).
5. **Step 5:** Explain that this satisfies the **Explainable AI (XAI)** requirement, proving the model is not a blind "black-box".

---

## 5. Architecture & Engineering Deep Dive Q&A

### Q1: "Why did you build a simulator instead of just testing on static data?"
> **Answer:** "In real-world banking environments (e.g., SWIFT or Visa/MasterCard switch), transactions arrive as high-throughput event streams, not static CSVs. The simulator proves that our system architecture supports asynchronous, low-latency scoring and can handle continuous data ingestion in production."

### Q2: "What is Explainable AI (XAI) and why does a technical interviewer care about it?"
> **Answer:** "Under financial compliance regulations (like GDPR Article 22 'Right to Explanation' and SBP banking directives), an automated algorithm cannot reject a customer's payment without an explainable reason. Our XAI engine decomposes the prediction vector to reveal why the transaction was blocked."
