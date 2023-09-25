from django import forms
from django.core.validators import FileExtensionValidator

from expenses.models import Period, Expense


class ExpenseFileUploadForm(forms.Form):
    period = forms.ModelChoiceField(
        queryset=Period.objects.filter(closed=False).order_by("-pk"),
        empty_label=None,
        help_text="Seleccione el periodo",
    )
    file = forms.FileField(
        label="Archivo",
        help_text="Seleccione un archivo CSV para cargar",
        validators=[FileExtensionValidator(allowed_extensions=['csv'])]
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
