import streamlit as st

# ------------------- APP CONFIG -------------------
st.set_page_config(page_title="Beyond Chat - Engineering", layout="wide")
#st.title("Engineering")

# ------------------- SESSION STATE SETUP -------------------
st.session_state['current_bot'] = 'Engineering'

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'models_created' not in st.session_state:
    st.session_state['models_created'] = []

if 'last_query_result' not in st.session_state:
    st.session_state['last_query_result'] = None


with st.sidebar:
    st.header("🧭 BeyondChat")
    st.markdown("---")
    st.markdown("### Modes")
    st.markdown("You can choose one of the following states once a dataset is selected:")
    selected_mode = st.radio("Current Mode", options=["Exploration", "Engineering"], index=1)
    if selected_mode != st.session_state['current_bot']:
        st.session_state['current_bot'] = selected_mode
        if selected_mode == "Exploration":
            st.switch_page("pages/exploration.py")
    st.markdown("---")
    st.markdown("### Status")
    st.markdown(f"**Selected Dataset:** {st.session_state['dataset_info']['name'] if st.session_state['dataset_info']['loaded'] else 'None'}")


