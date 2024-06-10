import hashlib
import json
import re

from django.conf import settings
from django.utils import timezone

from expenses.models import Account, Transaction, Period, Currency, Upload
from expenses.serializers import TransactionSerializer

from expenses.utils.tools import change_account_from_assoc, str_to_date


DATE_FIELD = 0
DESCRIPTION_FIELD = 1
AMOUNT_FIELD = 2
AMOUNT_CURRENCY_FIELD = 3
ACCOUNT_FIELD = 3


def process_bank_csv(upload: Upload):
    context = {"result": {}}
    created = 0

    # get default values
    default_currency, default_account = get_defaults()

    # get the upload metadata
    row_range = upload.parameters["rows"]
    indexes = get_field_indexes(upload.parameters["cols"])

    for row in upload.data[row_range["start"] : row_range["end"]]:
        row = [str(item).strip() for item in row]

        if skip_row(row, indexes):
            continue

        message = {
            "data": context,
            "line_number": row[0],
            "source": row,
        }

        # create identifier
        row_hash = hashlib.sha256("".join(row[1:]).encode()).hexdigest()

        # check if the transaction already exists
        if Transaction.objects.filter(identifier=row_hash).exists():
            message["description"] = "Transaction already exists"
            set_message(**message)
            continue

        payment_date, period = get_payment_date_and_period(row, indexes)
        if not period or period.closed:
            set_message(
                description="Period not found or closed",
                line_number=row[0],
                source=row,
                data=context,
            )
            continue

        # get the amount and local currency
        amount, currency = get_transaction_amount_and_currency(
            row, indexes, default_currency
        )

        if not amount:
            message["description"] = "Amount zero"
            set_message(**message)
            continue

        description = row[indexes["description"]]

        # TODO: temporal
        if Transaction.objects.filter(
            period=period,
            currency=currency,
            description=description,
            amount=amount,
            payment_date=payment_date,
        ).exists():
            message["description"] = "Transaction already exists"
            set_message(**message)
            continue

        serializer = TransactionSerializer(
            data={
                "payment_date": payment_date,
                "description": description,
                "period": period.pk,
                "account": default_account.pk,
                "currency": currency.pk,
                "amount": amount,
                "upload": upload.pk,
                "identifier": row_hash,
            }
        )
        if serializer.is_valid():
            serializer.save()
            created += 1
            message["description"] = "CREATED"
        else:
            message["description"] = str(serializer.errors)
        set_message(**message)

    context["summary"] = {
        "created": created,
        "total": upload.parameters["rows"]["end"] - upload.parameters["rows"]["start"],
    }

    # change the account from the association
    change_account_from_assoc()

    upload.result = json.dumps(context)
    upload.save()


def get_defaults():
    default_currency = Currency.objects.filter(alpha3=settings.DEFAULT_CURRENCY).first()
    if not default_currency:
        raise ValueError("Default currency not configured")
    default_account = Account.objects.filter(name=settings.DEFAULT_ACCOUNT).first()
    if not default_account:
        raise ValueError("Default account not configured")
    return default_currency, default_account


def get_field_indexes(cols):
    return {
        "payment_date": cols[DATE_FIELD]["payment_date"],
        "description": cols[DESCRIPTION_FIELD]["description"],
        "amount": cols[AMOUNT_FIELD]["amount"],
        "amount_currency": cols[AMOUNT_CURRENCY_FIELD]["amount_currency"],
    }


def skip_row(row: list, indexes: list) -> bool:
    return (
        not row
        or not row[indexes["payment_date"]]
        or (not row[indexes["amount"]] and not row[indexes["amount_currency"]])
    )


def get_payment_date_and_period(row, indexes):
    payment_date = str_to_date(row[indexes["payment_date"]]) or timezone.now().date()
    period = Period.get_period_from_date(payment_date)
    return payment_date, period


def get_transaction_amount_and_currency(row, indexes, default_currency):
    amount_1, currency_1 = get_amount(row, indexes["amount"], default_currency)

    if amount_1 is not None and currency_1 is not None:
        amount_2, currency_2 = None, None
    else:
        amount_2, currency_2 = get_amount_currency(
            row, indexes["amount_currency"], default_currency
        )

    if amount_1 is not None and amount_2 is not None:
        if amount_1 >= amount_2:
            return amount_1, currency_1
        else:
            return amount_2, currency_2
    elif amount_1 is not None:
        return amount_1, currency_1
    elif amount_2 is not None:
        return amount_2, currency_2
    else:
        return None, None


def set_message(data: dict, line_number: int, source: str, description: str):
    if line_number not in data["result"]:
        data["result"][line_number] = {}

    data["result"][line_number] = {
        "source": str(source),
        "description": description,
    }


def get_amount(row: list, index: int, default_currency) -> tuple:
    """
    Asumming that the value is: [number currency]
    """
    # check if the index is valid
    if index < 0:
        return None, None

    try:
        value = str(row[index])
    except IndexError:
        return None, None

    # replace weird characters
    value = value.replace("\xa0", " ").replace(",", "")
    amount_str, currency_str = extract_currency_and_value(value)
    try:
        amount = float(amount_str)
    except (IndexError, ValueError, TypeError):
        amount = None

    if not amount:
        return None, None

    currency_str = currency_str or ""
    q_currency = Currency.objects.filter(alpha3=currency_str)
    if q_currency.exists():
        currency = q_currency.first()
    else:
        currency = default_currency

    return (float(amount), currency)


def get_amount_currency(row: list, index: int, default_currency) -> tuple:
    row[index] = "USD " + str(row[index])
    return get_amount(row, index, default_currency)


def extract_currency_and_value(input: str) -> tuple:
    # Updated pattern to handle negative amounts and currency symbol both before and after the value
    pattern = r"(?P<currency1>L|LPS|HNL|USD)?\s*(?P<value>-?\d+(?:\.\d{2})?)\s*(?P<currency2>L|LPS|HNL|USD)?"
    match = re.search(pattern, input)
    if match:
        value = match.group("value")
        # Check if currency1 is present, else fallback to currency2
        currency = match.group("currency1") or match.group("currency2")

        currency_map = {
            "L": "HNL",  # Assuming 'L' stands for Lempira, the currency of Honduras
            "LPS": "HNL",
            "HNL": "HNL",
            "USD": "USD",
        }

        return value, currency_map.get(currency, None)
    else:
        return None, None
