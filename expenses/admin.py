from django.contrib import admin

from expenses.models import (
    Account,
    AccountAsociation,
    Currency,
    CurrencyConvert,
    Period,
    Expense,
)


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    ordering = ["-year", "-month"]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(CurrencyConvert)
class CurrencyConvertAdmin(admin.ModelAdmin):
    pass


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    ordering = ["name"]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "period",
        "description",
        "currency",
        "amount",
        "account_name",
        "payment_date",
        "created",
    )
    list_filter = (
        "period",
        "account",
        "created",
    )
    ordering = (
        "-payment_date",
        "-created",
    )
    search_fields = (
        "description__startswith",
        "amount",
    )

    def account_name(self, obj):
        return obj.account.name

    account_name.short_description = "Account Name"


@admin.register(AccountAsociation)
class AccountAsociationAdmin(admin.ModelAdmin):
    search_fields = (
        "account__name",
        "token",
    )
    ordering = (
        "account__name",
        "token",
    )
