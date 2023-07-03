# common imports

# django imports
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import get_object_or_404

# drf imports
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# models import
from expenses.models import Account, Expense
from expenses.serializers import AccountSerializer, ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    @action(detail=False, methods="GET")
    def summary(self, request):
        queryset = self.queryset.values("period", "account").aggregate(
            total_amount=Sum("amount")
        )
        return queryset
