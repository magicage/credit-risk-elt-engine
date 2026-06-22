{% snapshot customer_scd %}

{{
    config(
        target_schema='TRANSFORMATION',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='source_updated_at',
        invalidate_hard_deletes=true,
        tags=['snapshot', 'scd2']
    )
}}

select
    customer_id,
    first_name,
    last_name,
    date_of_birth,
    employment_status,
    annual_income,
    ingested_at,
    dbt_updated_at::timestamp_ntz as source_updated_at  -- renaming dbt's internal updated_at to source_updated_at for clarity
from {{ ref('stg_customers') }}

{% endsnapshot %}