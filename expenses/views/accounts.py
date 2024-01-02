from django.views.generic import ListView

from expenses.models import Account


class AccountListView(ListView):
    model = Account
    template_name = "accounts/list.html"
    context_object_name = "accounts"
    ordering = ["name"]