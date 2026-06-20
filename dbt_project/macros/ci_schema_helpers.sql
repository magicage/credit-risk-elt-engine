{% macro create_ci_schema() %}
    {% set ci_schema = target.schema %}
    {% set create_schema_sql %}
        CREATE SCHEMA IF NOT EXISTS {{ ci_schema }}
    {% endset %}
    {% do run_query(create_schema_sql) %}
    {{ log("✅ CI Schema '" ~ ci_schema ~ "' created successfully", info=true) }}
{% endmacro %}

{% macro drop_ci_schema() %}
    {% set ci_schema = target.schema %}
    {% set drop_schema_sql %}
        DROP SCHEMA IF EXISTS {{ ci_schema }} CASCADE
    {% endset %}
    {% do run_query(drop_schema_sql) %}
    {{ log("🗑️ CI Schema '" ~ ci_schema ~ "' dropped successfully", info=true) }}
{% endmacro %}