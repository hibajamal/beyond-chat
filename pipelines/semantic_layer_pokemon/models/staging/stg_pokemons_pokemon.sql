{{ config(materialized='view') }}

with source as (
    select * from pokemons_main
)

select distinct
s.base_experience,
s.cries__latest,
s.cries__legacy,
s.height,
s.id pokemon_id,
s.is_default,
s.location_area_encounters,
s.name,
s.species__name,
s.species__url,
s.weight,
s._dlt_load_id,
s._dlt_id,
pms.base_stat,
pms.stat__name
from source s
left join pokemons_main__stats pms on pms._dlt_parent_id = s._dlt_id
