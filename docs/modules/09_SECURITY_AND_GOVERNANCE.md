# Module 09: System Security Settings & Governance

## 1. Quick Reference & Specifications
- **URL Route:** `/settings` (GET, POST)
- **Template File:** `templates/settings.html`
- **Controller Function:** `settings()` in `app.py`
- **Access Level:** Role-Aware (Admin has full tuning and audit capabilities; Analyst has personal workstation settings).
- **Primary Objective:** Provide administrative governance over the anti-fraud decision engine, including ML sensitivity threshold tuning, telemetry monitoring, and immutable security audit logs.

---

## 2. Visual Layout & On-Page Elements

### A. Analyst / Admin Workstation Identity Card (Left)
- **Profile Avatar:** Monogram initials with role badge (`Administrator` or `Fraud Analyst`).
- **Workstation Identity:** Username, full name, enrollment date.
- **Access Level Privileges:** Summary of active session capabilities.

### B. Machine Learning Engine Threshold Tuning (Admin Only)
- **Decision Boundary Slider / Input:** Allows adjusting the classification threshold from `0.50` (Standard) to `0.30` (Aggressive Quarantine) or `0.70` (High Tolerance).
- **Velocity Limit Parameter:** Rolling 24-hour transaction attempt ceiling.
- **Auto-Refresh Rate:** Polling interval for live threat feeds.
- **Save / Restore Defaults Buttons:** Persists changes or resets to calibrated baseline parameters.

### C. Live Database & System Telemetry Metrics
- **Total Registered Users:** Count of active credentials in `users`.
- **Audited Ledger Size:** Total records in `transactions` and `predictions`.
- **Active Alerts Count:** Count of unresolved threats.
- **Storage Footprint:** SQLite database file size (`.db`) and serialized ML pipeline size (`model.pkl`).

### D. Security Audit Trails & Event Log Table
- Displays immutable log of system actions:
  - Timestamp of event.
  - Acting user (`admin` or `user`).
  - Action performed (`USER_LOGIN`, `MODEL_PREDICTION`, `LEDGER_PURGED`, `SETTINGS_UPDATED`).
  - IP Address / Workstation client.

---

## 3. Underlying Technical Architecture & Configuration Persistence

```python
# System configurations are persisted in a key-value SQLite table 'system_settings':
def get_system_settings():
    conn = get_db()
    rows = conn.execute("SELECT key, value FROM system_settings").fetchall()
    conn.close()
    return {row["key"]: row["value"] for row in rows}

def update_system_setting(key, value):
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO system_settings (key, value) VALUES (?, ?)", 
                 (key, str(value)))
    conn.commit()
    conn.close()
```

---

## 4. Live Interactive Demonstration Walkthrough

1. **Step 1:** Navigate to **"Settings"** from the bottom of the sidebar.
2. **Step 2:** Show the **Workstation Profile Card**: explain how user roles and identities are separated.
3. **Step 3:** Walk through the **Database Telemetry Card**: show the live SQLite database size in KB and the model size.
4. **Step 4:** Show the **Model Threshold Tuning**: explain how administrators can dynamically tighten or loosen fraud quarantine policies in response to seasonal shopping surges (e.g., Black Friday) without modifying a single line of Python source code!

---

## 5. Architecture & Engineering Deep Dive Q&A

### Q1: "Why would a bank ever want to adjust the fraud decision threshold?"
> **Answer:** "During peak shopping events like Eid or Black Friday, legitimate consumer velocity and spending surge drastically. An inflexible model would trigger thousands of false alarms, frustrating customers. By tuning the threshold from 0.50 to 0.60 via the Settings page, administrators can temporarily reduce false alarms while maintaining baseline security."

### Q2: "Where are these settings stored?"
> **Answer:** "Settings are persisted in the `system_settings` table in SQLite, ensuring that threshold adjustments and operational configurations survive server reboots."
