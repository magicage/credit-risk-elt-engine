{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='loan_id',
        cluster_by=['DATE(origination_date)'],
        tags=['transformation', 'fact']
    )
}}

with stg_loans as (
    select * from {{ ref('stg_loans') }}
),

{% if is_incremental() %}

filtered as (
    select * from stg_loans
    where dbt_updated_at > (select max(dbt_updated_at) from {{ this }})
)
{% else %}

filtered as (
    select * from stg_loans
)
{% endif %}

select
    loan_id,
    customer_id,
    product_type,
    origination_date,
    term_months,
    interest_rate,
    loan_amount,
    loan_status,
    delinquency_days,
    pd_score,
    ifrs9_stage,
    vintage_month,
    dbt_updated_at
from filtered