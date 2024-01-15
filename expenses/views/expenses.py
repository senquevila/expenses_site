import csv
import io
import requests
from datetime import date

from django.db.models import Q, Sum
from django.conf import settings
from django.forms import ValidationError
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, ListView

from expenses.forms import ExpenseFileUploadForm
from expenses.models import (
    Account,
    Currency,
    CurrencyConvert,
    Expense,
    Period,
)
from expenses.serializers import ExpenseSerializer
from expenses.utils import (
    change_account_from_assoc,
    get_total_local_amount,
    str_to_date,
)


class UploadExpenseView(FormView):
    template_name = "expenses/expenses/upload.html"
    form_class = ExpenseFileUploadForm
    success_url = reverse_lazy("home")

    def form_invalid(self, form):
        context = {"form": form}
        return self.render_to_response(context=context)

    def form_valid(self, form):
        file = form.cleaned_data["file"]

        if not CurrencyConvert.objects.filter(
            date=date.today(), currency__alpha3="USD"
        ).exists():
            self._post_convert_dollars(self.request)

        decoded_file = io.TextIOWrapper(file, encoding="utf-8-sig", newline="")
        csv_reader = csv.reader(decoded_file)

        try:
            default_currency = Currency.objects.get(alpha3=settings.DEFAULT_CURRENCY)
        except Currency.DoesNotExist:
            raise ValidationError("Default currency not found")

        try:
            default_account = Account.objects.get(name=settings.DEFAULT_ACCOUNT)
        except Account.DoesNotExist:
            raise ValidationError("Default account not found")

        lines = 0
        for row in csv_reader:
            lines += 1
            print(f"Line: {lines} - {row}")
            row = self._clear_row(row)
            q_account = Account.objects.filter(name=row[3])

            if q_account.exists():
                account = q_account.first()
            else:
                account = self._assoc_accounts(row[2])

            if not account:
                account = default_account
                print("Default account")

            money = row[2].split(" ")
            try:
                amount = float(money[0].replace(",", ""))
            except (IndexError, ValueError) as e:
                print("Error: amount not found")
                continue

            try:
                code_currency = money[1]
            except IndexError as e:
                code_currency = None

            currency = Currency.objects.filter(alpha3=code_currency)
            if not currency.exists():
                print("Warning: using default currency")
                currency = default_currency
            else:
                currency = currency.first()

            payment_date = str_to_date(row[0])
            try:
                period = Period.objects.get(
                    year=payment_date.year, month=payment_date.month
                )
            except Period.DoesNotExist:
                print("Error: Period does not exists")
                continue

            if period.closed:
                print("Error: Period is closed")
                continue

            if not payment_date:
                payment_date = timezone.now().date()

            data = {
                "payment_date": payment_date,
                "description": row[1],
                "period": period.pk,
                "account": account.pk,
                "currency": currency.pk,
                "amount": amount,
            }

            serializer = ExpenseSerializer(data=data)
            if serializer.is_valid():
                expense = serializer.save()
                expense.local_amount = expense.get_local_amount
                expense.save()
                print("Expense saved!!")
            else:
                print(serializer.errors)

        changes = change_account_from_assoc()
        print(changes)
        return super().form_valid(form)

    def _clear_row(self, row: list):
        return [str(item).strip() for item in row]

    def _post_convert_dollars(self):
        url = self.request.build_absolute_uri(reverse("create-dollar-convert"))
        response = requests.post(url, headers={"Content-Type": "application/json"})

        # Check the status of the response
        if response.status_code == 200:
            print("POST request sent successfully")
        else:
            print("Error: Failed to send POST request")


class ExpenseGroupListView(ListView):
    model = Expense
    template_name = "expenses/expenses/group.html"
    context_object_name = "expenses"

    def get_queryset(self):
        self.period_id = self.kwargs.get("period")
        self.account_id = self.kwargs.get("account")

        # Filter expenses by the specified period
        queryset = (
            Expense.objects.filter(period=self.period_id)
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
        return context


class ExpenseListView(ListView):
    model = Expense
    template_name = "expenses/expenses/list.html"
    context_object_name = "expenses"

    def get_queryset(self):
        self.period_id = self.kwargs.get("period")
        self.account_id = self.kwargs.get("account")

        # Filter expenses by the specified period
        queryset = Expense.objects.filter(
            period=self.period_id, account=self.account_id
        ).order_by("local_amount")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        period = Period.objects.get(pk=self.period_id)
        account = Account.objects.get(pk=self.account_id)
        context["period"] = str(period)
        context["account"] = account.name
        context["total"] = get_total_local_amount(Q(period=period, account=account))
        return context
