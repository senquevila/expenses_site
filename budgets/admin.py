from django.contrib import admin
from .models import Category, Budget, BudgetAssignment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category_type"]


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ["user", "period", "total", "is_active"]


@admin.register(BudgetAssignment)
class BudgetAssignmentAdmin(admin.ModelAdmin):
    list_display = ["budget", "category", "budget_amount", "expense_amount"]
