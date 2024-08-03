from typing import Optional, Union, Tuple, List, Dict
import re
from datetime import datetime
import pandas as pd
import requests  # type: ignore

from sovai.api_config import ApiConfig
from sovai.errors.sovai_errors import InvalidInputData
from sovai.utils.converter import convert_data2df
from sovai.utils.stream import stream_data, stream_data_pyarrow
from sovai.utils.datetime_formats import datetime_format
from sovai.utils.plot import plotting_data
from sovai.utils.client_side import client_side_frame

from sovai.extensions.pandas_extensions import CustomDataFrame

import pandas as pd
import polars as pl

import boto3
from io import BytesIO
import json

# from fastapi import HTTPException
import pyarrow.parquet as pq
import time
import hashlib
import json
import numpy as np

# client_side_frame is the one for very quick public files.

# Now you can call the method directly on any DataFrame with a 'date' index and 'prediction' column
# df_breakout.get_latest()


# Wall time: 2min 14s (pyarrow via fastapi)
# Wall time: 1min 38s (pandas via fastapi)
# Wall time: 50s (direct via gcp)


## This is not in use
def load_df_from_wasabi(bucket_name, file_name, access_key, secret_key):
    """
    Load a Parquet file from a Wasabi bucket into a pandas DataFrame.

    Args:
    bucket_name (str): Name of the Wasabi bucket.
    file_name (str): Name of the file in the bucket.
    access_key (str): Wasabi access key.
    secret_key (str): Wasabi secret key.

    Returns:
    pandas.DataFrame: DataFrame loaded from the Parquet file.
    """

    # Set up Boto3 client
    s3_client = boto3.client(
        "s3",
        endpoint_url="https://s3.wasabisys.com",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    # Download the file
    parquet_buffer = BytesIO()
    s3_client.download_fileobj(bucket_name, file_name, parquet_buffer)
    parquet_buffer.seek(0)

    return pq.read_table(source=parquet_buffer).to_pandas()


def is_all(tickers):
    # Include "" in the pattern list
    PATTERN = ["ENTIRE", "ALL", "FULL", ""]

    # Return False if tickers is None
    if tickers is None:
        return False

    # Check if tickers is a string and not a list, then convert it to a list
    if isinstance(tickers, str):
        tickers = [tickers]

    # Check if any ticker matches the pattern
    return any(ticker.upper() in PATTERN for ticker in tickers)


import pandas as pd
import polars as pl
from typing import Union


def read_parquet(
    url: str, use_polars: bool = False
) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    Reads a Parquet file into a DataFrame using Pandas or Polars.

    :param url: URL or file path of the Parquet file.
    :param use_polars: If True, use Polars to read the file; otherwise, use Pandas.
    :return: DataFrame loaded from the Parquet file.
    """
    if use_polars:
        return pl.read_parquet(url)
    else:
        return CustomDataFrame(pd.read_parquet(url))


# Global cache
_query_cache = {}

### |||||||||||||||||| VERY IMPORTANT, IF HAVE FULL DATAFRAME ADD THE PATH HERE |||||||||||||||||| ###

## None means no ticker. "" Mean ticker but on parquet for all.

endpoint_to_ticker = {
    "/risks": "",
    "/bankruptcy": "",
    "/bankruptcy/shapleys": "",
    "/bankruptcy/description": "",
    "/corprisk/accounting": "",
    "/corprisk/events": "",
    "/corprisk/misstatement": "",
    "/corprisk/risks": "",
    "/bankruptcy/risks": "",
    "/breakout": "",
    "/breakout/median": "",
    "/institutional/trading": "",
    "/institutional/flow_prediction": "",
    "/news/daily": "",
    "/news/match_quality": "",
    "/news/match_quality": "",
    "/news/within_article": "",
    "/news/relevance": "",
    "/news/magnitude": "",
    "/news/sentiment": "",
    "/news/article_count": "",
    "/news/associated_people": "",
    "/news/associated_companies": "",
    "/news/tone": "",
    "/news/positive": "",
    "/news/negative": "",
    "/news/polarity": "",
    "/news/activeness": "",
    "/news/pronouns": "",
    "/news/word_count": "",
    "/news/sentiment_score": None,
    "/insider/trading": "",
    "/wikipedia/views": "",
    "/spending/contracts": "",
    "/spending/details": "",
    "/spending/transactions": "",
    "/spending/products": "",
    "/spending/location": "",
    "/spending/compensation": "",
    "/spending/competition": "",
    "/spending/entities": "",
    "/accounting/weekly": "",
    "/visa/h1b": "",
    "/factors/accounting": "",
    "/factors/alternative": "",
    "/factors/comprehensive": "",
    "/factors/coefficients": "",
    "/factors/standard_errors": "",
    "/factors/t_statistics": "",
    "/factors/model_metrics": "",
    "/ratios/normal": "",
    "/ratios/relative": "",
    "/movies/boxoffice": "",
    "/complaints/private": "",
    "/complaints/public": "",
    "/short/over_shorted": "",
    "/earnings/surprise": "",
    "/market/closeadj": "",
}

## There are give types of file retrievals
# Postgres - SQL
# Large Parquet Wasabi - Via FastaAPI
# Small Parquet Pandas GCP - Via FastaAPI
# Small Parquet Pyarrow GCP - Via FastaAPI (Same speed above)
# Small Parquet GCP Pub - Via FastaAPI (Same speed above) - By far the best


def normalize_endpoint(endpoint):
    return endpoint.strip("/").strip()


client_side_endpoints = {
    "ratios/relative",
    "market/prices",
    "market/closeadj",
    "short/volume",
    "complaints/public",
    "complaints/private",
    "lobbying/public",
}

# In your main function or wherever this logic is implemented:


def get_ticker_from_endpoint(endpoint: str, tickers, endpoint_to_ticker_map):
    """
    Returns the appropriate ticker value based on the endpoint and tickers.

    :param endpoint: The endpoint string.
    :param tickers: The current tickers value.
    :param endpoint_to_ticker_map: A dictionary mapping endpoints to ticker values.
    :return: The ticker value from the map if the endpoint is found and tickers is None or False, otherwise the original tickers.
    """
    if tickers is None or tickers is False:
        # Check if the endpoint is in the map and return its value, else return the original tickers
        return endpoint_to_ticker_map.get(endpoint, tickers)
    return tickers


class VerboseMode:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def vprint(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)

    def toggle_verbose(self, verbose=None):
        if verbose is None:
            self.verbose = not self.verbose
        else:
            self.verbose = verbose


verbose_mode = VerboseMode()


def print_tickers_value(tickers):
    if tickers is None:
        verbose_mode.vprint("tickers is None")
    elif tickers is False:
        verbose_mode.vprint("tickers is False")
    else:
        verbose_mode.vprint(f"tickers is: {tickers}")


def map_synonyms(params):
    synonym_mapping = {
        "start": "start_date",
        "from_date": "start_date",
        "end": "end_date",
        "to_date": "end_date",
        "ticker": "tickers",
        "symbol": "tickers",
        "columns_name": "columns",
        "col": "columns",
        "cols": "columns",
    }

    return {synonym_mapping.get(key, key): value for key, value in params.items()}


def data(
    endpoint: str,
    tickers: Union[str, list] = None,
    chart: str = None,
    columns: str = None,
    version: str = None,
    start_date: str = None,
    end_date: str = None,
    # predict: bool = False,
    plot: bool = False,
    limit: int = None,
    params: dict = None,
    body: dict = None,
    use_polars: bool = False,
    purge_cache: bool = False,
    parquet: bool = True,
    frequency: str = None,
    verbose: bool = False,
    # **kwargs,                  ## kwargs if you want to allow for random
) -> pd.DataFrame:
    verbose_mode.toggle_verbose(verbose)

    params = params or {}
    # params.update(kwargs)
    params = map_synonyms(params)

    params.update(
        _prepare_params(
            tickers=params.get("tickers", tickers),
            chart=params.get("chart", chart),
            version=params.get("version", version),
            from_date=params.get("start_date", start_date),
            to_date=params.get("end_date", end_date),
            limit=params.get("limit", limit),
            # predict=params.get('predict', predict),
            columns=params.get("columns", columns),
            parquet=params.get("parquet", parquet),
            frequency=params.get("frequency", frequency),
        )
    )
    endpoint, params = _prepare_endpoint(endpoint, params)
    # print(endpoint)
    verbose_mode.vprint(endpoint)
    params = params or None
    headers = {"Authorization": f"Bearer {ApiConfig.token}"}
    url = ApiConfig.base_url + endpoint

    verbose_mode.vprint(f"Requesting URL: {url} with params: {params}")

    # Create a unique cache key
    cache_key = hashlib.sha256(
        json.dumps([url, params], sort_keys=True).encode()
    ).hexdigest()

    # Check if the result is already in the cache
    # Purge cache if requested
    if purge_cache and cache_key in _query_cache:
        del _query_cache[cache_key]
        verbose_mode.vprint("Cache entry purged.")

    # Check if the result is already in the cache
    if not purge_cache and cache_key in _query_cache:
        verbose_mode.vprint("Returning cached data")
        return _query_cache[cache_key]

    # print(endpoint)
    # print(client_side_endpoints)
    # print(tickers)
    # print(frequency)

    normalized_endpoint = normalize_endpoint(endpoint)

    if (
        normalized_endpoint in client_side_endpoints
        and tickers is not None
        and frequency is None
    ):
        verbose_mode.vprint("Grabbing client side")
        _query_cache[cache_key] = client_side_frame(
            normalized_endpoint, tickers, columns, start_date, end_date
        )
        return _query_cache[cache_key]

    try:
        res = requests.get(
            url=url,
            headers=headers,
            data=body,
            params=params,
            stream=True,
            verify=ApiConfig.verify_ssl,
        )
        res.raise_for_status()
        verbose_mode.vprint(f"Response Status: {res.status_code}")
        verbose_mode.vprint(f"Response Content-Type: {res.headers.get('content-type')}")

        print_tickers_value(tickers)

        verbose_mode.vprint(params)

        tickers = get_ticker_from_endpoint(endpoint, tickers, endpoint_to_ticker)

        print_tickers_value(tickers)

        data_format = res.headers.get("X-Data-Format")
        content_type = res.headers["content-type"]

        if content_type == "application/octet-stream":
            if data_format == "pyarrow":
                verbose_mode.vprint(f"header: {data_format}")
                data = CustomDataFrame(stream_data_pyarrow(res))
            else:
                verbose_mode.vprint(f"header: not pyarrow")
                data = CustomDataFrame(stream_data(res))
            _query_cache[cache_key] = data
            return data

        if is_all(tickers):
            verbose_mode.vprint("All ticker Initialized")
            url = res.text.strip('"')
            verbose_mode.vprint(url, " (download link)")
            data = read_parquet(url, use_polars=use_polars)
            _query_cache[cache_key] = data
            return data

        verbose_mode.vprint("It reached the DF")
        data = CustomDataFrame(convert_data2df(res.json()))
        _query_cache[cache_key] = data
        verbose_mode.vprint("It passed the DF")

        if plot:
            _draw_graphs(data)
            return None
        return data
    except Exception as err:
        verbose_mode.vprint("An error occurred:", err)
        if res.status_code == 404:
            msg = res.json()
            msg.update({"status_code": 404, "error": err.args[0]})
            raise InvalidInputData(str(msg))
    return None


# def print_tickers_value(tickers):
#     if tickers is None:
#         print("tickers is None")
#     elif tickers is False:
#         print("tickers is False")
#     else:
#         print(f"tickers is: {tickers}")

# # Example usage

# def data(
#     endpoint: str,
#     tickers: Union[str, list, None] = None,
#     chart: Optional[str] = None,
#     columns_name: Optional[str] = None,
#     version: Optional[str] = None,
#     start_date: Optional[str] = None,
#     end_date: Optional[str] = None,
#     predict: bool = False,
#     plot: bool = False,
#     rows: Optional[int] = None,
#     limit: Optional[int] = None,
#     params: Optional[dict] = None,
#     body: Optional[dict] = None,
#     use_polars: bool = False,
#     purge_cache: bool = False,
#     parquet: bool = True,
# ) -> Union[pd.DataFrame, None]:
#     params = params or {}
#     params.update(
#         _prepare_params(
#             tickers=tickers,
#             chart=chart,
#             version=version,
#             from_date=start_date,
#             to_date=end_date,
#             limit=rows or limit,
#             predict=predict,
#             columns=columns_name,
#         )
#     )
#     endpoint, params = _prepare_endpoint(endpoint, params)
#     print(endpoint)
#     params = params or None
#     headers = {"Authorization": f"Bearer {ApiConfig.token}"}
#     url = ApiConfig.base_url + endpoint

#     print(f"Requesting URL: {url} with params: {params}")

# # Create a unique cache key
#     cache_key = hashlib.sha256(json.dumps([url, params], sort_keys=True).encode()).hexdigest()

#     # Check if the result is already in the cache
#     # Purge cache if requested
#     if purge_cache and cache_key in _query_cache:
#         del _query_cache[cache_key]
#         print("Cache entry purged.")

#     # Check if the result is already in the cache
#     if not purge_cache and cache_key in _query_cache:
#         print("Returning cached data")
#         return _query_cache[cache_key]

#     try:
#         res = requests.get(
#             url=url,
#             headers=headers,
#             data=body,
#             params=params,
#             stream=True,
#             verify=ApiConfig.verify_ssl,
#         )
#         res.raise_for_status()
#         print(f"Response Status: {res.status_code}")
#         print(f"Response Content-Type: {res.headers.get('content-type')}")

#         # Print a small part of the response for preview
#         # response_preview = res.text[:2]  # Adjust the number of characters as needed
#         # print(f"Response Preview: {response_preview}")
#         print_tickers_value(tickers)

#         print(params)

#         # print("Before check..")
#         # print(is_all(tickers))
#         # if is_all(tickers):
#         #     response_dict = res.json()
#         #     print("this is loading parquet")
#         #     # Assuming response_dict is a dictionary containing the required keys
#         #     print("Bucket Name:", response_dict["bucket_name"])
#         #     print("File Name:", response_dict["file_name"])
#         #     print("Access Key:", response_dict["access_key"])
#         #     print("Secret Key:", response_dict["secret_key"])

#         #     return load_df_from_wasabi(response_dict["bucket_name"], response_dict["file_name"], response_dict["access_key"], response_dict["secret_key"])

#         tickers = get_ticker_from_endpoint(endpoint, tickers, endpoint_to_ticker)

#         print_tickers_value(tickers)


#         data_format = res.headers.get("X-Data-Format")
#         content_type = res.headers["content-type"]

#         if content_type == "application/octet-stream":
#             if data_format == "pyarrow":
#                 data = CustomDataFrame(stream_data_pyarrow(res))
#             else:
#                 data = CustomDataFrame(stream_data(res))
#             _query_cache[cache_key] = data
#             return data


#         if is_all(tickers):
#             print("All ticker Initialized")
#             url = res.text.strip('"')
#             print(url, " (download link)", )
#             data = read_parquet(url, use_polars=use_polars)
#             _query_cache[cache_key] = data

#             return data


#         print("It reached the DF")
#         data = CustomDataFrame(convert_data2df(res.json()))
#         _query_cache[cache_key] = data
#         print("It passsed the DF")

#         if plot:
#             _draw_graphs(data)
#             return None
#         return data
#     except Exception as err:
#         print("An error occurred:", err)
#         if res.status_code == 404:
#             msg = res.json()
#             msg.update({"status_code": 404, "error": err.args[0]})
#             raise InvalidInputData(str(msg))
#     return None


# def _prepare_params(**kwargs):
#     finish_params = {}
#     if isinstance(kwargs["tickers"], list):
#         kwargs["tickers"] = ",".join(kwargs["tickers"])
#     if isinstance(kwargs["columns"], list):
#         kwargs["columns"] = ",".join(kwargs["columns"])
#     for server_param, client_param in kwargs.items():
#         if client_param:
#             finish_params[server_param] = str(client_param)

#     return finish_params


def _prepare_params(**kwargs):
    finish_params = {}

    if isinstance(kwargs["tickers"], list):
        kwargs["tickers"] = ",".join(kwargs["tickers"])

    if isinstance(kwargs["columns"], list):
        kwargs["columns"] = ",".join(kwargs["columns"])

    for server_param, client_param in kwargs.items():
        if client_param is not None:
            finish_params[server_param] = str(client_param)

    return finish_params


def _prepare_endpoint(endpoint: str, params: dict) -> Tuple[str, dict]:
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    endpoint_params_key = re.findall(r"\{(.*?)\}", endpoint)
    endpoint_params = {
        key: value for key, value in params.items() if key in endpoint_params_key
    }
    other_params = {
        key: value for key, value in params.items() if key not in endpoint_params_key
    }
    _uniform_datetime_params(other_params)
    if endpoint_params:
        endpoint = endpoint.format(**endpoint_params)
    return endpoint.lower(), other_params


def _uniform_datetime_params(datetime_params: dict[str, str]):
    for key, val in datetime_params.items():
        if "date" in key.lower():
            for _format in datetime_format:
                try:
                    origin_datetime = datetime.strptime(val, _format)
                    datetime_params[key] = origin_datetime.strftime(datetime_format[0])
                    break
                except ValueError:
                    continue
        else:
            datetime_params[key] = val


def _draw_graphs(data: Union[Dict, List[Dict]]):
    if isinstance(data, list):
        for plot in data:
            for _, val in plot.items():
                plotting_data(val)
                break
    else:
        for _, val in data.items():
            plotting_data(val)
            break
