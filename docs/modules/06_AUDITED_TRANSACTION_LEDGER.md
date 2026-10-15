# Module 06: Audited Transaction Monitoring Ledger

## 1. Quick Reference & Specifications
- **URL Route:** `/results` (GET) and `/transactions/clear` (POST, Admin-Only)
- **Template File:** `templates/results.html`
- **Controller Function:** `results()` and `clear_transactions()` in `app.py`
- **Primary Objective:** Provide a tamper-evident audit ledger displaying all historical transactions, real-time client-side search, multi-vector filtering, dynamic pagination, quick inspection drawers, and role-guarded purge controls.

---

## 2. Visual Layout & On-Page Elements

### A. Top Action Toolbar
- **Ledger Title:** "Transaction Monitoring Ledger" with `Audited Ledger` status chip.
- **Export CSV Report Button:** Streams out full database history as a formatted spreadsheet via `/report.csv`.
- **+ New Txn Button:** Quick jump to single transaction analyzer (`/analyze`).
- **Clear Ledger Button (Role-Restricted):** 
  - Rendered **ONLY** if logged in as `Administrator` (`session.role == 'admin'`).
  - Completely hidden from standard Fraud Analysts (`role == 'user'`).
  - Protected on the backend with authorization verification.

### B. Interactive Filter & Live Search Toolbar
- **Live Search Input (`#tableSearchInput`):** Real-time keyup filter matching Transaction IDs, locations, hardware types, or PKR amounts.
- **Verdict Filter Dropdown (`#verdictFilter`):** Instant filter for `All Verdicts`, `Flagged Fraud Only`, or `Legitimate Only`.
- **Payment Method Dropdown (`#paymentFilter`):** Filters by `Credit Card`, `Debit Card`, or `Digital Wallet`.
- **Dynamic Counters:** Displays real-time matching count and active low-risk vs anomaly flag legend.

### C. Audited Transactions Data Table
- Columns:
  1. `Txn ID`: Formatted `#TXN-XXX` linking directly to the Forensic Dossier.
  2. `Amount (PKR)`: Currency-formatted monetary value.
  3. `Hour`: Diurnal hour formatted as `HH:00` with crimson highlights for night hours (00:00 - 05:00).
  4. `Geolocation`: Pill badge indicating `local`, `domestic`, or `foreign`.
  5. `Device`: Hardware type with `(New)` flag for unrecognized devices.
  6. `Payment`: Payment rail used.
  7. `Classification`: Green `LEGITIMATE` or Red `FRAUD` badge.
  8. `Risk Score`: Percentage probability bar (0% - 100%).
  9. `Timestamp`: ISO-standard audit timestamp.
  10. `Inspect`: Quick Drawer View button (eye icon) + Direct Dossier button.

### D. Clean Dynamic Pagination Toolbar
- **Left Summary:** `Showing X to Y of Z transactions • Show [Select: 5, 10, 15, 25, 50, All] per page`.
- **Right Controls:**
  - `‹ Prev` button (disabled on page 1).
  - Numbered page pills (`1`, `2`, `3`...) with active highlight for the current page.
  - Smart ellipsis (`...`) for large record sets.
  - `Next ›` button (disabled on final page).
- **Responsive Slicing:** Selecting `5` per page immediately partitions records into multiple pages with instant pagination navigation.

### E. Quick Drawer Inspection Modal
- Triggered by clicking the eye icon on any row:
  - Instant overlay without reloading the page.
  - Shows 7-feature breakdown, verdict banner, and direct link to full dossier.

### F. Admin Purge Ledger Confirmation Modal
- Destructive safety modal requiring explicit administrator confirmation before purging records.

---

## 3. Underlying Technical Architecture & JavaScript Logic

1. **Client-Side Reactive Filtering & Pagination:**
   ```javascript
   function filterTable() {
     const searchVal = document.getElementById('tableSearchInput').value.toLowerCase();
     const verdictVal = document.getElementById('verdictFilter').value;
     const paymentVal = document.getElementById('paymentFilter').value;
     
     currentFilteredRows = allRows.filter(row => {
       // Multi-attribute matching
       return matchesSearch && matchesVerdict && matchesPayment;
     });
     
     currentPage = 1;
     renderPagination();
   }
   ```

2. **Role-Based Ledger Purge Security:**
   ```python
   @app.route("/transactions/clear", methods=["POST"])
   @login_required
   def clear_transactions():
       if session.get("role") != "admin":
           flash("Access Denied: Only administrators can clear the transaction ledger.", "danger")
           return redirect(url_for("results"))
       
       # Atomic SQLite deletion across transactions, predictions, and alerts
       conn.execute("DELETE FROM alerts")
       conn.execute("DELETE FROM predictions")
       conn.execute("DELETE FROM transactions")
       conn.commit()
   ```

---

## 4. Live Interactive Demonstration Walkthrough

1. **Step 1:** Demonstrate **Pagination**: Show how page size `5` creates 3 pages. Click **`Next ›`** to smoothly page through rows 6 to 10, then rows 11 to 13.
2. **Step 2:** Change the dropdown to **`10`** and show how the table instantly recalculates into 2 pages.
3. **Step 3:** Use the **Live Search**: Type `"foreign"` or `"9500"` in the search bar. Show how the table filters instantly without refreshing the page.
4. **Step 4:** Click the **Eye Icon** on any row to open the **Quick Inspection Drawer**.
5. **Step 5:** Point out the **"Clear Ledger"** button. Explain that because you are logged in as Admin, the button is available, but if logged in as Analyst, the button is completely absent for security compliance.

---

## 5. Architecture & Engineering Deep Dive Q&A

### Q1: "Why did you implement client-side filtering and pagination?"
> **Answer:** "Client-side pagination provides zero-latency instant filtering and page switching for thousands of audit records without issuing repetitive HTTP requests to the database, delivering an enterprise-grade responsive experience."

### Q2: "How do you prevent an ordinary user from hacking the 'Clear Ledger' function by crafting a POST request with Postman or Curl?"
> **Answer:** "Security is enforced at the backend controller level, not just in HTML. Even if an analyst bypasses the UI and posts directly to `/transactions/clear`, the route checks `if session.get('role') != 'admin':` and immediately rejects the request with an HTTP 403 / Access Denied flash message."
