# django imports
from django.db.models import Count

# drf imports
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response

# models import
from expenses.models import Transaction, Upload
from expenses.serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionUploadFileCleanupView(APIView):
    def delete(self, request, *args, **kwargs):
        unused_uploads = Upload.objects.annotate(num_expenses=Count("expense")).filter(
            num_expenses=0
        )
        deletes = unused_uploads.count()
        unused_uploads.delete()
        return Response(data={"files-removed": deletes}, status=status.HTTP_200_OK)


class TransactionDeleteInvalidView(APIView):
    def delete(self, request, *args, **kwargs):
        invalid_expenses = Transaction.objects.filter(account__name="Invalido")
        deletes = invalid_expenses.count()
        invalid_expenses.delete()
        return Response(data={"transaction-removed": deletes}, status=status.HTTP_200_OK)
