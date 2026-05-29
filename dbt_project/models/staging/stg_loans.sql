{{ config(materialized='view') }}

with source as (
    select * from {{ source('credit_risk_src', 'loans') }}
),

renamed as (
    select
        loan_id,
        customer_id,
        lower(product_type) as product_type,
        cast(origination_date as date) as origination_date,
        term_months,
        interest_rate,
        loan_amount,
        --
        case 
            when status = 'current' then 'active'
            when status like 'past_due%' then 'delinquent'
            when status = 'default' then 'charged_off'
            else status
        end as loan_status,
        delinquency_days,
        pd_score,
        ifrs9_stage,
        cast(vintage_month as date) as vintage_month,
        created_at as ingested_at,
        {{ current_timestamp() }} as dbt_updated_at
    from source
)

select * from renamed