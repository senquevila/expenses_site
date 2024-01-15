from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .models import Category, Budget, BudgetAssignment
from .forms import CategoryForm, BudgetForm, BudgetAssignmentForm


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "budgets/category_form.html"
    success_url = reverse_lazy("category_list")  # Replace with the actual URL


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "budgets/category_form.html"
    success_url = reverse_lazy("category_list")


class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = "budgets/budget_form.html"
    success_url = reverse_lazy("budget_list")


class BudgetUpdateView(UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = "budgets/budget_form.html"
    success_url = reverse_lazy("budget_list")


class BudgetAssignmentCreateView(CreateView):
    model = BudgetAssignment
    form_class = BudgetAssignmentForm
    template_name = "budgets/budget_assignment_form.html"
    success_url = reverse_lazy("budget_assignment_list")


class BudgetAssignmentUpdateView(UpdateView):
    model = BudgetAssignment
    form_class = BudgetAssignmentForm
    template_name = "budgets/budget_assignment_form.html"
    success_url = reverse_lazy("budget_assignment_list")
