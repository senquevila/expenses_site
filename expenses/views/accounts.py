from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from expenses.forms import AccountTransferForm
from expenses.models import Account, AccountAsociation, Transaction


class AccountListView(ListView):
    model = Account
    template_name = "expenses/account_list.html"
    context_object_name = "accounts"
    ordering = ["name"]


class AccountTransferView(FormView):
    template_name = "expenses/account_transfer.html"
    form_class = AccountTransferForm

    def get_success_url(self) -> str:
        return reverse("account-list")

    def form_valid(self, form):
        account_origin = form.cleaned_data["account_origin"]
        account_destination = form.cleaned_data["account_destination"]

        # change expenses from account_origin to account_destination
        Transaction.objects.filter(account=account_origin).update(
            account=account_destination
        )

        AccountAsociation.objects.filter(account=account_origin).update(
            account=account_destination
        )

        account_origin.delete()

        return HttpResponseRedirect(self.get_success_url())
