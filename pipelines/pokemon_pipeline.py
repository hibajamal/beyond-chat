import dlt
from dlt.sources.rest_api import rest_api_source
from dlt.sources.helpers.rest_client.paginators import OffsetPaginator
import requests

def extract_id(record):
    print(record)
    record["id"] = record["url"].split("/")[-2]
    return record


def anxiety_logger(record):
    print(record)
    return record


def load_pokemon() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="thesis_pipeline",
        destination="duckdb",
        dataset_name="pokemons",
    )

    pokemon_source = rest_api_source(
        {
            "client": {
                "base_url": "https://pokeapi.co/api/v2/",
                "paginator": OffsetPaginator(
                            limit=60,
                            offset=60,
                            total_path="count"
                ),
            },
            "resources": [
                {
                    "name": "pokemon",
                    "processing_steps": [
                        {"map": extract_id},
                    ],
                },
                {
                    "name": "pokemons_main",
                    "endpoint": {
                        "path": "pokemon/{resources.pokemon.id}",
                    },
                    "processing_steps": [
                        {"map": anxiety_logger},
                    ],
                },
            ],
        }
    )

    load_info = pipeline.run(pokemon_source)
    print(load_info)


def load_pokemon_abilities():
    pipeline = dlt.pipeline(
        pipeline_name="thesis_pipeline",
        destination="duckdb",
        dataset_name="pokemons",
    )

    dataset = pipeline.dataset().pokemons_main__abilities.df()

    @dlt.resource(table_name="abilities_main", write_disposition="merge", primary_key="id")
    def abilities_main(urls):
        for url in urls:
            print(url)
            response = requests.get(url)
            assert response.status_code == 200, "Invalid url: " + url
            yield response.json()

    load_info = pipeline.run(abilities_main(dataset["ability__url"]))
    print(load_info)

if __name__ == "__main__":
    #load_pokemon()
    load_pokemon_abilities()
