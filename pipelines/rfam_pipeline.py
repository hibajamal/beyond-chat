import dlt
from dlt.sources.sql_database import sql_database


def load_entire_database() -> None:
    # Define the pipeline
    pipeline = dlt.pipeline(
        pipeline_name="thesis_pipeline",
        destination='duckdb',
        dataset_name="rfam_data"
    )

    # Fetch all the tables from the database
    source = sql_database(
        table_names = ["family", "clan", "clan_membership",])

    # Run the pipeline
    info = pipeline.run(source, write_disposition="replace")

    # Print load info
    print(info)


if __name__ == '__main__':
    load_entire_database()
    pipeline = dlt.pipeline(
        pipeline_name="thesis_pipeline",
        destination='duckdb',
        dataset_name="rfam_data"
    )

    dataset = pipeline.dataset().family.df()

    print(dataset)
