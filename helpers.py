import streamlit as st
import duckdb


def get_dataset():
    name_ = st.session_state['dataset_info']['name']
    dataset_name = 'marketstack_data'
    if name_.startswith("Rfam"):
        dataset_name = 'rfam_data'
    if name_.startswith("PokeApi"):
        dataset_name = "pokemons"
    st.session_state['dataset_info']['dataset_name'] = dataset_name
    return st.session_state['dataset_info']['dataset_name']


def get_schema():
    conn = duckdb.connect("pipelines/thesis_pipeline.duckdb")
    df = conn.sql("show all tables").df()
    dataset = df.loc[df['schema'] == st.session_state['dataset_info']['dataset_name']]
    tables = list(dataset['name'])
    columns = list(dataset['column_names'])
    types = list(dataset['column_types'])
    # different dataframes for each table
    object_to_be_returned = {}
    for i, table in enumerate(tables):
        object_to_be_returned[table] = {
                "column_name": columns[i],
                "column_type": types[i]
            }

    conn.close()
    return object_to_be_returned


def get_table_preview(table):
    dataset = st.session_state['dataset_info']['dataset_name']
    conn = duckdb.connect("pipelines/thesis_pipeline.duckdb")
    preview = conn.sql(f"select * from {dataset}.{table} limit 10").df()
    conn.close()
    return preview
