# scripts/generate_data.py
import pandas as pd
import numpy as np
from faker import Faker
import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import os

RANDOM_SEED = 42
N_CUSTOMERS = 5000
N_LOANS = 15000
N_TRANSACTIONS = 60000

fake = Faker()
np.random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)

engine = create_engine(os.getenv("DATABASE_URL", "postgresql://credit_dev:devpass123@localhost:5432/credit_risk_db"))

def generate_customers(n):
    records = []
    for _ in range(n):
        records.append({
            "customer_id": str(uuid.uuid4()),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "date_of_birth": fake.date_of_birth(minimum_age=20, maximum_age=65),
            "employment_status": np.random.choice(["employed", "self_employed", "unemployed", "retired"], p=[0.6, 0.2, 0.1, 0.1]),
            "annual_income": float(np.clip(np.random.normal(55000, 15000), 15000, 200000)),
        })
    return pd.DataFrame(records)

def generate_loans(customers_df, n):
    records = []
    customer_ids = customers_df["customer_id"].tolist()
    products = ["personal_loan", "mortgage", "auto_loan", "credit_card"]
    terms = {"personal_loan": 36, "mortgage": 240, "auto_loan": 60, "credit_card": 12}
    rates = {"personal_loan": 0.08, "mortgage": 0.035, "auto_loan": 0.06, "credit_card": 0.18}
    
    for _ in range(n):
        cust_id = np.random.choice(customer_ids)
        prod = np.random.choice(products, p=[0.4, 0.3, 0.2, 0.1])
        orig_date = fake.date_between(start_date="-5y", end_date="-1m")
        term = terms[prod]
        rate = rates[prod] + float(np.clip(np.random.normal(0, 0.01), -0.005, 0.02))
        amount = np.random.choice([5000, 10000, 25000, 50000, 100000, 250000, 500000], p=[0.2, 0.25, 0.2, 0.15, 0.1, 0.08, 0.02])
        
        # 模拟逾期天数与状态逻辑
        delq = int(np.random.exponential(15))
        delq = min(delq, 365)
        if delq == 0: status = "current"
        elif delq <= 30: status = "past_due_1_30"
        elif delq <= 90: status = "past_due_31_90"
        else: status = "default"
        
        # IFRS 9 阶段划分
        if delq <= 30: stage = 1
        elif delq <= 90: stage = 2
        else: stage = 3
        
        # 简单 PD 模拟 (仅演示)
        pd_score = max(0.001, min(0.99, 0.02 + 0.0001 * delq + np.random.normal(0, 0.01)))
        
        records.append({
            "loan_id": str(uuid.uuid4()),
            "customer_id": cust_id,
            "product_type": prod,
            "origination_date": orig_date,
            "term_months": term,
            "interest_rate": round(rate, 4),
            "loan_amount": round(amount, 2),
            "status": status,
            "delinquency_days": delq,
            "pd_score": round(pd_score, 4),
            "ifrs9_stage": stage,
            "vintage_month": orig_date.replace(day=1),
        })
    return pd.DataFrame(records)

def generate_transactions(loans_df, n):
    records = []
    loan_ids = loans_df["loan_id"].tolist()
    for _ in range(n):
        lid = np.random.choice(loan_ids)
        tx_date = fake.date_between(start_date="-2y", end_date="today")
        amount = round(float(np.clip(np.random.normal(500, 200), 50, 5000)), 2)
        tx_type = np.random.choice(["repayment", "fee", "interest", "late_charge"], p=[0.7, 0.1, 0.15, 0.05])
        records.append({
            "transaction_id": str(uuid.uuid4()),
            "loan_id": lid,
            "transaction_date": tx_date,
            "amount": amount,
            "type": tx_type,
        })
    return pd.DataFrame(records)

if __name__ == "__main__":
    print("🔄 Generating customers...")
    customers = generate_customers(N_CUSTOMERS)
    customers.to_sql("customers", engine, if_exists="replace", index=False)
    
    print("🔄 Generating loans...")
    loans = generate_loans(customers, N_LOANS)
    loans.to_sql("loans", engine, if_exists="replace", index=False)
    
    print("🔄 Generating transactions...")
    txs = generate_transactions(loans, N_TRANSACTIONS)
    txs.to_sql("transactions", engine, if_exists="replace", index=False)
    
    print("✅ Data loaded to PostgreSQL. Ready for dbt/Snowflake sync.")