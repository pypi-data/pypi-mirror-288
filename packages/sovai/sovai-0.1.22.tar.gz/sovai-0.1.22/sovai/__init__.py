"""
Main SovAI SDK Tool Kit package
"""

from .api_config import read_key, save_key
from .api_config import ApiConfig
from .get_data import data
from .get_plots import plot
from .get_reports import report
from .get_compute import compute

from .basic_auth import basic_auth
from .token_auth import token_auth
from .studies.nowcasting import nowcast

from .extensions.pandas_extensions import CustomDataFrame as extension


from .utils.file_management import save_or_update_tickers


# Call the function to ensure tickers data is up-to-date
save_or_update_tickers()


__version__ = "0.1.25"
