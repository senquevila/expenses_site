from decimal import Decimal
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from expenses.models import Expense, Period


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
