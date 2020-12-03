import pytest
import pandas as pd
from pandas._testing import assert_frame_equal

from movies.dataprocessing.data_preprocessing import (
    remove_doubles,
    clean_lists,
    clean_list_columns,
)


@pytest.mark.unit_test
def test_remove_doubles():

    df = pd.DataFrame({"genres": [["Mark", "Mark"], ["John"]]})
    result = remove_doubles(df, "genres")
    expected = pd.DataFrame({"genres": [["Mark"], ["John"]]})
    assert_frame_equal(result, expected)


@pytest.mark.unit_test
def test_clean_lists():

    df = pd.DataFrame(
        {
            "genres": [[" Animation", " Family"], [], [" comedy", " adventure"]],
            "country": [[" USA", " Canada"], [" France"], []],
        }
    )

    df = clean_lists(df, "genres")
    df = clean_lists(df, "country")

    expected = pd.DataFrame(
        {
            "genres": [["Animation", "Family"], [], ["Comedy", "Adventure"]],
            "country": [["USA", "Canada"], ["France"], []],
        }
    )

    assert_frame_equal(df, expected)


@pytest.mark.unit_test
def test_clean_list_columns():

    df = pd.DataFrame(
        {
            "stars": [["Ed", "Steve"], ""],
            "genres": [["Animation", "Family"], ""],
            "plot_keywords": [["pixar"], ["troublesome"]],
            "director": [["John Lasseter"], ""],
            "writer": ["", ["Kenny"]],
            "country": [["USA"], ["Canada"]],
            "creator": ["", ""],
        }
    )

    df = clean_list_columns(df)
    expected = pd.DataFrame(
        {
            "stars": [["Ed", "Steve"], []],
            "genres": [["Animation", "Family"], []],
            "plot_keywords": [["pixar"], ["troublesome"]],
            "director": [["John Lasseter"], []],
            "writer": [[], ["Kenny"]],
            "country": [["USA"], ["Canada"]],
            "creator": [[], []],
        }
    )

    assert_frame_equal(df, expected)
