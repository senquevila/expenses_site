from bs4 import BeautifulSoup
from decimal import Decimal
from datetime import datetime
from urllib.request import Request, urlopen

from django.conf import settings
from django.db.models import F, Sum
from django.db.models.functions import Abs
from rest_framework import status

from expenses.models import AccountAsociation, Currency, CurrencyConvert, Transaction

DOLAR_CODE = "USD"


def get_real_amount(expense: Transaction) -> float:
    data = (
        CurrencyConvert.objects.filter(currency=expense.currency)
        .annotate(date_diff=Abs(F("date") - expense.payment_date))
        .order_by("date_diff")[:1]
    )
    return expense.account.sign * expense.amount * data.first().exchange


def str_to_date(str_date) -> datetime.date:
    valid_formats = ["%Y-%m-%d", "%d/%m/%y", "%d/%m/%Y", "%d-%m-%Y", "%d-%m-%y"]

    for format in valid_formats:
        try:
            return datetime.strptime(str_date, format).date()
        except ValueError:
            pass

    raise ValueError("Invalid date")


def get_total_local_amount(filtered) -> Decimal:
    queryset = Transaction.objects.filter(filtered).aggregate(total=Sum("local_amount"))
    return queryset["total"] or 0


def change_account_from_assoc() -> dict:
    data = []
    assocs = AccountAsociation.objects.only("token", "account")
    for assoc in assocs:
        expenses = Transaction.objects.filter(
            description__icontains=assoc.token, account__name=settings.DEFAULT_ACCOUNT
        )
        for expense in expenses:
            if assoc.account.name == expense.account.name:
                continue

            data.append(
                {
                    "id": expense.id,
                    "expense": expense.description,
                    "account_found": assoc.account.name,
                    "account_original": expense.account.name,
                    "date": expense.payment_date,
                }
            )
            expense.account = assoc.account
            expense.save()

    return data


def remove_invalid_transactions() -> int:
    invalid_expenses = Transaction.objects.filter(account__name="Invalido")
    rows, _ = invalid_expenses.delete()
    return rows


def create_dollar_conversion() -> tuple:
    def _get_exchange() -> float:
        req = Request(settings.SCRAPING_URL, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req)
        soup = BeautifulSoup(page, "html.parser")
        result = soup.find(id=settings.SCRAPING_TAG_ID)
        result_text = result.text.strip()
        tokens = result_text.split(settings.SCRAPING_TOKEN_SPLIT)
        value = float(tokens[-1].strip().replace("L", ""))
        return value

    if not CurrencyConvert.objects.filter(date=datetime.today()).exists():
        try:
            exchange = _get_exchange()
        except Exception:
            return {
                "message": "Problem capturing exchange"
            }, status.HTTP_424_FAILED_DEPENDENCY

        currency = Currency.objects.filter(alpha3=DOLAR_CODE).first()

        CurrencyConvert.objects.create(currency=currency, exchange=exchange)

        return {"message": "Exchange created"}, status.HTTP_201_CREATED

    return {"message": "Exchange already exists"}, status.HTTP_204_NO_CONTENT
