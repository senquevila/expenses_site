from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Category(models.Model):
    FIXED = "FIX"
    VARIABLE = "VAR"
    CATEGORY_TYPE=(
        (FIXED, "Costo Fijo"),
        (VARIABLE, "Costo Variable"),
    )

    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE, default=FIXED)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self) -> str:
        return self.name


class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    period = models.ForeignKey("expenses.Period", on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        unique_together = ('user', 'period')
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"

    def __str__(self):
        return str(self.period)

    @property
    def is_active(self) -> bool:
        """Return True if the budget is currently active."""
        return self.period.year == now().year and self.period.month == now().month


class BudgetAssignment(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    budget_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Asignacion de presupuesto"
        verbose_name_plural = "Asignaciones de presupuesto"
