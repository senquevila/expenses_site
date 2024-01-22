import csv
import requests

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    ListView,
    UpdateView,
)

from expenses.forms import ExpenseUploadForm, ExpenseForm
from expenses.models import (
    Account,
    Currency,
    Expense,
    Period,
    Upload,
)
from expenses.serializers import ExpenseSerializer
from expenses.utils import (
    change_account_from_assoc,
    get_total_local_amount,
    str_to_date,
)

DATE_FIELD = 0
DESCRIPTION_FIELD = 1
AMOUNT_FIELD = 2
ACCOUNT_FIELD = 3


class ExpenseUploadView(FormView):
    template_name = "expenses/expense_upload.html"
    form_class = ExpenseUploadForm
    success_url = reverse_lazy("expense-upload-process")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        file = form.cleaned_data["file"]

        if file:
            context = {}
            self.process_csv(file=file, context=context)
            return render(self.request, 'expenses/expense_upload_result.html', context)
        else:
            form.add_error(None, "File empty")

    def process_csv(self, file, context):
        context["result"] = {}
        self._set_defaults()

        decoded_file = file.read().decode('utf-8-sig').splitlines()
        csv_reader = csv.reader(decoded_file)

        # save the file upload
        upload = Upload()
        upload.file = file
        upload.lines = len(decoded_file)
        upload.save()

        lines = 0
        created = 0
        for row in csv_reader:
            lines += 1

            if lines == 1:  # Avoid the header
                continue

            print(f"Line: {lines} - {row}")
            row = self._clear_row(row)

            payment_date = self._get_payment_date(row[DATE_FIELD])
            period = Period.get_period_from_date(payment_date)

            if not period:
                context["result"][lines] = "Period not found for the payment date"
                continue

            if period.closed:
                context["result"][lines] = "Error: Period is closed"
                continue

            amount, currency = self._get_amount(row)

            if amount == 0:
                context["result"][lines] = "Amount zero"
                continue

            account = self._get_account(row)

            if Expense.objects.filter(
                period=period,
                currency=currency,
                description=row[1],
                amount=amount,
            ).exists():
                context["result"][lines] = "Expense already exists"
                continue

            serializer = ExpenseSerializer(
                data={
                    "payment_date": payment_date,
                    "description": row[DESCRIPTION_FIELD],
                    "period": period.pk,
                    "account": account.pk,
                    "currency": currency.pk,
                    "amount": amount,
                    "upload": upload.pk,
                }
            )
            if serializer.is_valid():
                serializer.save()
                created += 1
            else:
                context["result"][lines] = str(serializer.errors)

        context["summary"] = {
            "saved": created,
            "total": upload.lines,
        }

        from pprint import pprint
        pprint(context)

        change_account_from_assoc()

    def _set_defaults(self):
        # get the default values
        self.default_currency = Currency.objects.filter(
            alpha3=settings.DEFAULT_CURRENCY
        ).first()
        self.default_account = Account.objects.filter(
            name=settings.DEFAULT_ACCOUNT
        ).first()

        if not self.default_currency:
            raise ValueError("Default currency not configured")

        if not self.default_account:
            raise ValueError("Default account not configured")

        # get the actual currency convertion
        '''if not CurrencyConvert.objects.filter(
            date=date.today(), currency__alpha3="USD"
        ).exists():
            self._post_convert_dollars()'''

    def _clear_row(self, row: list):
        return [str(item).strip() for item in row]

    def _post_convert_dollars(self):
        url = self.request.build_absolute_uri(reverse("create-dollar-convert"))
        requests.post(url, headers={"Content-Type": "application/json"})

    def _get_account(self, values: list):
        try:
            value = values[ACCOUNT_FIELD]
        except IndexError:
            return self.default_account

        account_q = Account.objects.filter(name=value)

        if account_q.exists():
            return account_q.first()

        return self.default_account

    def _get_amount(self, values: list) -> tuple:
        """
        Asumming that the value is: [number currency]
        """
        try:
            value = values[AMOUNT_FIELD]
        except IndexError:
            return (0, self.default_currency)

        money = value.split(" ")
        try:
            amount = float(money[0].replace(",", ""))
        except (IndexError, ValueError) as e:
            amount = 0

        try:
            code_currency = money[1]
        except IndexError:
            code_currency = None

        currency_q = Currency.objects.filter(alpha3=code_currency)
        if currency_q.exists():
            currency = currency_q.first()
        else:
            currency = self.default_currency

        return (amount, currency)

    def _get_payment_date(self, value: str):
        payment_date = str_to_date(value)

        if not payment_date:
            payment_date = timezone.now().date()

        return payment_date


class ExpenseGroupListView(ListView):
    model = Expense
    template_name = "expenses/expense_group.html"
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


class ExpenseListPerAccountView(ListView):
    model = Expense
    template_name = "expenses/expense_per_account_list.html"
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


class ExpenseListView(ListView):
    model = Expense
    template_name = "expenses/expense_list.html"
    context_object_name = "expenses"
    paginate_by = 12
    ordering = ["-period", "-payment_date"]

    def get_context_data(self, **kwargs):
        context = super(ExpenseListView, self).get_context_data(**kwargs)
        expenses = Expense.objects.all()
        paginator = Paginator(expenses, self.paginate_by)

        page = self.request.GET.get("page")

        try:
            expenses = paginator.page(page)
        except PageNotAnInteger:
            expenses = paginator.page(1)
        except EmptyPage:
            expenses = paginator.page(paginator.num_pages)

        context["expenses"] = expenses
        return context


class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_form.html"
    success_url = reverse_lazy("expense-list")


class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_form.html"
    success_url = reverse_lazy("expense-list")


class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = "expenses/expense_confirm_delete.html"
    success_url = reverse_lazy("expense-list")
