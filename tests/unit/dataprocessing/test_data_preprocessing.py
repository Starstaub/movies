import pytest
import pandas as pd
from pandas._testing import assert_frame_equal

from movies.dataprocessing.data_preprocessing import remove_doubles


@pytest.mark.unit_test
def test_remove_doubles():

    df = pd.DataFrame(
        {
            "genres": [["Mark", "Mark"], ["John"]]
        }
    )
    result = remove_doubles(df, "genres")
    expected = pd.DataFrame(
        {
            "genres": [["Mark"], ["John"]]
        }
    )
    assert_frame_equal(result, expected)
