import streamlit as st


def get_dataset():
    name_ = st.session_state['dataset_info']['name']
    dataset_name = 'marketstack_data'
    if name_.startswith == "Rfam":
        dataset_name = 'rfam_data'
    if name_.startswith == "PokeApi":
        dataset_name = "pokemons"

    return dataset_name

