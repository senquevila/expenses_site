from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from rest_framework.views import APIView

from expenses.models import CurrencyConvert
from expenses.utils.tools import create_dollar_conversion


class CurrencyConvertListView(ListView):
    model = CurrencyConvert
    template_name = "expenses/currency_convert_list.html"
    context_object_name = "currency_converts"
    ordering = ["-date"]


class CreateDollarConversionView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy("currency-convert-list"))
