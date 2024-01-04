from decimal import Decimal

from datetime import datetime
from django.db.models import F, Sum
from django.db.models.functions import Abs

from expenses.models import Expense, CurrencyConvert


def get_real_amount(expense: Expense) -> float:
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
    queryset = Expense.objects.filter(filtered).aggregate(
        total=Sum("local_amount")
    )
    return queryset["total"] or 0