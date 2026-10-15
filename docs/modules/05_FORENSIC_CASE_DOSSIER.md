# Module 05: Single Transaction Forensic Dossier & Deep Inspection

## 1. Quick Reference & Specifications
- **URL Route:** `/transaction/<int:txn_id>` (GET)
- **Template File:** `templates/transaction_detail.html`
- **Controller Function:** `transaction_detail(txn_id)` in `app.py`
- **Primary Objective:** Provide a comprehensive, full-page forensic investigation dossier for any single transaction in the database, complete with an interactive risk gauge speedometer, 7-feature behavioral matrix, XAI factor impact cards, and audit actions (Print/Export).

---

## 2. Visual Layout & On-Page Elements

### A. Case File Header & Navigation
- **Dossier Case Number:** `TRANSACTION DOSSIER #TXN-XXX` with timestamp.
- **Back Button:** "← Back to Ledger" allowing seamless return to `/results`.
- **Action Buttons:**
  - `Print Forensic Report`: Invokes browser print formatting.
  - `Export PDF / Case Dossier`: Standardized export for compliance records.

### B. The Risk Probability Speedometer (Analog Semi-Circle Gauge)
- **Dynamic CSS/SVG Gauge:** Displays a 180-degree calibrated dial from `0% (Safe)` to `100% (High Anomaly)`.
- **Needle Rotation:** Mathematically bound to `calc(score * 180deg - 90deg)`.
- **Verdict Card:** 
  - Green Shield with `LEGITIMATE CLEARED` if score < 50%.
  - Pulsing Crimson Shield with `FLAGGED FRAUDULENT` if score $\ge$ 50%.

### C. Evaluated Behavioral Feature Matrix (7 Vector Cards)
1. **Monetary Value:** Formatted PKR amount with baseline comparison.
2. **Execution Window:** Diurnal hour (e.g. `03:00 UTC - High Anomaly Night Window`).
3. **Geographical IP Route:** Origin tagged with security badge (`Foreign IP - Flagged`).
4. **Client Hardware Type:** `Mobile Client`, `Desktop Workstation`, or `Tablet`.
5. **Payment Instrument:** Payment rail used (`Credit Card`, `Debit Card`, `Digital Wallet`).
6. **Rolling 24-Hour Velocity:** Number of attempts in previous 24 hours.
7. **Hardware Fingerprint History:** `Known Authenticated Hardware` vs `Unrecognized New Device (Risk)`.

### D. Explainable AI (XAI) Attribution & Factor Impact Breakdown
- Individual cards rating whether each factor had a **Positive Impact (+ Risk)**, **Neutral Impact**, or **Mitigating Factor (- Risk)** on the final Random Forest prediction.
- Shows percentage weight contribution and human-readable explanation of why the model flagged this attribute.

### E. Security Investigation Timeline
- Step 1: Transaction Ingested & Schema Validated.
- Step 2: Random Forest Scored across 100 Decision Trees.
- Step 3: Risk Level Evaluated against 50% Threshold.
- Step 4: Security Alert Created & Ledger Audited.

---

## 3. Underlying Technical Architecture & Calculation Logic

```python
@app.route("/transaction/<int:txn_id>")
@login_required
def transaction_detail(txn_id):
    conn = get_db()
    txn = conn.execute("""
        SELECT t.*, p.predicted_class, p.score, p.created_at as scored_at
        FROM transactions t
        LEFT JOIN predictions p ON t.transaction_id = p.transaction_id
        WHERE t.transaction_id = ?
    """, (txn_id,)).fetchone()
    
    # Dynamic Explainable AI Risk Attribution Calculations:
    # Analyzes amount, velocity, hour, location, and hardware novelty
    # Returns formatted factor impact cards to the template
```

---

## 4. Live Interactive Demonstration Walkthrough

1. **Step 1:** From the **Ledger** or **Dashboard**, click on any transaction ID (e.g., `#TXN-80` or `#TXN-115`) or click **"Dossier"**.
2. **Step 2:** Point out the **Risk Gauge Speedometer**. Show how the needle points directly to 100% (or 0%) with calibrated color gradients.
3. **Step 3:** Walk through the **7-Feature Matrix** to show every parameter captured for this transaction.
4. **Step 4:** Highlight the **XAI Factor Impact Cards** to explain exactly why this specific transaction was deemed a risk.
5. **Step 5:** Click **"Print Forensic Report"** to show the reviewer or interviewer that the dossier is formatted cleanly for physical bank compliance audit trails.

---

## 5. Architecture & Engineering Deep Dive Q&A

### Q1: "Why did you build a dedicated dossier page instead of just showing details in a pop-up?"
> **Answer:** "In institutional anti-money-laundering (AML) and banking fraud compliance, forensic evaluators or engineering interviewers require an immutable, comprehensive dossier they can audit, print, and attach to regulatory reports. A dedicated dossier URL (`/transaction/<id>`) provides bookmarkable, deep-linkable case management."

### Q2: "How is the needle rotation of the speedometer calculated?"
> **Answer:** "It is dynamically derived from the model's confidence probability `p.score`. Because a semi-circular speedometer spans 180 degrees from -90° to +90°, we calculate `deg = (score * 180) - 90`. A score of 0.0 results in -90° (full left, safe green), 0.5 results in 0° (center, caution), and 1.0 results in +90° (full right, danger red)."
