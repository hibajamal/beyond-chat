import dlt

if __name__ == "__main__":
    # perform transformations on the data loaded by dlt
    pipeline = dlt.pipeline(
        pipeline_name='thesis_pipeline',
        destination='duckdb',
        dataset_name='pokemons'
    )

    # get venv for dbt
    venv = dlt.dbt.get_venv(pipeline)

    # get runner
    dbt = dlt.dbt.package(
        pipeline,
        "semantic_layer_pokemon",
        venv=venv
    )

    # run the dbt models
    models = dbt.run_all()

    for m in models:
        print(
            f"Model {m.model_name} materialized" +
            f"in {m.time}" +
            f"with status {m.status}" +
            f"and message {m.message}"
        )