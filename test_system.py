"""
System test suite - Online Transaction Scam Detection System.
Run with:  python -m unittest test_system -v

Covers unit testing (ML model, validation), integration testing
(Flask routes + database + model together), and the main functional
requirements FR1-FR10 from the SRS.
"""
import os
import unittest

os.environ.setdefault("TESTING", "1")

import app as application
from app import app, init_db, parse_txn_form, predict_transaction


FRAUD_TXN = {"amount": 9500, "hour": 3, "location": "foreign",
             "device_type": "mobile", "payment_method": "credit_card",
             "txn_last_24h": 12, "is_new_device": 1}
LEGIT_TXN = {"amount": 45, "hour": 14, "location": "local",
             "device_type": "mobile", "payment_method": "debit_card",
             "txn_last_24h": 1, "is_new_device": 0}


class UnitTests(unittest.TestCase):
    """TC-01 .. TC-04: unit tests for the ML model and input validation."""

    def test_tc01_fraud_pattern_detected(self):
        predicted, score = predict_transaction(FRAUD_TXN)
        self.assertEqual(predicted, "Fraud")
        self.assertGreater(score, 0.5)

    def test_tc02_legitimate_pattern_detected(self):
        predicted, score = predict_transaction(LEGIT_TXN)
        self.assertEqual(predicted, "Legitimate")
        self.assertLess(score, 0.5)

    def test_tc03_invalid_amount_rejected(self):
        bad = dict(LEGIT_TXN, amount=-100)
        with self.assertRaises(ValueError):
            parse_txn_form(bad)

    def test_tc04_invalid_hour_rejected(self):
        bad = dict(LEGIT_TXN, hour=99)
        with self.assertRaises(ValueError):
            parse_txn_form(bad)


class IntegrationTests(unittest.TestCase):
    """TC-05 .. TC-10: integration tests through the Flask application."""

    @classmethod
    def setUpClass(cls):
        init_db()
        app.config["TESTING"] = True

    def login(self, client, username="user", password="user123"):
        return client.post("/login", data={"username": username,
                                           "password": password},
                           follow_redirects=True)

    def test_tc05_login_valid_credentials(self):
        with app.test_client() as c:
            resp = self.login(c)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Dashboard", resp.data)

    def test_tc06_login_invalid_credentials(self):
        with app.test_client() as c:
            resp = c.post("/login", data={"username": "user",
                                          "password": "wrongpass"})
            self.assertIn(b"Invalid username or password", resp.data)

    def test_tc07_dashboard_requires_login(self):
        with app.test_client() as c:
            resp = c.get("/", follow_redirects=False)
            self.assertEqual(resp.status_code, 302)
            self.assertIn("/login", resp.headers["Location"])

    def test_tc08_analyze_fraud_creates_alert(self):
        with app.test_client() as c:
            self.login(c)
            resp = c.post("/analyze", data={k: str(v) for k, v in FRAUD_TXN.items()})
            self.assertIn(b"FRAUDULENT", resp.data)
            dashboard = c.get("/")
            self.assertIn(b"FRAUD", dashboard.data)   # alert visible

    def test_tc09_csv_upload_batch_prediction(self):
        header = "amount,hour,location,device_type,payment_method,txn_last_24h,is_new_device\n"
        rows = ("45,14,local,mobile,debit_card,1,0\n"
                "9500,3,foreign,mobile,credit_card,12,1\n")
        with app.test_client() as c:
            self.login(c)
            data = {"file": (__import__("io").BytesIO((header + rows).encode()), "batch.csv")}
            resp = c.post("/upload", data=data, content_type="multipart/form-data")
            self.assertIn(b"Processed <strong>2</strong>", resp.data)

    def test_tc10_report_export_csv(self):
        with app.test_client() as c:
            self.login(c)
            resp = c.get("/report.csv")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("text/csv", resp.content_type)
            self.assertIn(b"TransactionID", resp.data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
