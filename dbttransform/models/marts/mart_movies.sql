with stg_movies as (
    select * from {{ ref('stg_movies') }}
),

final as (
    select 
        title,
        year,
        runtime,
        released,
        rated,
        -- A simple business calculation: decade
        (floor(year / 10) * 10)::int as release_decade
    from stg_movies
    where year is not null
)

select * from final
