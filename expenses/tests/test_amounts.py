import pytest
from expenses.models import Currency
from expenses.utils.uploads import get_amount


@pytest.fixture
def default_currency(db):
    return Currency.objects.create(alpha3="HNL", name="Lempira")


@pytest.fixture
def setup_currencies(db):
    Currency.objects.create(alpha3="USD", name="Dollars")


@pytest.mark.django_db
def test_get_amount_default_currency(default_currency, setup_currencies):
    row = ["100"]
    amount, currency = get_amount(row, 0, default_currency)
    assert amount == 100.0
    assert currency.alpha3 == "HNL"

    row = ["HNL 100"]
    amount, currency = get_amount(row, 0, default_currency)
    assert amount == 100.0
    assert currency.alpha3 == "HNL"

    row = ["100 HNL"]
    amount, currency = get_amount(row, 0, default_currency)
    assert amount == 100.0
    assert currency.alpha3 == "HNL"


@pytest.mark.django_db
def test_get_amount_default_currency_usd_preffix(default_currency, setup_currencies):
    row = ["USD 100"]
    amount, currency = get_amount(row, 0, default_currency)
    assert amount == 100.0
    assert currency.alpha3 == "USD"

@pytest.mark.django_db
def test_get_amount_default_currency_usd_suffix(default_currency, setup_currencies):
    row = ["100 USD"]
    amount, currency = get_amount(row, 0, default_currency)
    assert amount == 100.0
    assert currency.alpha3 == "USD"

@pytest.mark.django_db
def test_get_amount_default_currency_invalid_index(default_currency, setup_currencies):
    row = ["100 ABC"]
    amount, currency = get_amount(row, -1, default_currency)
    assert amount is None
    assert currency is None

@pytest.mark.django_db
def test_get_amount_default_currency_none(default_currency, setup_currencies):
    row = []
    amount, currency = get_amount(row, 0, default_currency)
    assert amount is None
    assert currency is None


@pytest.mark.django_db
def test_get_amount_default_currency_empty(default_currency, setup_currencies):
    row = ['']
    amount, currency = get_amount(row, 0, default_currency)
    assert amount is None
    assert currency is None


@pytest.mark.django_db
def test_get_amount_default_currency_negative(default_currency, setup_currencies):
    row = ['USD -1.99']
    amount, currency = get_amount(row, 0, default_currency)
    assert amount == -1.99
    assert currency.alpha3 == "USD"
