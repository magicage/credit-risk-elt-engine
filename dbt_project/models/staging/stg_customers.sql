{{ config(materialized='view') }}

with source as (
    select * from {{ source('credit_risk_src', 'customers') }}
),

renamed as (
    select
        customer_id,
        first_name,
        last_name,
        cast(date_of_birth as date) as date_of_birth,
        lower(employment_status) as employment_status,
        annual_income,
        created_at as ingested_at,
        {{ current_timestamp() }} as dbt_updated_at
    from source
)

select * from renamed