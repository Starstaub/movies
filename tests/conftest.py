import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def money_data():
    return pd.DataFrame(
        {
            "budget": ["$120,000,000", "AUD12,345,700", "JPY56,800,855", ""],
            "cum_worldwide_gross": ["$245,899,899", "", "EUR34,500", "$500"],
        }
    )


@pytest.fixture
def release_data():
    return pd.DataFrame(
        {
            "release": [
                "TV Series (1970-1980)",
                "Video game released July 10, 2018",
                "10 December 2019",
                "TV Mini-Series (2017)",
            ]
        }
    )


@pytest.fixture
def ml_df():
    return pd.DataFrame(
        {
            "genres": [
                ["Animation", "Adventure"],
                ["Western"],
                [],
                "",
                np.NaN,
                ["Comedy", "Family", "Animation"],
            ],
            "certificate": ["PG", "PG-R", "R", "", "Not rated", "Not rated"],
        }
    )
