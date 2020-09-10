import pytest

from movies.dataprocessing.money_dataprocessing import (
    determine_currencies,
    convert_money_columns,
)


@pytest.mark.unit_test
def test_determine_currencies(money_data):

    currency = ["$", "AUD", "JPY", 0.0]
    currency_value = [1.0, 0.73, 0.0094, 0.0]

    assert (
        determine_currencies(money_data, "budget")["currency"].fillna(0.0).tolist()
        == currency
    )
    assert (
        determine_currencies(money_data, "budget")["currency_value"]
        .fillna(0.0)
        .tolist()
        == currency_value
    )


@pytest.mark.unit_test
def test_convert_money_columns(money_data):

    budget = [120000000.0, 9012361.0, 533928.037, 0.0]
    cum_worldwide_gross = [245899899.0, 0.0, 40710.0, 500.0]

    assert (
        convert_money_columns(money_data, "budget")["budget"].fillna(0.0).tolist()
        == budget
    )
    assert (
        convert_money_columns(money_data, "cum_worldwide_gross")["cum_worldwide_gross"]
        .fillna(0.0)
        .tolist()
        == cum_worldwide_gross
    )
