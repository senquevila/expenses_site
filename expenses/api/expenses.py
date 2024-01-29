# django imports
from django.db.models import Count
from django.shortcuts import get_object_or_404

# drf imports
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response

# models import
from expenses.models import Account, Expense, Upload
from expenses.serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


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


class ExpenseUploadFileCleanupView(APIView):
    def delete(self, request, *args, **kwargs):
        unused_uploads = Upload.objects.annotate(num_expenses=Count("expense")).filter(
            num_expenses=0
        )
        deletes = unused_uploads.count()
        unused_uploads.delete()
        return Response(data={"files-removed": deletes}, status=status.HTTP_200_OK)


class ExpenseDeleteInvalidView(APIView):
    def delete(self, request, *args, **kwargs):
        invalid_expenses = Expense.objects.filter(account__name='Invalido')
        deletes = invalid_expenses.count()
        invalid_expenses.delete()
        return Response(data={"expenses-removed": deletes}, status=status.HTTP_200_OK)