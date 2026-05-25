-- scripts/db/init.sql
CREATE TABLE IF NOT EXISTS customers (
    customer_id UUID PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    employment_status VARCHAR(20),
    annual_income DECIMAL(12,2),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS loans (
    loan_id UUID PRIMARY KEY,
    customer_id UUID,  -- 👈 暂时移除 REFERENCES customers(customer_id)
    product_type VARCHAR(30),
    origination_date DATE,
    term_months INT,
    interest_rate DECIMAL(5,2),
    loan_amount DECIMAL(12,2),
    status VARCHAR(20),
    delinquency_days INT DEFAULT 0,
    pd_score DECIMAL(5,4),
    ifrs9_stage INT,
    vintage_month DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
    -- FOREIGN KEY (customer_id) REFERENCES customers(customer_id)  -- 👈 暂时注释
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id UUID PRIMARY KEY,
    loan_id UUID,  -- 👈 暂时移除 REFERENCES loans(loan_id)
    transaction_date DATE,
    amount DECIMAL(12,2),
    type VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW()
    -- FOREIGN KEY (loan_id) REFERENCES loans(loan_id)  -- 👈 暂时注释
);