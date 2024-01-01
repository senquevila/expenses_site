from django import forms
from django.core.validators import FileExtensionValidator

from expenses.models import Period, Expense


class ExpenseFileUploadForm(forms.Form):
    file = forms.FileField(
        label="Archivo",
        help_text="Seleccione un archivo CSV para cargar",
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
    )

    class Meta:
        model = Expense
        fields = (
            "periodo",
            "description",
            "payment_date",
            "account",
            "currency",
            "amount",
            "created",
        )
