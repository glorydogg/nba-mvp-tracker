{{ config(materialized='table') }}

WITH staging AS (
    SELECT * 
    FROM {{ ref('stg_mvp_rankings') }}
)

SELECT
    *,
    DENSE_RANK() OVER (ORDER BY MVP_SCORE DESC) AS MVP_RANK
FROM staging
ORDER BY MVP_RANK ASC