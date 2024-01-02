from django.views.generic import ListView

from expenses.models import Period


class PeriodListView(ListView):
    model = Period
    template_name = "periods/list.html"
    context_object_name = "periods"
    ordering = ["-year", "-month"]

