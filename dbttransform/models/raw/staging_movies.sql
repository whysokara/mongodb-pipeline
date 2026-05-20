with source_data as (

select * from {{ source('mongodb_movies', 'RAW_MOVIES') }}

)

select *
from source_data
