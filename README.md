# beyond-chat

Steps to run:
1. Install requirements: `pip install -r requirements.txt`
2. Set up your openai key as `OPENAI_API_KEY` in a .env file. 
3. If you wish to run the pipelines, you will require a marketstack api key, which you can get for free. Once you have it, please also set it in the .env file under `MARKETSTACK_API`.
4. Run the streamlit app: `streamlit run main.py`

In order to have the dlt configuration work, you will have to run all the `..._pipeline.py` files, and then all the `..._modeling.py` files respectively. Then you will be able to seamlessly use the local duckdb destination.  