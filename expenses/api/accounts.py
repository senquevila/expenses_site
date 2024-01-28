from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.views import APIView

from expenses.models import Account
from expenses.utils import change_account_from_assoc
from expenses.serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountAssociationView(APIView):
    def post(self, request, *args, **kwargs):
        data = change_account_from_assoc()
        return JsonResponse(data=data, safe=False)
