import pytest
import pandas as pd
from pandas._testing import assert_frame_equal

from dataprocessing.data_preprocessing import (
    remove_doubles,
    clean_lists,
    clean_list_columns, clean_dataframe,
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


@pytest.mark.unit_test
def test_clean_dataframe():

    df = pd.DataFrame(
        {
            "duration": ["1h 45min", "30min"],
            "release": ["10 December 2019", "Video game released July 10, 2018"],
            "budget": ["$120,000,000", "AUD12,345,700"],
            "cum_worldwide_gross": ["$245,899,899", ""],
            "stars": [["Ed", "Steve"], ""],
            "genres": [[" Animation", " Family"], ""],
            "plot_keywords": [["pixar"], ["troublesome"]],
            "director": [["John Lasseter"], ""],
            "writer": ["", ["Kenny", "Kenny"]],
            "country": [["USA"], ["Canada"]],
            "creator": ["", ""],
            "certificate": ["Tous Public", "R"],
            "imdb_score": ["8.1", ""],

        })

    df = clean_dataframe(df)
    expected = pd.DataFrame(
        {
            "duration": [105],
            "release": ["10 December 2019"],
            "budget": [120000000.0],
            "cum_worldwide_gross": [245899899.0],
            "stars": [["Ed", "Steve"]],
            "genres": [["Animation", "Family"]],
            "plot_keywords": [["pixar"]],
            "director": [["John Lasseter"]],
            "writer": [[]],
            "country": [["USA"]],
            "creator": [[]],
            "certificate": ["Tous publics"],
            "imdb_score": ["8.1"],
            "type": ["Other"]
        })
    assert_frame_equal(df, expected)
