from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from expenses.models import Expense, Period


class PeriodListView(ListView):
    model = Period
    template_name = "periods/list.html"
    context_object_name = "periods"
    ordering = ["-year", "-month"]


class PeriodCloseView(APIView):
    def get(self, request, pk: int = None):
        try:
            period = Period.objects.get(pk=pk, closed=False)
            period.closed = True
            period.total = self._get_total(period)
            period.save()
        except Period.DoesNotExist:
            messages.error(request=request, message="Period is closed")
        return redirect("period-list")

    def _get_total(self, period: Period) -> float:
        expenses = Expense.objects.filter(period=period)
        return sum(expense.local_amount for expense in expenses)

class PeriodOpenView(APIView):
    def get(self, request, pk:int=None):
        try:
            period = Period.objects.get(pk=pk, closed=True)
            period.closed = False
            period.total = 0
            period.save()
        except Period.DoesNotExist:
            messages.error(request=request, message="Period is already open or not exists")
        return redirect("period-list")