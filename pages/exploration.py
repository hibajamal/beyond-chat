import streamlit as st

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

# ------------------- SESSION STATE INIT -------------------
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# ------------------- UI LAYOUT -------------------
st.title("💬 Interactive Exploration Console")
st.markdown("Use this chat interface to ask questions about your data or explore pipeline operations.")

# ------------------- CHAT DISPLAY -------------------
chat_container = st.container()

with chat_container:
    st.subheader("📜 Chat History")
    for entry in st.session_state['chat_history']:
        with st.chat_message("user"):
            st.markdown(entry['user'])
        with st.chat_message("assistant"):
            st.markdown(entry['bot'])

# ------------------- CHAT INPUT -------------------
user_input = st.chat_input("Type your message here...")
if user_input:
    # Echo the message for now
    st.session_state['chat_history'].append({
        'user': user_input,
        'bot': f"You said: {user_input}"
    })
    st.rerun()

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

