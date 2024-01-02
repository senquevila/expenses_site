from django.views.generic import ListView

from expenses.models import CurrencyConvert


class CurrencyConvertListView(ListView):
    model = CurrencyConvert
    template_name = "currency_convert/list.html"
    context_object_name = "currency_converts"
    ordering = ["-date"]