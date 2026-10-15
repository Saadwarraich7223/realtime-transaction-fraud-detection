# Module 02: Executive Fraud & Security Dashboard

## 1. Quick Reference & Specifications
- **URL Route:** `/` or `/dashboard` (GET)
- **Template File:** `templates/dashboard.html`
- **Controller Function:** `dashboard()` in `app.py`
- **Primary Data Sources:** `transactions`, `predictions`, `alerts` tables in `scam_detection.db`.
- **Primary Objective:** Provide C-level and senior security analysts with real-time operational risk metrics, 24-hour anomaly spikes, and capital loss mitigation statistics.

---

## 2. Visual Layout & On-Page Elements

### A. Top Executive Header
- **Page Title:** "Fraud Operations & Risk Command Center" with live status badge (`Operational`).
- **Quick Actions:** "Analyze Single Txn" (direct link to `/analyze`) and "Live Simulator" (link to `/simulator`).

### B. The 4 Financial & Risk KPI Cards (Clean, Uncluttered)
1. **Analyzed Volume (Card 1):**
   - Main Metric: Total transactions scored across the life of the system (e.g. `13` or `1,000+`).
   - Context Subtitle: Gross PKR volume processed (e.g., `PKR 52,665.53 Processed`).
   - Footer Badge: `[Green Dot] X Legitimate Transactions | Active Ledger`.
2. **Flagged Fraud (Card 2):**
   - Main Metric: Count of transactions classified as fraudulent (in bold crimson red `text-rose-600`).
   - Context Subtitle: Anomaly rate percentage (e.g., `30.8% Threat Detection Rate`).
   - Footer Badge: `[Red Pulsing Dot] Auto Quarantined | Threat Active`.
3. **Capital Protected (Card 3):**
   - Main Metric: Cumulative sum of PKR prevented from leaving the financial institution.
   - Context Subtitle: `Prevented Outflow`.
   - Footer Badge: `[Blue Dot] 100% Retained | Zero Breach`.
4. **Model Governance (Card 4):**
   - Main Metric: Current production ML accuracy (e.g. `98.6%`).
   - Context Subtitle: Model test F1-Score (e.g., `F1-Score: 86.0%`).
   - Footer Badge: `[Emerald Dot] RandomForest-v1 (Balanced)`.

### C. Analytics & Interactive Charts Section
1. **24-Hour Diurnal Velocity Chart (Left 8 Columns):**
   - Dual-line smooth area chart powered by Chart.js.
   - **Green Curve:** Legitimate transaction frequency distribution across hours 00:00 to 23:00.
   - **Red Curve:** Detected fraud frequency distribution, highlighting peak cybercrime windows (typically between 01:00 AM and 05:00 AM).
2. **Risk Spectrum Donut Chart (Right 4 Columns):**
   - Categorical breakdown of transactions by Risk Tiers:
     - Low Risk (<30% score): Green.
     - Moderate Suspicion (30%–60% score): Amber.
     - Critical High Anomaly (>60% score): Red.

### D. Live Active Security Alerts Feed (Table)
- Shows the latest transactions flagged as `Fraud` requiring immediate human review.
- Columns: `Alert ID`, `Severity Pill`, `Transaction ID`, `Amount (PKR)`, `Risk Probability`, `Timestamp`, `Actions`.
- Actions: "Investigate →" direct button navigating to the Single Transaction Forensic Dossier (`/transaction/<id>`).

---

## 3. Underlying Technical Architecture & SQL Queries

```python
# Aggregate Financial Volume and Fraud Ratios:
total_txns = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
total_volume = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions").fetchone()[0]
fraud_txns = conn.execute("SELECT COUNT(*) FROM predictions WHERE predicted_class='Fraud'").fetchone()[0]
fraud_volume = conn.execute("""
    SELECT COALESCE(SUM(t.amount), 0) 
    FROM transactions t 
    JOIN predictions p ON t.transaction_id = p.transaction_id 
    WHERE p.predicted_class='Fraud'
""").fetchone()[0]
```

- **Hourly Diurnal Aggregation:**
  SQL `GROUP BY hour` partitions volume into a 24-element vector `[0..23]` passed into Chart.js via JSON serialization.

---

## 4. Live Interactive Demonstration Walkthrough

1. **Step 1:** Point out the **4 KPI Cards** at the top. Explain how they translate raw machine learning outputs into real-world banking terminology (Capital Protected in PKR, Loss Avoidance).
2. **Step 2:** Hover over the **24-Hour Velocity Chart**. Show the reviewer or interviewer how legitimate transactions peak during daytime retail hours (10:00 AM to 08:00 PM), whereas fraudulent activities spike during late-night anomaly windows (02:00 AM to 04:00 AM).
3. **Step 3:** Point to the **Active Alerts Feed** at the bottom. Click **"Investigate →"** on any flagged alert to demonstrate the transition into the Single Transaction Forensic Dossier.

---

## 5. Architecture & Engineering Deep Dive Q&A

### Q1: "Why do you emphasize 'Capital Protected' over simple accuracy?"
> **Answer:** "In financial fraud detection, overall accuracy is deceptive due to severe class imbalance (99% of transactions are legitimate). A system that predicts everything as legitimate would achieve 99% accuracy but cause 100% financial ruin. 'Capital Protected' directly quantifies the monetary value saved by intercepting high-value fraudulent outflows."

### Q2: "How does the diurnal (hourly) chart help fraud analysts?"
> **Answer:** "Legitimate consumer transactions follow human biological patterns (active daytime, minimal sleeping hours). Scammers and automated credential-stuffing bots predominantly strike during off-peak hours (01:00 to 05:00 UTC) when fraud monitoring teams have lower staffing. The chart visualizes this anomaly disparity."
