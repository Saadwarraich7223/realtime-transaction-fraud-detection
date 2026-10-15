# Module 01: Login & Role-Based Authentication

## 1. Quick Reference & Specifications
- **URL Route:** `/login` (GET, POST) and `/logout` (GET)
- **Template File:** `templates/login.html`
- **Controller Function:** `login()` and `logout()` in `app.py`
- **Security Mechanism:** Werkzeug PBKDF2 with SHA-256 password hashing, Flask cryptographic session cookies.
- **Default Credentials:**
  - **Administrator:** `admin` / `admin123` (Role: `admin`)
  - **Fraud Analyst:** `user` / `user123` (Role: `user`)

---

## 2. Visual Layout & On-Page Elements

### A. Branding & Identity Header
- **FraudGuard AI Logo:** Dual shield icon with gradient blue accent representing banking-grade security.
- **System Version Badge:** `v2.4 Production Engine` indicating an enterprise ML release.
- **Subheading:** "Autonomous Financial Transaction Fraud Detection & Risk Quarantine Engine".

### B. Authentication Card
- **Username Field (`input[name="username"]`):** Validates required presence, sanitized against SQL injection via parameterized queries.
- **Password Field (`input[name="password"]`):** Masked input field with password toggle visibility icon.
- **Quick-Fill Role Selectors:** Two demo buttons allowing the recruiter or reviewer to 1-click fill `admin` or `user` credentials for presentation convenience.
- **Submit Button ("Sign In to Workstation"):** Triggers secure POST request with animated loading feedback.

---

## 3. Underlying Technical Architecture & Data Flow

1. **Password Verification:**
   ```python
   # Passwords are NEVER stored in plaintext. They use salted PBKDF2 hashes:
   user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
   if user and check_password_hash(user["password_hash"], password):
       session["user_id"] = user["user_id"]
       session["username"] = user["username"]
       session["role"] = user["role"]
       session["name"] = user["name"]
   ```

2. **Session Security & Role-Based Access Control (RBAC):**
   - `@login_required` decorator checks `if "user_id" not in session:` and redirects unauthorized requests to `/login`.
   - Role segregation:
     - `admin`: Granted destructive privileges (Purge Ledger, System Threshold Adjustments, User Management).
     - `user` (Fraud Analyst): Read/Scoring access (Detect Fraud, Simulator, Ledger, Batch Ingestion), but destructive buttons (Clear Ledger) are hidden in UI and rejected by backend authorization checks.

---

## 4. Live Interactive Demonstration Walkthrough

1. **Step 1:** Open `http://localhost:5001`. Point out how trying to access the dashboard automatically redirects to `/login` because unauthenticated access is strictly blocked.
2. **Step 2:** Click the **"Fill Analyst"** button (`user` / `user123`) and log in. Point out the workstation sidebar display name (`Analyst: Saad`) and show that the "Clear Ledger" button is hidden.
3. **Step 3:** Log out and log back in as **"Administrator"** (`admin` / `admin123`). Show how the workstation badge reflects `Administrator` and the red "Clear Ledger" security button becomes visible.

---

## 5. Architecture & Engineering Deep Dive Q&A

### Q1: "How do you protect user passwords against database leaks?"
> **Answer:** "We use Werkzeug's `generate_password_hash()` implementing salted PBKDF2 with SHA-256. Even if an attacker obtains an offline dump of `scam_detection.db`, passwords cannot be decrypted because each hash contains a unique cryptographic salt preventing rainbow-table attacks."

### Q2: "What is Role-Based Access Control (RBAC) in your system?"
> **Answer:** "RBAC partitions system permissions between `admin` and `user`. Administrators have authority over governance policies, threshold tuning, and database ledger purging. Fraud Analysts can score transactions, monitor alerts, and generate reports, but are blocked from deleting audit trails."

### Q3: "What prevents SQL Injection on the login form?"
> **Answer:** "All queries in SQLite use parameterized statements with `?` placeholders (e.g., `SELECT * FROM users WHERE username=?`). User inputs are treated strictly as data literals, rendering SQL injection payloads inert."
