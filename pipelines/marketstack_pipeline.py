import os
import dlt
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://api.marketstack.com/v2/"
TICKERS = ["AAPL", "SHOP", "NVDA", "COIN", "TSLA", "INTC", "AMZN"]


@dlt.resource(table_name="tickers")
def get_tickers():
    for ticker in TICKERS:
        url = BASE_URL + f"tickers/{ticker}?access_key={os.getenv('MARKETSTACK_API')}"
        response = requests.get(url)
        assert response.status_code == 200, "Invalid request: " + response.text
        yield response.json()


@dlt.resource(table_name="historical_data")
def get_historical_data():
    for ticker in TICKERS:
        url = f"{BASE_URL}eod?access_key={os.getenv('MARKETSTACK_API')}&symbols={ticker}&date_from=2024-12-10&date_to=2025-05-18"
        response = requests.get(url)
        assert response.status_code == 200, response.text
        yield response.json()


@dlt.resource(table_name="dividends")
def get_dividends():
    for ticker in TICKERS:
        url = f"{BASE_URL}dividends?access_key={os.getenv('MARKETSTACK_API')}&symbols={ticker}"
        response = requests.get(url)
        assert response.status_code == 200, response.text
        yield response.json()


if __name__ == "__main__":

    pipeline = dlt.pipeline(
        pipeline_name="thesis_pipeline",
        destination="duckdb",
        dataset_name="marketstack_data"
    )

    print("Get tickers...")
    info = pipeline.run(get_tickers)
    print(info)

    print("Get historical data...")
    info = pipeline.run(get_historical_data)
    print(info)

    print("Get dividends data...")
    info = pipeline.run(get_dividends)
    print(info)

    dataset = pipeline.dataset().tickers
    print(dataset.df())
