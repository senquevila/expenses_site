from django.contrib import admin

from expenses.models import (
    Account,
    Currency,
    CurrencyConvertion,
    Period,
    Expense,
)


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    ordering = ['-year', '-month']


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(CurrencyConvertion)
class CurrencyConvertionAdmin(admin.ModelAdmin):
    pass


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    ordering = ['name']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    pass
