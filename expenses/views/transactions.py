from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from rest_framework.views import APIView

from expenses.forms import TransactionForm, LoanForm, SubscriptionForm
from expenses.models import Transaction, Period, Loan, Subscription
from expenses.utils.tools import get_total_local_amount

DATE_FIELD = 0
DESCRIPTION_FIELD = 1
AMOUNT_FIELD = 2
ACCOUNT_FIELD = 3


class TransactionGroupListView(ListView):
    model = Transaction
    template_name = "expenses/transaction_group.html"
    context_object_name = "expenses"

    def get_queryset(self):
        self.period_id = self.kwargs.get("period")
        self.account_id = self.kwargs.get("account")

        # Filter expenses by the specified period
        queryset = (
            Transaction.objects.filter(period=self.period_id)
            .values("account")
            .annotate(total=Sum("local_amount"))
            .values("account__name", "account__id", "total")
            .order_by("total")
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        period = Period.objects.get(pk=self.period_id)
        context["period"] = str(period)
        context["period_id"] = period.id

        context["total"] = get_total_local_amount(Q(period=period))
        _last = (
            Transaction.objects.filter(period=self.period_id)
            .values("payment_date")
            .order_by("-payment_date")
            .first()
        )
        context["last_trx"] = _last["payment_date"] if _last else None

        return context


class TransactionListView(ListView):
    model = Transaction
    template_name = "expenses/transaction_list.html"
    context_object_name = "expenses"
    paginate_by = 12

    def get_queryset(self) -> QuerySet:
        queryset = Transaction.objects.all().order_by("-payment_date")

        upload_id = self.request.GET.get("upload")
        if upload_id:
            queryset = queryset.filter(upload__id=upload_id)

        period_id = self.request.GET.get("period")
        if period_id:
            queryset = queryset.filter(period__id=period_id)

        account_id = self.request.GET.get("account")
        if account_id:
            queryset = queryset.filter(account__id=account_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get("page")

        try:
            expenses = paginator.page(page)
        except PageNotAnInteger:
            expenses = paginator.page(1)
        except EmptyPage:
            expenses = paginator.page(paginator.num_pages)

        context["expenses"] = expenses
        return context


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "expenses/transaction_add.html"
    success_url = reverse_lazy("transaction-list")


class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "expenses/transaction_add.html"
    success_url = reverse_lazy("transaction-list")


class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = "expenses/transaction_confirm_delete.html"
    success_url = reverse_lazy("transaction-list")


class TransactionRemoveInvalidView(APIView):
    def get(self, request):
        invalid_expenses = Transaction.objects.filter(account__name="Invalido")
        invalid_expenses.delete()
        return redirect("home")


class LoanListView(ListView):
    model = Loan
    template_name = "loans/loan_list.html"
    context_object_name = "loans"
    ordering = ["-is_active", "-monthly_payment"]

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["total"] = Loan.objects.filter(is_active=True).aggregate(
            Sum("monthly_payment")
        )["monthly_payment__sum"]
        return ctx


class SubscriptionListView(ListView):
    model = Subscription
    template_name = "expenses/subscription_list.html"
    context_object_name = "subscriptions"
    ordering = ["-is_active", "-monthly_payment"]

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["total"] = Subscription.objects.filter(is_active=True).aggregate(
            Sum("monthly_payment")
        )["monthly_payment__sum"]
        return ctx


class LoanCreateView(CreateView):
    def get(self, request):
        form = LoanForm()
        return render(request, "expenses/loan_add.html", {"form": form})

    def post(self, request):
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("loan-list")
        return render(request, "expenses/loan_add.html", {"form": form})


class SubscriptionCreateView(CreateView):
    def get(self, request):
        form = SubscriptionForm()
        return render(request, "expenses/subscription_add.html", {"form": form})

    def post(self, request):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("subscription-list")
        return render(request, "expenses/subscription_add.html", {"form": form})
