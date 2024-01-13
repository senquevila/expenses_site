from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse

from rest_framework.views import APIView

from expenses.utils import change_account_from_assoc


class AccountAssociationView(APIView):
    def post(self, request, *args, **kwargs):
        data = change_account_from_assoc()
        return JsonResponse(data=data, safe=False)
