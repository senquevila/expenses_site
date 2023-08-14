from django.db.models import OuterRef, Subquery, F
from django.db.models.functions import Abs

from expenses.models import Expense, CurrencyConvert


def get_real_amount(expense: Expense) -> float:
    data =  (
        CurrencyConvert.objects.filter(currency=expense.currency)
        .annotate(date_diff=Abs(F("date") - expense.payment_date))
        .order_by("date_diff")[:1]
    )
    return expense.account.sign * expense.amount * data.first().exchange
