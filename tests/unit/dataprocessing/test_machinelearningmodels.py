import pytest

import pandas as pd
from pandas._testing import assert_frame_equal

from dataprocessing.machinelearningmodels import (
    get_genres_dummies,
    encode_column, model_df,
)


@pytest.mark.unit_test
def test_get_genres_dummies(ml_df):
    result = get_genres_dummies(ml_df)
    expected = pd.DataFrame(
        {
            "Adventure": [1, 0, 0, 0, 0, 0],
            "Animation": [1, 0, 0, 0, 0, 1],
            "Comedy": [0, 0, 0, 0, 0, 1],
            "Family": [0, 0, 0, 0, 0, 1],
            "Western": [0, 1, 0, 0, 0, 0],
        }
    )
    assert_frame_equal(result, expected)


@pytest.mark.unit_test
def test_encode_column(ml_df):
    result = encode_column(ml_df, pd.DataFrame())
    expected = pd.DataFrame({"certificate": [2, 3, 4, 0, 1, 1]})
    assert_frame_equal(result, expected)


@pytest.mark.unit_test
def test_model_df(ml_df):

    ml_df["imdb_score"] = ["6.8", "5.4", "5.4", "8.1", "9.0", "3.5"]
    result = model_df(ml_df)
    expected = pd.DataFrame(
        {
            "Adventure": [1, 0, 0, 0, 0, 0],
            "Animation": [1, 0, 0, 0, 0, 1],
            "Comedy": [0, 0, 0, 0, 0, 1],
            "Family": [0, 0, 0, 0, 0, 1],
            "Western": [0, 1, 0, 0, 0, 0],
            "certificate": [2, 3, 4, 0, 1, 1],
            "imdb_score": [6.8, 5.4, 5.4, 8.1, 9.0, 3.5]
        }
    )
    assert_frame_equal(result, expected)
