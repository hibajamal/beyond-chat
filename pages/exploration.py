import streamlit as st
import pandas as pd
import dlt
import helpers
import altair as alt
import json
import re

# ------------------- APP CONFIG -------------------
st.set_page_config(page_title="Beyond Chat - Explore", layout="wide")
st.markdown("""
    <style>
        .block-container {
            padding-top: 5rem;
            padding-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)
#st.title("Exploration")
# ------------------- SESSION STATE SETUP -------------------
st.session_state['current_bot'] = 'Exploration'

if 'dataset_info' not in st.session_state:
    st.session_state['dataset_info'] = {
        'name': None,
        'schema': pd.DataFrame(),
        'preview_rows': pd.DataFrame(),
        'loaded': False
    }

# maintaining chat history
if 'messages' not in st.session_state or not st.session_state['messages']:
    st.session_state['messages'] = [
        {"role": "system", "content": f'''
        You are a helpful data analyst that assists with exploring and understanding datasets.

        You answer in two ways, and must choose which option is appropriate given the user's prompt:
        
        1. **Plain text response**: When the question requires general explanation, summarization, or cannot be directly answered with code.
        2. **Python script only**: When the question can be answered with data exploration using DataFrames, visualizations, or filtering logic. In this case:
           - Respond **only with a code block** — no natural language outside it.
           - Include helpful explanations **inside the code as comments**.
           - Use `pandas` and `altair` for analysis and charts.
           - Avoid trivial code like `print()` or placeholders.
           - Always declare and initialize the pipeline object at the top using the dlt.pipeline(...) format.
           - Access data from the relevant table(s) using .df() calls via pipeline.dataset().<table>.df().
           - Perform any data exploration or analysis needed (filtering, aggregating, grouping, plotting, etc.).
           - Store the final result (whether it’s a DataFrame or a chart) in a variable called `result`.
           - If it's a chart (e.g. Altair), store the chart object in `result`.
           - If it's a table, make sure it's a clean Pandas DataFrame, stored in a variable called `result`.
           - Only return a properly formatted Python script, inside a single code block.
        
        You are also an expert on this dataset schema:
        - Dataset name: `{helpers.get_dataset()}`
        - Schema: `{helpers.read_semantic_layer()}`
        - Pipeline name: 'thesis_pipeline'
        
        When answering with code, use the following access pattern:
        
        ```python
        import dlt
        
        pipeline = dlt.pipeline(
            pipeline_name="thesis_pipeline", # always use this param value
            destination="duckdb", # always use this param value
            dataset_name={st.session_state['dataset_info']['dataset_name']} #always use this param value
        )
        ```
        
        Use both your semantic understanding of the schema and general data reasoning to determine the most appropriate response.
                                      '''},
        {"role": "user", "content": "What's in this dataset? Please describe the schema within 200 words."},
    ]
    helpers.gpt_call()


# setting default response
if not st.session_state['chat_history']:
    st.session_state['chat_history'] = [
        {
            'user': "Here's a prompt to start you off with:\n"+st.session_state['messages'][-2]["content"],
            'bot': st.session_state['messages'][-1]["content"]
        }
    ]

if 'last_query_result' not in st.session_state:
    st.session_state['last_query_result'] = None

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


# ------------------- ALTAR CHART RENDERING FUNCTION -------------------
def render_altair_chart(data, x, y, title):
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(x, title=x),
        y=alt.Y(y, title=y)
    ).properties(title=title)
    with st.chat_message("assistant"):
        st.markdown(f"**{title}**")
        st.altair_chart(chart, use_container_width=True)

# ------------------- LAYOUT -------------------
col_chat, col_schema = st.columns([3, 1], gap="large")

# ------------------- CHAT AREA -------------------
with col_chat:
    st.title("💬 Interactive Exploration Console")
    with st.container(border=True):
        with st.container(height=500):
            st.subheader("📜 Chat History")
            for entry in st.session_state['chat_history']:
                if 'user' in entry and entry['user']:
                    with st.chat_message("user"):
                        st.markdown(entry['user'])
                if 'bot' in entry and entry['bot']:
                    with st.chat_message("assistant"):
                        st.markdown(entry['bot'])
                if 'chart' in entry:
                    with st.chat_message("assistant"):
                        if entry['chart']['type'] == 'altair':
                            spec = entry['chart']['spec']
                            st.vega_lite_chart(spec, use_container_width=True)
                            st.session_state['messages'].append({"role": "user", "content": f'''
                            Can you explain the previous question with these results in text:
                            Results: {spec} 
                            '''})
                            print("context updated????")
                            helpers.gpt_call()
                            st.session_state['chat_history'].append({
                                'user': '',
                                'bot': st.session_state['messages'][-1]["content"]
                            })
                if 'dataframe' in entry:
                    with st.chat_message("assistant"):
                        df = pd.DataFrame(entry['dataframe'])
                        st.dataframe(df, use_container_width=True)
                        st.session_state['messages'].append({"role": "user", "content": f'''
                        Can you explain the previous question with these results in text:
                        Results: {df} 
                        '''})
                        helpers.gpt_call()
                        st.session_state['chat_history'].append({
                            'user': '',
                            'bot': st.session_state['messages'][-1]["content"]
                        })

        user_input = st.chat_input("Type your message here...")
        if user_input:
            # Show Input
            st.session_state['chat_history'].append({
                'user': user_input,
                'bot': ''
            })
            # Update messages list
            st.session_state['messages'].append({"role": "user", "content": user_input})
            helpers.gpt_call()
            is_script = False

            if "```python" in st.session_state['messages'][-1]["content"]:
                is_script = True
                script = st.session_state['messages'][-1]["content"].strip("```python").strip("```")
                helpers.execute_script_and_render_result(script)
            else:
                st.session_state['messages'].append({"role": "assistant", "content": st.session_state['messages'][-1]["content"]})

            # Limit to last 10 exchanges plus system prompt
            MAX_HISTORY = 10
            system_prompt = st.session_state['messages'][0]
            recent_messages = st.session_state['messages'][-2 * MAX_HISTORY:]
            st.session_state['messages'] = [system_prompt] + recent_messages

            print(st.session_state['messages'])
            if not is_script:
                st.session_state['chat_history'].append({
                    'user': '',
                    'bot': st.session_state['messages'][-1]["content"]
                })
            st.rerun()

# ------------------- SCHEMA AREA -------------------
with col_schema:
    top, bottom = st.container(height=448), st.container()

    with top:
        st.markdown("**🗂 Dataset Overview**")
        if st.session_state['dataset_info']['loaded']:
            print(st.session_state['dataset_info']['dataset_name'])
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

    with bottom:
        st.markdown("**💡 Exploration Suggestions:**")
        exploration_suggestion_prompt = '''
        Based on the following:
        - the chat history so far,
        - the dataset schema and its structure,
        - and the semantic definitions of the dataset,
        suggest 3 relevant and **simple** follow-up questions that a data analyst might ask next. Return your response in numbered format using this structure:
        - First question here
        - Second question here
        - Third question here
        '''
        st.session_state['messages'].append({"role": "user", "content": exploration_suggestion_prompt})
        helpers.gpt_call()
        suggestion = st.session_state['messages'][-1]["content"]

        st.markdown(suggestion)
        if len(st.session_state['messages']) > 1:
            st.session_state['messages'].pop()  # remove response from history
            st.session_state['messages'].pop()  # remove question from history


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

