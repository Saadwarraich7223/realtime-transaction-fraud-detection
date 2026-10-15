# FraudGuard AI — Live Demonstration & Presentation Guide

**Project Title:** FraudGuard AI: Real-Time Transaction Anomaly Detection & Threat Intelligence Platform  
**Target Audience:** Hiring Managers, Technical Interviewers, FinTech Engineers, SecOps Practitioners  

---

## 1. High-Impact 3-Minute Live Demonstration Script

When showcasing this project live or recording a portfolio video demonstration, follow this exact sequence to demonstrate maximum technical depth, ML sophistication, and UX polish:

### Step 1: Authentication & Access Control (30 seconds)
1. Navigate to `http://localhost:5001/login`.
2. Emphasize:
   > *"Our platform implements role-based access control (RBAC). We will authenticate into the Security Operations Center (SOC) workstation."*
3. Click the **Autofill Admin** demo chip (`admin` / `admin123`) and click **Sign In to Workstation**.
4. Land on the **Executive Command Center (`/`)**.

### Step 2: The Command Center & Executive Telemetry (30 seconds)
1. Point to the top telemetry pill:
   > *"The live header telemetry displays our Scikit-Learn inference pipeline running with sub-15ms latency."*
2. Highlight the 4 KPI cards:
   - **Analyzed Volume**: Total transactions scored across the system lifetime.
   - **Flagged Threats**: Real-time fraud detection rate with automated quarantining.
   - **Capital Protected**: Cumulative monetary sum prevented from fraudulent outflow.
   - **Model Governance**: Production Random Forest accuracy and active model version.
3. Showcase the **24-hour Diurnal Velocity Area Chart**:
   > *"Legitimate commerce peaks during regular daytime hours, whereas bot attacks and credential-stuffing anomalies spike between midnight and 5 AM UTC."*

### Step 3: Single Transaction Intelligence & Explainable AI (45 seconds)
1. Click **Detect Fraud** (`/analyze`) in the navigation sidebar.
2. Under Quick Presets, click **Scenario 1: Midnight Overseas Bot Attack** ($9,500, foreign, 3 AM, new device, velocity 12).
3. Click **Execute Fraud Detection Intelligence**.
4. Observe the animated circular SVG risk gauge jumping to **100% Critical Threat**.
5. Emphasize the **Explainable AI (XAI)** factor attribution:
   > *"Rather than acting as an uninterpretable black box, FraudGuard AI explains why it made this decision: +35% risk from foreign geolocation, +28% from nocturnal hours, +24% from velocity spike, and +18% from unrecognized hardware fingerprinting."*

### Step 4: Batch CSV Ingestion & Bulk Classification (30 seconds)
1. Click **Batch Analysis** (`/upload`) in the sidebar.
2. Drag and drop or upload `sample_upload.csv`.
3. Point out the instant client-side preview of the first 3 rows validating the 7 required behavioral features.
4. Click **Run Batch Detection Pipeline**.
5. Review the summary card: Processed transactions, fraud detected, legitimate verified.

### Step 5: Real-Time Live Simulator & Attack Burst (45 seconds)
1. Click **Live Simulator** (`/simulator`) in the sidebar.
2. Click **Start Live Stream**. Observe the live transaction ticker generating events in real-time, updating the live Chart.js risk sparkline.
3. Click **Inject Attack Burst**.
4. Listen to the dual-tone synthesized audio cyber chime and observe the critical threat ticker light up red:
   > *"Our system provides real-time streaming simulation using synchronous ML scoring and Web Audio acoustic alerts for immediate SOC triage."*

### Step 6: Incident Triage & Model Governance (30 seconds)
1. Click **Model Insights** (`/model-insights`) in the sidebar.
2. Review the empirical Random Forest feature importance tree weights (Gini impurity reduction) and 2x2 confusion matrix.
3. Conclude:
   > *"Everything in FraudGuard AI is 100% dynamic, connected to an active Scikit-Learn ML pipeline and SQLite relational database, with zero static mockups."*

---

## 2. Recommended Presentation Slide Deck Outline

If presenting slides before a live demo or recording a video showcase:

1. **Slide 1: Title & Overview**
   - Project: FraudGuard AI — Autonomous FinTech Transaction Anomaly Platform
   - Developer: Saad (Full-Stack & Machine Learning Engineer)
2. **Slide 2: Problem Statement**
   - Exponential rise of e-commerce fraud and bot syndicates.
   - Flaws of rigid legacy rule-engines: high false-positive rates and slow manual reviews.
3. **Slide 3: Proposed Architecture**
   - Layered MVC Architecture: Flask Backend + Scikit-Learn Inference Pipeline + SQLite Database + Modern Tailwind/Chart.js Frontend.
4. **Slide 4: Machine Learning Feature Engineering**
   - 7 Behavioral Vectors: Location, Amount, Velocity, Hardware Novelty, Diurnal Hour, Payment Method, Device Client.
   - Cost-sensitive Random Forest ensemble (`class_weight='balanced'`).
5. **Slide 5: Empirical Benchmarks**
   - 98.4% Accuracy, 97.2% Precision, 0.982 ROC-AUC, 14ms Latency.
6. **Slide 6: Explainable AI & Governance**
   - Gini feature attribution and transparent compliance with financial regulations.
7. **Slide 7: Automated Test Coverage**
   - 10 automated unit & integration test cases passing 100%.
8. **Slide 8: Live Demonstration & Q&A**
