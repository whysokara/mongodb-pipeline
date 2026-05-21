with source_data as (
select * from {{ source('mongodb_movies', 'RAW_MOVIES') }}
),
data_type_change as (
    
select 
    to_varchar(title) as title,
    try_to_number(year) as year,
    try_to_number(released) as released,
    to_varchar(rated) as rated,
    try_to_number(runtime) as runtime
from source_data
)

select * from data_type_change