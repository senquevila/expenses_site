import csv
import io

from django.conf import settings
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import FormView, ListView
from rest_framework import status
from rest_framework.response import Response

from expenses.forms import ExpenseFileUploadForm
from expenses.models import Account, Currency, Expense
from expenses.utils import transform_string_to_date


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request=request, template_name="expenses/home.html")


class UploadExpenseView(FormView):
    template_name = "expenses/upload_form.html"
    form_class = ExpenseFileUploadForm
    success_url = "/expenses/"

    def form_invalid(self, form):
        context = {'form': form}
        return self.render_to_response(context=context)

    def form_valid(self, form):
        period = form.cleaned_data["period"]
        file = form.cleaned_data["file"]

        print("DEFAULT_CURRENCY:", settings.DEFAULT_CURRENCY)
        print("DEFAULT_ACCOUNT:", settings.DEFAULT_ACCOUNT)

        decoded_file = io.TextIOWrapper(file, encoding="utf-8", newline="")
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
            row = self._clear_row(row)
            print(row)

            account = Account.objects.filter(name=row[3])

            if not account.exists():
                account = default_account

            money = row[2].split(" ")
            try:
                amount = float(money[0].replace(",", ""))
            except (IndexError, ValueError) as e:
                continue

            try:
                code_currency = money[1]
            except (IndexError) as e:
                code_currency = None

            currency = Currency.objects.filter(alpha3=code_currency)
            if not currency.exists():
                currency = default_currency

            payment_date = transform_string_to_date(row[0])
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
            expense.save()

        return super().form_valid(form)

    def _clear_row(self, row: list):
        return [str(item).strip() for item in row]


class ExpenseListView(ListView):
    model = Expense
    template_name = "expenses/list.html"
    context_object_name = "expenses"
    ordering = ["-created"]
