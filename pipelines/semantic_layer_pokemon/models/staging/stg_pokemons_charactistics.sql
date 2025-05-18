{{ config(materialized='view') }}

select distinct
pms.stat__name as stat_name,
sm.move_damage_class__name ,
split_part(smc.url, '/',7) as characteristic_id,
cmd.description
from pokemons_main__stats pms
left join stats_main sm on sm.name = pms.stat__name
left join stats_main__characteristics smc on sm._dlt_id = smc._dlt_parent_id
left join characteristics_main cm on split_part(smc.url, '/',7) = cm.id
left join characteristics_main__descriptions cmd on cmd._dlt_parent_id = cm._dlt_id
where cmd.language__name = 'en'