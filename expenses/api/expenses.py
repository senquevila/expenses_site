# django imports
from django.db.models import Sum
from django.shortcuts import get_object_or_404

# drf imports
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response

# models import
from expenses.models import Account, Expense, Period
from expenses.serializers import AccountSerializer, ExpenseSerializer
from expenses.utils import get_real_amount


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class ExpenseSummaryListView(APIView):
    def get(self, request, *args, **kwargs):
        _period = get_object_or_404(Period, pk=kwargs.get("period"))

        expenses = (
            Expense.objects.filter(period=_period)
            .annotate(total_amount=Sum("amount"))
            .only("period", "account")
            .order_by("account__name")
        )

        # transform data
        data = {"total": 0, "content": []}
        content = {}
        for expense in expenses:
            value = round(get_real_amount(expense), 2)
            data["total"] += value
            if expense.account.name not in content:
                content[expense.account.name] = {
                    "period": str(expense.period),
                    "account": expense.account.name,
                    "total_amount": value,
                }
            else:
                content[expense.account.name]["total_amount"] = (
                    content[expense.account.name].get("total_amount", 0) + value
                )

        data["content"] = list(content.values())

        return Response(data=data, status=status.HTTP_200_OK)


class SwapAccountView(APIView):
    def post(self, request, *args, **kwargs):
        account_origin = get_object_or_404(
            Account, pk=request.data.get("account_origin")
        )
        account_destination = get_object_or_404(
            Account, pk=request.data.get("account_destination")
        )

        if account_origin.id == account_destination.id:
            return Response(
                {"desciption": "Accounts are the same"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # change expenses from account_origin to account_destination
        Expense.objects.filter(account=account_origin).update(
            account=account_destination
        )
        # remove account_origin
        Account.objects.filter(account=account_origin).delete()
        return Response(status=status.HTTP_200_OK)
