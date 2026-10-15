"""
Generate a synthetic online-transaction dataset for training the
scam detection model. Produces transactions.csv with realistic
fraud patterns (high amounts, odd hours, foreign locations, new devices).
"""
import numpy as np
import pandas as pd

np.random.seed(42)
N = 5000

# --- legitimate transactions (~95%) ---
n_legit = int(N * 0.95)
legit = pd.DataFrame({
    "amount": np.round(np.random.gamma(2.0, 60, n_legit), 2),          # mostly small amounts
    "hour": np.random.choice(range(8, 23), n_legit),                    # daytime/evening
    "location": np.random.choice(["local", "domestic"], n_legit, p=[0.7, 0.3]),
    "device_type": np.random.choice(["mobile", "desktop"], n_legit, p=[0.6, 0.4]),
    "payment_method": np.random.choice(["credit_card", "debit_card", "wallet"], n_legit, p=[0.4, 0.4, 0.2]),
    "txn_last_24h": np.random.poisson(2, n_legit),                      # normal frequency
    "is_new_device": np.random.choice([0, 1], n_legit, p=[0.9, 0.1]),
    "is_fraud": 0,
})

# --- fraudulent transactions (~5%) ---
n_fraud = N - n_legit
fraud = pd.DataFrame({
    "amount": np.round(np.random.gamma(4.0, 500, n_fraud), 2),          # much larger amounts
    "hour": np.random.choice(list(range(0, 6)) + [23], n_fraud),        # late night
    "location": np.random.choice(["foreign", "domestic"], n_fraud, p=[0.8, 0.2]),
    "device_type": np.random.choice(["mobile", "desktop"], n_fraud, p=[0.5, 0.5]),
    "payment_method": np.random.choice(["credit_card", "debit_card", "wallet"], n_fraud, p=[0.6, 0.2, 0.2]),
    "txn_last_24h": np.random.poisson(8, n_fraud),                      # burst of transactions
    "is_new_device": np.random.choice([0, 1], n_fraud, p=[0.2, 0.8]),   # usually a new device
    "is_fraud": 1,
})

# --- hard cases: make some fraud look normal and some legit look suspicious ---
# (real-world fraud is not perfectly separable, so the model should not reach 100%)
hard_fraud_idx = fraud.sample(frac=0.35, random_state=1).index
fraud.loc[hard_fraud_idx, "amount"] = np.round(np.random.gamma(2.0, 80, len(hard_fraud_idx)), 2)
fraud.loc[hard_fraud_idx, "hour"] = np.random.choice(range(8, 23), len(hard_fraud_idx))
fraud.loc[hard_fraud_idx, "location"] = "domestic"
fraud.loc[hard_fraud_idx, "txn_last_24h"] = np.random.poisson(3, len(hard_fraud_idx))

hard_legit_idx = legit.sample(frac=0.05, random_state=2).index
legit.loc[hard_legit_idx, "amount"] = np.round(np.random.gamma(3.0, 350, len(hard_legit_idx)), 2)
legit.loc[hard_legit_idx, "hour"] = np.random.choice(list(range(0, 6)) + [23], len(hard_legit_idx))
legit.loc[hard_legit_idx, "is_new_device"] = 1

df = pd.concat([legit, fraud]).sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("transactions.csv", index=False)
print(f"Saved transactions.csv: {len(df)} rows ({df.is_fraud.sum()} fraud, {len(df)-df.is_fraud.sum()} legitimate)")
