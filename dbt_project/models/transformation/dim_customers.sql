{{
    config(
        materialized='table',
        tags=['transformation', 'dimension']
    )
}}

with scd as (
    select * from {{ ref('customer_scd') }}
    where dbt_valid_to is null
),

dim as (
    select
        customer_id,
        first_name || ' ' || last_name as full_name,
        date_of_birth,
        employment_status,
        annual_income,
        datediff(year, date_of_birth, current_date) as age,
        case
            when annual_income < 30000 then 'low'
            when annual_income between 30000 and 80000 then 'medium'
            else 'high'
        end as income_bracket,
        dbt_valid_from as dimension_loaded_at
    from scd
)

select * from dim