import time

import streamlit as st
import pandas as pd
import duckdb

# ------------------- APP CONFIG -------------------
st.set_page_config(page_title="Beyond Chat", layout="wide")
st.title("Home")

# ------------------- SESSION STATE SETUP -------------------
if 'current_bot' not in st.session_state:
    st.session_state['current_bot'] = 'Exploration'

if 'dataset_info' not in st.session_state:
    st.session_state['dataset_info'] = {
        'name': None,
        'schema': None,
        'preview_rows': None,
        'loaded': False
    }

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'models_created' not in st.session_state:
    st.session_state['models_created'] = []

if 'last_query_result' not in st.session_state:
    st.session_state['last_query_result'] = None



# ------------------- APP HOMEPAGE UI -------------------
st.title("🧠 Beyond Chat: A Multimodal Exploration Interface")
st.markdown("""
Welcome to the prototype interface for multimodal data exploration. This tool allows you to switch between two modes:
- **Exploration**: Analyze datasets and ask questions
- **Engineering**: Review pipelines, handle data issues, and build clean models

Please begin by selecting one of the available datasets:
""")

# Dummy datasets for selection
available_datasets = ["Rfam: The RNA families database",
                      "Marketstack: Real-Time, Intraday & Historical Market Data",
                      "PokeApi: The RESTful Pokémon API"]
selected_dataset = st.selectbox("📊 Select a dataset to get started:", ["-- Select --"] + available_datasets)

if selected_dataset != "-- Select --":
    # Simulate loading schema and preview (dummy)
    df = pd.DataFrame({
        'col1': range(5),
        'col2': ['A', 'B', 'C', 'D', 'E']
    })
    con = duckdb.connect(database=':memory:')
    con.execute("CREATE TABLE selected_data AS SELECT * FROM df")
    schema_info = con.execute("DESCRIBE selected_data").fetchdf()

    # Save into session
    st.session_state['dataset_info'] = {
        'name': selected_dataset,
        'schema': schema_info,
        'preview_rows': df.head(),
        'loaded': True
    }

    st.success(f"✅ Dataset '{selected_dataset}' selected. Redirecting to explore...")
    time.sleep(2)
    st.switch_page("pages/exploration.py")
else:
    st.info("⬆️ Select a dataset to begin.")

# ------------------- SIDEBAR -------------------
with st.sidebar:
    st.header("🧭 BeyondChat")
    st.markdown("---")
    st.markdown("### Modes")
    st.markdown("You can choose one of the following states once a dataset is selected:")
    selected_mode = st.radio("Current Mode", options=["Exploration", "Engineering"], index=0, disabled=True)
    if selected_mode != st.session_state['current_bot']:
        st.session_state['current_bot'] = selected_mode
        if selected_mode == "Exploration":
            st.switch_page("pages/exploration.py")
        elif selected_mode == "Engineering":
            st.switch_page("pages/engineering.py")
    st.markdown("---")
    st.markdown("### Status")
    st.markdown(f"**Selected Dataset:** {st.session_state['dataset_info']['name'] if st.session_state['dataset_info']['loaded'] else 'None'}")
