{{ config(materialized='view') }}

select distinct pm.id as pokemon_id,
am.id as ability_id,
am.name as ability_name,
ee.effect as ability_effects
from pokemons.pokemons_main pm
left join pokemons.pokemons_main__abilities pa on pa._dlt_parent_id = pm._dlt_id
left join pokemons.abilities_main am on am.name = pa.ability__name
left join pokemons.abilities_main__effect_entries ee on ee._dlt_parent_id = am._dlt_id
where ee.language__name = 'en'