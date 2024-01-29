from typing import Any

from django.db.models import ExpressionWrapper, F, FloatField, Sum
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from rest_framework.views import APIView

from budgets.models import Category, Budget, BudgetAssignment, MatchAccount
from budgets.forms import CategoryForm, BudgetForm, BudgetAssignmentForm
from expenses.models import Expense


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "budgets/category_form.html"
    success_url = reverse_lazy("category-list")  # Replace with the actual URL


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "budgets/category_form.html"
    success_url = reverse_lazy("category-list")


class CategoryListView(ListView):
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"


class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = "budgets/budget_form.html"
    success_url = reverse_lazy("budget-list")


class BudgetUpdateView(UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = "budgets/budget_form.html"
    success_url = reverse_lazy("budget-list")


class BudgetListView(ListView):
    model = Budget
    template_name = "budget_list.html"
    context_object_name = "budgets"


class BudgetAssignmentCreateView(CreateView):
    model = BudgetAssignment
    form_class = BudgetAssignmentForm
    template_name = "budgets/budget_assignment_form.html"
    success_url = reverse_lazy("budget-list")


class BudgetAssignmentUpdateView(UpdateView):
    model = BudgetAssignment
    form_class = BudgetAssignmentForm
    template_name = "budgets/budget_assignment_form.html"
    success_url = reverse_lazy("budget-list")


class BudgetUpdateExpensesView(APIView):
    def get(self, request, pk=None):
        budget = get_object_or_404(Budget, pk=pk)

        # Fetch expenses from the previous period
        expenses = Expense.objects.filter(period=budget.period)
        BudgetAssignment.objects.filter(
            budget=budget,
        ).update(expense_amount=0)

        for expense in expenses:
            # Find corresponding MatchAccount entry
            match_entry = MatchAccount.objects.filter(account=expense.account).first()

            if not match_entry:
                continue

            try:
                assignament = BudgetAssignment.objects.get(
                    budget=budget,
                    category=match_entry.category,
                )
                assignament.expense_amount += expense.local_amount
                assignament.save()
            except BudgetAssignment.DoesNotExist:
                print(match_entry.category.name)

        return redirect("budget-list")


class BudgetAssigmentListView(ListView):
    model = BudgetAssignment
    template_name = "budgets/budget_assignment_list.html"
    context_object_name = "budget_assignments"

    def get_queryset(self):
        budget = get_object_or_404(Budget, pk=self.kwargs["pk"])
        queryset = BudgetAssignment.objects.filter(budget=budget).annotate(
            difference=ExpressionWrapper(
                F("expense_amount") / F("budget_amount"), output_field=FloatField()
            )
        )
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        total = BudgetAssignment.objects.filter(budget__pk=self.kwargs["pk"]).aggregate(
            total_budget=Sum("budget_amount"),
            total_expense=Sum("expense_amount"),
        )
        context["total_budget"] = round(total.get("total_budget", 0), 2)
        context["total_expense"] = round(total.get("total_expense", 0), 2)
        return context
