# 🏦 Credit Risk ELT Engine

A production-grade, configuration-driven ELT framework for credit risk analytics. Built with `dbt` for declarative transformation, `Snowpark` for vectorized feature engineering, and `Airflow` for orchestration & observability. Designed for testability, scalability, and cross-team collaboration.

## 🔍 JD Requirement Mapping
| Requirement | Implementation |
|-------------|----------------|
| Snowpark + dbt workflows | `dbt` handles SQL transformation & testing; `Snowpark` delivers vectorized UDFs for PD scoring & vintage analysis |
| CI/CD & test automation | GitHub Actions + `pre-commit` + `dbt compile/test` + manifest validation |
| Process monitoring | `run_results.json` parsing + SLA checks + Slack/email alerting + data freshness assertions |
| AI integration | LangChain RAG over `dbt manifest.json` metadata + secure Snowflake query execution |
| Financial/Credit Risk | Explicit IFRS 9 staging, PD/LGD modeling, vintage cohort tracking, delinquency migration logic |
