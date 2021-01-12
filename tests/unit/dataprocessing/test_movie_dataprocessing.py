import pytest

from dataprocessing.movie_dataprocessing import (
    define_types,
    clean_release_column,
)


@pytest.mark.unit_test
def test_define_types(release_data):

    expected = ["TV Series", "Video game", "Other", "TV Mini-Series"]

    assert release_data["release"].apply(define_types).tolist() == expected


@pytest.mark.unit_test
def test_clean_release_column(release_data):

    expected = ["1970-1980", "July 10, 2018", "10 December 2019", "2017"]

    assert clean_release_column(release_data, "release")["release"].tolist() == expected
