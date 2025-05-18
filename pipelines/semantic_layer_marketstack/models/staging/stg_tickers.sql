{{ config(materialized='view') }}

SELECT * exclude(_dlt_id, _dlt_load_id) FROM marketstack_data.tickers