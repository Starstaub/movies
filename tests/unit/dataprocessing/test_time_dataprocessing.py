import pytest
import pandas as pd

from dataprocessing.time_dataprocessing import format_time_to_minutes


@pytest.mark.unit_test
def test_format_time_to_minutes():

    df = pd.DataFrame({"duration": ["1h 45min", "30min", "2h"]})
    expected = [105, 30, 120]

    assert format_time_to_minutes(df, "duration")["duration"].tolist() == expected
