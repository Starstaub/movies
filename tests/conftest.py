import pytest
import pandas as pd


@pytest.fixture
def money_data():
    return pd.DataFrame(
        {
            "budget": ["$120,000,000", "AUD12,345,700", "JPY56,800,855", ""],
            "cum_worldwide_gross": ["$245,899,899", "", "EUR34,500", "$500"],
        }
    )
