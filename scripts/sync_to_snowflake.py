import pandas as pd
from sqlalchemy import create_engine
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# ================= 配置区 =================
PG_URL = 'postgresql://credit_dev:devpass123@localhost:5432/credit_risk_db'

PG_USER = os.environ.get('PG_USER', 'credit_dev')
PG_PASS = os.environ.get('PG_PASS', 'devpass123')
PG_HOST = os.environ.get('PG_HOST', 'localhost')
PG_PORT = os.environ.get('PG_PORT', '5432')
PG_DB = os.environ.get('PG_DB', 'credit_risk_db')
PG_URL = f'postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}'

SF_CONFIG = {
    'user': os.environ.get('SNOWFLAKE_USER'),
    'password': os.environ.get('SNOWFLAKE_PASSWORD'),
    'account': os.environ.get('SNOWFLAKE_ACCOUNT'),
    'warehouse': os.environ.get('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
    'database': os.environ.get('SNOWFLAKE_DATABASE', 'CREDIT_RISK_DB'),
    'schema': 'RAW'
}

required_vars = ['SNOWFLAKE_USER', 'SNOWFLAKE_PASSWORD', 'SNOWFLAKE_ACCOUNT']
missing_vars = [var for var in required_vars if not os.environ.get(var)]
if missing_vars:
    raise EnvironmentError(f" Environment variables are missing: {missing_vars} run: source ../.env")
# ==========================================

def sync_table(table_name):
    print(f"🔄 Syncing {table_name}...")
    
    # 1. read fromPostgreSQL
    df = pd.read_sql(f"SELECT * FROM {table_name}", create_engine(PG_URL))
    df.columns = [c.upper() for c in df.columns]  
    
    # 2. connect Snowflake
    conn = snowflake.connector.connect(**SF_CONFIG)
    
    # 3. overwrite
    conn.cursor().execute(f"TRUNCATE TABLE RAW.{table_name}")
    success, nchunks, nrows, _ = write_pandas(
        conn, df, table_name, 
        quote_identifiers=False,
        auto_create_table=False
    )
    print(f"✅ {table_name}: {nrows} rows loaded")
    conn.close()

if __name__ == "__main__":
    for tbl in ['CUSTOMERS', 'LOANS', 'TRANSACTIONS']:
        sync_table(tbl)
    print("🎉 All tables synced to Snowflake RAW schema!")