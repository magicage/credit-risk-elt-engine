#  Credit Risk ELT Engine

A production-grade, configuration-driven ELT framework for credit risk analytics. Built with **dbt** for declarative transformation, **Snowflake** for scalable data warehousing, and **Airflow** for orchestration. Designed for testability, scalability, and cross-team collaboration, strictly adhering to modern DataOps best practices.

## 🏗️ Architecture & Data Flow

graph TD
    subgraph Source Systems
        A[PostgreSQL / Mock Data]
        B[Client Fraud Logs JSON]
    end

    subgraph Snowflake Data Warehouse
        C[(RAW Layer)]
        D[(STAGING Layer)]
        E[(TRANSFORMATION Layer)]
        F[(SERVING Layer)]
    end

    subgraph Consumption
        G[BI Dashboards]
        H[ML Risk Models]
    end

    A -->|Python Sync| C
    B -->|Direct Ingestion| C
    C -->|dbt Staging Views<br/>JSON Parsing| D
    D -->|dbt Models & Snapshots<br/>SCD Type 2 / Incremental| E
    E -->|Aggregations| F
    F --> G
    F --> H

    subgraph CI/CD & DevOps
        I[GitHub Actions] -->|PR Trigger| J[Dynamic CI Schema]
        J -->|dbt build| E
    end

    ✨ Key Features & Highlights
1. 📊 Standard Data Warehouse Layering
Strict separation of concerns across RAW, STAGING, TRANSFORMATION, and SERVING schemas. Custom dbt macros (generate_schema_name) ensure precise schema routing, preventing namespace pollution.
2. 🔄 Incremental Processing & SCD Type 2
Fact Table (fct_loans): Uses incremental materialization with merge strategy. Configured with cluster_by: ['DATE(origination_date)'] to optimize Snowflake micro-partition pruning.
Dimension Table (dim_customers): Implements SCD Type 2 using dbt snapshots to track historical changes in customer demographics, enabling accurate point-in-time analysis.
3. 🧩 Semi-Structured Data (JSON) Parsing
Handles complex fraud detection logs using Snowflake's native high-performance capabilities:
Dot Notation: Efficiently extracts nested scalar values (e.g., payload:device.os::STRING).
LATERAL FLATTEN: Explodes JSON arrays into relational rows for downstream analysis, avoiding costly Python UDFs.
4. 🛡️ Data Quality Gates (Test-Driven Development)
Schema Tests: unique, not_null, accepted_values, relationships.
Custom Business Tests: Enforces financial domain rules (e.g., IFRS 9 stage migration logic, PD score monotonicity). Tests return failing rows, adhering to CDC (Continuous Data Quality) standards.
5. CI/CD with Dynamic Isolation
GitHub Actions pipeline automatically creates an isolated CI_<run_id> schema for every Pull Request, runs dbt build, and cleans up afterwards. This ensures zero pollution to production environments while allowing parallel testing.
🛠️ Tech Stack
Data Warehouse: Snowflake (Micro-partitions, Clustering, VARIANT JSON)
Transformation: dbt-core (v1.11), Jinja SQL, Python
Orchestration: Apache Airflow (DAG templates included)
CI/CD: GitHub Actions (Dynamic Schema Isolation)
Source Database: PostgreSQL (Dockerized for local dev)
Containerization: Docker & Docker Compose

## 📁 Project Structure

```text
credit-risk-elt-engine/
├── .github/
│   └── workflows/
│       └── dbt-ci.yml              # CI/CD pipeline for dbt validation
├── dbt_project/
│   ├── .dbt/
│   │   └── profiles.yml            # Connection profiles for dev and CI
│   ├── macros/                     # Custom Jinja macros and CI helpers
│   ├── models/
│   │   ├── ingestion/              # Source definitions and freshness rules
│   │   ├── staging/                # Data cleaning, JSON parsing, standardization
│   │   └── transformation/         # Core business logic: facts and dimensions
│   ├── snapshots/                  # SCD Type 2 history tracking
│   └── tests/                      # Custom SQL data tests
├── orchestration/
│   └── airflow/                    # Airflow DAG templates
├── scripts/                        # Data generation and Snowflake sync scripts
├── docker-compose.yml              # Local development services
└── README.md
```

## Local Development Setup

This project uses Docker Compose for a reproducible local environment.

### Start Dev Services

```bash
docker compose up -d postgres
```

### Generate & Sync Mock Data

```bash
python scripts/generate_data.py
set -a && source .env && set +a
python scripts/sync_to_snowflake.py
```

### Run dbt Pipeline

```bash
cd dbt_project
dbt deps
dbt build --target dev
```

🚀 CI/CD Workflow
1.Create a feature branch: git checkout -b feature/my-update
2.Push changes and open a Pull Request to main.
3.GitHub Actions automatically triggers the dbt CI/CD Pipeline.
4.The pipeline creates a temporary CI_<run_id> schema, runs dbt build, and posts the results as a PR comment.
5.Upon completion, the temporary schema is automatically dropped.

📈 Future Improvements
Snowpark Integration: Implement vectorized Python UDFs for complex PD/LGD scoring directly within Snowflake.
AI-Powered Discovery: Integrate LangChain to query dbt manifest.json for natural language data dictionary lookups.
Advanced Monitoring: Integrate dbt-artifacts package for execution cost tracking and Snowflake Query History analysis.
Row-Level Security (RLS): Implement dynamic data masking in the SERVING layer for BI consumers.
