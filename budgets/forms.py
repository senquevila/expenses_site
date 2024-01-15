from django import forms
from budgets.models import Category, Budget, BudgetAssignment


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "category_type"]


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["user", "period", "total"]


class BudgetAssignmentForm(forms.ModelForm):
    class Meta:
        model = BudgetAssignment
        fields = ["budget", "category", "budget_amount", "expense_amount"]
