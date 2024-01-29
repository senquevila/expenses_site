from django.http import JsonResponse

from rest_framework.views import APIView

from expenses.models import Account
from budgets.models import MatchAccount


class ExpenseNotIncludedView(APIView):
    def get(self, request):
        accounts = Account.objects.exclude(
            id__in=MatchAccount.objects.values_list("account__id", flat=True)
        ).values("name", "sign", "parent__name")
        return JsonResponse(list(accounts), safe=False)
