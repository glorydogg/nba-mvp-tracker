{{ config(materialized='view') }}

SELECT *
FROM NBA_MVP_DB.PUBLIC.MVP_RANKINGS