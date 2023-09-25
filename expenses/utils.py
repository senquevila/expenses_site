from datetime import datetime
from django.db.models import F
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
        print(str_date, format)
        try:
            return datetime.strptime(str_date, format).date()
        except ValueError:
            print("Invalid date format")
            #pass

    raise ValueError("Invalid date")
