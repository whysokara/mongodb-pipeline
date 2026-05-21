with staging_movies as (
    select * from {{ ref('staging_movies') }}
)

select * from staging_movies
