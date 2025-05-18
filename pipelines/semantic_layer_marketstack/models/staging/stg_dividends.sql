{{ config(materialized='view') }}

SELECT * exclude(_dlt_id,_dlt_parent_id,_dlt_list_idx) FROM marketstack_data.dividends__data