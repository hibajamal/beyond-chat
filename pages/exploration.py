import streamlit as st
import pandas as pd
import dlt
import helpers

# ------------------- APP CONFIG -------------------
st.set_page_config(page_title="Beyond Chat - Explore", layout="wide")
#st.title("Exploration")
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
    with st.container(border=True):
        with st.container(height=500):
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
        with st.container(border=True):
            with st.container(height=500):
                print(helpers.get_dataset())
                st.markdown(f"Dataset name: **{st.session_state['dataset_info']['dataset_name']}**")
                schema_df = st.session_state['dataset_info']['schema']
                schema = helpers.get_schema()
                for table in schema:
                    with st.expander(f"➕ {table}"):
                        st.dataframe(pd.DataFrame(schema[table]), use_container_width=True, hide_index=True)
                        with st.popover(f"🔍 Preview: {table}"):
                            preview = helpers.get_table_preview(table)
                            st.dataframe(preview, use_container_width=True)
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

