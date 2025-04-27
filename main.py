import streamlit as st
import pandas as pd
import duckdb

# Initialize session state
if 'current_bot' not in st.session_state:
    st.session_state['current_bot'] = 'Exploration'

if 'dataset_info' not in st.session_state:
    st.session_state['dataset_info'] = {
        'name': 'random_dataset',
        'schema': None,
        'preview_rows': None
    }

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'models_created' not in st.session_state:
    st.session_state['models_created'] = []

if 'last_query_result' not in st.session_state:
    st.session_state['last_query_result'] = None

# Create a random DataFrame and load to duckdb
df = pd.DataFrame({
    'customer_id': range(1, 21),
    'sales': [round(x, 2) for x in (1000 * pd.Series(range(1, 21)).apply(lambda x: x + 0.5 * (x % 3)) / 2)],
    'region': ['North', 'South', 'East', 'West'] * 5,
    'signup_date': pd.date_range(start='2023-01-01', periods=20)
})

con = duckdb.connect(database=':memory:')
con.execute("CREATE TABLE random_dataset AS SELECT * FROM df")

# Extract schema info
schema_info = con.execute("DESCRIBE random_dataset").fetchdf()

st.session_state['dataset_info']['schema'] = schema_info
st.session_state['dataset_info']['preview_rows'] = df.head()

# Sidebar
with st.sidebar:
    st.header("🔍 Navigation")
    st.markdown(f"**Active Dataset:** {st.session_state['dataset_info']['name']}")
    st.markdown(f"**Current Mode:** {st.session_state['current_bot']}")

    if st.button("Switch to Exploration"):
        st.session_state['current_bot'] = 'Exploration'
    if st.button("Switch to Engineering"):
        st.session_state['current_bot'] = 'Engineering'

    st.divider()
    st.header("🗂 Dataset Preview")
    st.dataframe(st.session_state['dataset_info']['preview_rows'])

# Main Screen
st.title("Multi-Modal Data Exploration Tool")
st.subheader(f"Mode: {st.session_state['current_bot']}")

# Bot selection
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("Bot 1 (Data Exploration)"):
        st.session_state['current_bot'] = 'Exploration'

with col2:
    if st.button("Bot 2 (Pipeline Master)"):
        st.session_state['current_bot'] = 'Engineering'

# CHAT INPUT SECTION
with col3:
    with st.form(key="chat_form"):
        user_query_temp = st.text_input("Enter your query here:")
        submit_button = st.form_submit_button(label="Submit")

# After user submits
if submit_button and user_query_temp:
    bot_response = f"****{user_query_temp}****"

    st.session_state['chat_history'].append({
        'bot': st.session_state['current_bot'],
        'user_query': user_query_temp,
        'bot_response': bot_response
    })

# Suggestions box
st.subheader("💡 Suggestions")
suggestion_cols = st.columns(3)
with suggestion_cols[0]:
    st.button("Suggestion 1")
with suggestion_cols[1]:
    st.button("Suggestion 2")
with suggestion_cols[2]:
    st.button("Suggestion 3")

st.divider()

# Chat Section
st.subheader("📜 Chat History")
for entry in st.session_state['chat_history']:
    st.markdown(f"**[{entry['bot']}]**: {entry['user_query']}")
    st.markdown(f"**Bot Response:** {entry['bot_response']}")
    st.divider()
