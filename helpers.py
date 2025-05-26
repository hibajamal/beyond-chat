import streamlit as st
import duckdb
import yaml
import openai
import os
from openai import OpenAI
from dotenv import load_dotenv
import altair as alt
import pandas as pd
load_dotenv()

# Set openai.api_key to the OPENAI environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai.api_key)


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


def read_semantic_layer():
    dataset = st.session_state['dataset_info']['dataset_name']
    semantic_dir = "semantic_layer_rfam"
    if "marketstack" in dataset:
        semantic_dir = "semantic_layer_marketstack"
    elif "pokemon" in dataset:
        semantic_dir = "semantic_layer_pokemon"

    path = f"pipelines/{semantic_dir}/models/schema.yml"
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data


def gpt_call(gpt_model="gpt-3.5-turbo"):
    res = client.chat.completions.create(
        model=gpt_model,
        messages=st.session_state['messages'],
        max_tokens=4096,
        temperature=0.7
    )

    response = {"role": "assistant", "content": res.choices[0].message.content.strip()}
    st.session_state['messages'].append(response)


def execute_script_and_render_result(script: str):
    print("correcting script...")
    script = correct_script(script)
    # Step 1: Prepare isolated namespace
    namespace = {}

    # Step 2: Try executing the script
    try:
        exec(script, namespace)
    except Exception as e:
        st.chat_message("assistant").error(f"Execution failed: {e}")
        return

    # Step 3: Check for `result` in the namespace
    result = namespace.get("result", None)

    # Step 4: Render based on result type
    with st.chat_message("assistant"):
        if isinstance(result, pd.DataFrame):
            st.markdown("Here’s the resulting table:")
            st.dataframe(result, use_container_width=True)
        elif isinstance(result, alt.Chart):
            st.markdown("Here’s the resulting chart:")
            st.altair_chart(result, use_container_width=True)
        else:
            st.info("Code executed, but no visualizable `result` was found.")


def correct_script(script, gpt_model="gpt-3.5-turbo"):
    prompt = f'''Can you fix this script according to the following rules:
    
    script: {script}
    
    rules:
           - Store the final result (whether it’s a DataFrame or a chart) in a variable called `result`.
           - If it's a chart (e.g. Altair), store the chart object in `result`.
           - If it's a table, make sure it's a clean Pandas DataFrame, stored in a variable called `result`.
           - Only return a properly formatted Python script, inside a single code block.
    '''
    res = client.chat.completions.create(
        model=gpt_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0.7
    )

    corrected_script = res.choices[0].message.content.strip()
    return corrected_script
