from django.contrib import admin, messages
from django.db.models import Count

from expenses.models import (
    Account,
    AccountAsociation,
    Currency,
    CurrencyConvert,
    Expense,
    Period,
    Upload,
)

from expenses.utils import change_account_from_assoc


def disabled_periods(PeriodAdmin, request, queryset):
    queryset.update(active=False)
    updates = queryset.count()
    messages.success(request=request, message=f"Disabled {updates} periods")


disabled_periods.short_description = "Disabled selected periods"


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    ordering = ["-year", "-month"]
    actions = [disabled_periods]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(CurrencyConvert)
class CurrencyConvertAdmin(admin.ModelAdmin):
    pass


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    ordering = ["name", "account_type"]


def remove_invalid_expenses(ExpenseAdmin, request, queryset):
    invalid_expenses = Expense.objects.filter(account__name="Invalido")
    deletes = invalid_expenses.count()
    invalid_expenses.delete()
    messages.success(request=request, message=f"Removed {deletes} invalid expenses")


remove_invalid_expenses.short_description = "Removed all the invalid expenses"


def assoc_default_account(ExpenseAdmin, request, queryset):
    changes = change_account_from_assoc()
    messages.success(
        request=request, message=f"Associated {len(changes)} expenses with Default account"
    )


assoc_default_account.short_description = "Associate expenses from default account"


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "period",
        "description",
        "currency",
        "amount",
        "local_amount",
        "account_name",
        "payment_date",
        "upload",
        "created",
    )
    list_filter = (
        "period",
        "created",
        "currency",
        "account",
        "upload",
    )
    ordering = (
        "-payment_date",
        "-created",
    )
    search_fields = (
        "description__icontains",
        "account__name__icontains",
        "amount",
    )
    actions = [remove_invalid_expenses, assoc_default_account]

    def account_name(self, obj):
        return obj.account.name

    account_name.short_description = "Account Name"


@admin.register(AccountAsociation)
class AccountAsociationAdmin(admin.ModelAdmin):
    search_fields = (
        "account__name__icontains",
        "token__icontains",
    )
    ordering = (
        "account__name",
        "token",
    )


def remove_empty_uploads(UploadAdmin, request, queryset):
    unused_uploads = Upload.objects.annotate(num_expenses=Count("expense")).filter(
        num_expenses=0
    )
    deletes = unused_uploads.count()
    unused_uploads.delete()
    messages.success(request=request, message=f"Removed {deletes} uploads")


remove_empty_uploads.short_description = "Remove uploads with no expenses"


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    actions = [remove_empty_uploads]
    ordering = (
        "-created",
    )
