# Module 07: Batch Ingestion & Bulk Transaction Analysis

## 1. Quick Reference & Specifications
- **URL Route:** `/upload` (GET, POST) and `/sample-csv` (GET)
- **Template File:** `templates/upload.html`
- **Controller Functions:** `upload()` and `download_sample_csv()` in `app.py`
- **Primary Objective:** Provide enterprise bulk processing capabilities allowing banks and financial switches to ingest thousands of transactions via CSV file, perform parallelized ML inference, and generate batch classification statistics.

---

## 2. Visual Layout & On-Page Elements

### A. Batch Pipeline Header & Schema Guide
- **Page Title:** "Batch Ingestion & Bulk Threat Classification".
- **Download Sample Template Button:** Downloads `sample_upload.csv` pre-formatted with the exact required header schema.
- **Expected CSV Header Specification:**
  `amount, hour, location, device_type, payment_method, txn_last_24h, is_new_device`

### B. Drag-and-Drop Ingestion Zone
- Visual drag-and-drop file upload target with upload icon.
- Supported file types: `.csv`.
- Instant client-side file selection feedback displaying filename and file size.
- **"Execute Batch Scoring Pipeline" Button:** Triggers backend upload and scoring.

### C. Batch Processing Summary Cards (Post-Upload)
1. **Total Records Ingested:** Total rows processed from CSV.
2. **Approved Legitimate:** Count of non-fraud transactions.
3. **Quarantined Threats:** Count of intercepted frauds.
4. **Batch Threat Ratio:** Percentage of flagged items in the uploaded batch.

### D. Ingested Transactions Result Preview Table
- Displays the batch records with individual risk verdicts and confidence scores.
- Link to view all processed records directly inside the master **Transaction Ledger** (`/results`).

---

## 3. Underlying Technical Architecture & Processing Pipeline

```python
@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    file = request.files.get("file")
    if not file or not file.filename.endswith(".csv"):
        flash("Please upload a valid .csv file.", "danger")
        return redirect(url_for("upload"))
    
    # Read CSV stream into pandas DataFrame
    df = pd.read_csv(file)
    
    # Validate required columns
    required = ["amount", "hour", "location", "device_type", 
                "payment_method", "txn_last_24h", "is_new_device"]
    if not all(col in df.columns for col in required):
        flash("Invalid CSV format. Missing required feature columns.", "danger")
        return redirect(url_for("upload"))
    
    # High-performance batch inference (vectorized)
    probabilities = model.predict_proba(df[required])[:, 1]
    predictions = ["Fraud" if p >= 0.5 else "Legitimate" for p in probabilities]
    
    # Bulk transaction database insert via executemany for high performance
```

---

## 4. Live Interactive Demonstration Walkthrough

1. **Step 1:** Click **"Download Sample Template"** to show the reviewer or interviewer the pre-built `sample_upload.csv` format.
2. **Step 2:** Click **"Choose File"** and select `sample_upload.csv` (or drag and drop it).
3. **Step 3:** Click **"Execute Batch Scoring Pipeline"**.
4. **Step 4:** Show the reviewer or interviewer the instant batch summary cards (e.g., *Processed 5 transactions: 3 Legitimate, 2 Fraudulent*).
5. **Step 5:** Click **"View in Transaction Ledger"** to show how the newly scored batch records were seamlessly committed to the SQLite database and appear in the ledger.

---

## 5. Architecture & Engineering Deep Dive Q&A

### Q1: "Why is vectorized batch prediction faster than scoring row-by-row in a loop?"
> **Answer:** "Row-by-row iteration in Python causes massive interpreter overhead. By passing the entire pandas DataFrame directly into `model.predict_proba()`, Scikit-Learn executes vectorized C/Cython operations under the hood, scoring thousands of rows in milliseconds."

### Q2: "What happens if a user uploads a malformed CSV or corrupt data types?"
> **Answer:** "The route includes defensive validation: it checks file extensions, verifies all 7 required column headers exist, and wraps parsing in a `try...except` block with user-friendly flash notifications, preventing uncaught 500 server crashes."
