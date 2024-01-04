import csv
from datetime import date
import io
import requests

from django.db.models import Q, Sum
from django.conf import settings
from django.forms import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.views.generic import FormView, ListView

from expenses.forms import ExpenseFileUploadForm
from expenses.models import Account, Currency, CurrencyConvert, Expense, Period
from expenses.utils import str_to_date, get_total_local_amount





class UploadExpenseView(FormView):
    template_name = "expenses/upload.html"
    form_class = ExpenseFileUploadForm
    success_url = "/home/"

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

        default_currency = Currency.objects.filter(alpha3=settings.DEFAULT_CURRENCY)
        if not default_currency.exists():
            raise ValidationError("Default currency not found")

        default_account = Account.objects.filter(name=settings.DEFAULT_ACCOUNT)
        if not default_account.exists():
            raise ValidationError("Default account not found")

        lines = 0
        for row in csv_reader:
            lines += 1
            print(f"Line: {lines}")
            row = self._clear_row(row)
            account = Account.objects.filter(name=row[3])

            if not account.exists():
                account = default_account

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

            payment_date = str_to_date(row[0])
            try:
                period = Period.objects.get(
                    year=payment_date.year, month=payment_date.month
                )
            except Period.DoesNotExist:
                print("Warning: Period does not exists")
                continue

            if period.closed:
                print("Warning: Period closed")
                continue

            if not payment_date:
                payment_date = timezone.now().date()

            expense = Expense(
                payment_date=payment_date,
                description=row[1],
                period=period,
                account=account.first(),
                currency=currency.first(),
                amount=amount,
            )
            expense.local_amount = expense.get_local_amount
            expense.save()
            print("Expense saved!!")

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
            print("Failed to send POST request")


class ExpenseGroupListView(ListView):
    model = Expense
    template_name = "expenses/group.html"
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
    template_name = "expenses/list.html"
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
