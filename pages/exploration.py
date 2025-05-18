import streamlit as st
import pandas as pd
import dlt
import helpers

# ------------------- APP CONFIG -------------------
st.set_page_config(page_title="Beyond Chat - Explore", layout="wide")
st.title("Exploration")
# ------------------- SESSION STATE SETUP -------------------
st.session_state['current_bot'] = 'Exploration'


if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'models_created' not in st.session_state:
    st.session_state['models_created'] = []

if 'last_query_result' not in st.session_state:
    st.session_state['last_query_result'] = None

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'dataset_info' not in st.session_state:
    st.session_state['dataset_info'] = {
        'name': None,
        'schema': pd.DataFrame(),
        'preview_rows': pd.DataFrame(),
        'loaded': False
    }

# ------------------- LAYOUT -------------------
col_chat, col_schema = st.columns([3, 1], gap="large")

# ------------------- CHAT AREA -------------------
with col_chat:
    st.title("💬 Interactive Exploration Console")
    st.markdown("Use this chat interface to ask questions about your data or explore pipeline operations.")

    with st.container():
        st.subheader("📜 Chat History")
        for entry in st.session_state['chat_history']:
            with st.chat_message("user"):
                st.markdown(entry['user'])
            with st.chat_message("assistant"):
                st.markdown(entry['bot'])

    user_input = st.chat_input("Type your message here...")
    if user_input:
        st.session_state['chat_history'].append({
            'user': user_input,
            'bot': f"You said: {user_input}"
        })
        st.rerun()

# ------------------- SCHEMA AREA -------------------
with col_schema:
    st.header("🗂 Dataset Overview")
    if st.session_state['dataset_info']['loaded']:
        st.markdown(f"**Name:** {st.session_state['dataset_info']['name']}")
        print(helpers.get_dataset())
        st.markdown(f"Saved dataset name: **{helpers.get_dataset()}**")
        schema_df = st.session_state['dataset_info']['schema']
        st.markdown(f"**Number of Columns:** {len(schema_df)}")
        if not schema_df.empty:
            st.dataframe(schema_df, use_container_width=True, hide_index=True)
    else:
        st.info("No dataset loaded. Please return to the homepage to select one.")

# ------------------- SIDE BAR -------------------
with st.sidebar:
    st.header("🧭 BeyondChat")
    st.markdown("---")
    st.markdown("### Modes")
    st.markdown("You can choose one of the following states once a dataset is selected:")
    selected_mode = st.radio("Current Mode", options=["Exploration", "Engineering"], index=0)
    if selected_mode != st.session_state['current_bot']:
        st.session_state['current_bot'] = selected_mode
        if selected_mode == "Engineering":
            st.switch_page("pages/engineering.py")
    st.markdown("---")
    st.markdown("### Status")
    st.markdown(f"**Selected Dataset:** {st.session_state['dataset_info']['name'] if st.session_state['dataset_info']['loaded'] else 'None'}")

