from django import forms
from django.core.validators import FileExtensionValidator

from expenses.models import Account, Expense


class ExpenseUploadForm(forms.Form):
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


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            "description",
            "payment_date",
            "period",
            "account",
            "currency",
            "amount",
        ]


class AccountTransferForm(forms.Form):
    account_origin = forms.ModelChoiceField(queryset=Account.objects.all())
    account_destination = forms.ModelChoiceField(queryset=Account.objects.all())

    def clean(self):
        cleaned_data = super().clean()
        account_origin = cleaned_data.get("account_origin")
        account_destination = cleaned_data.get("account_destination")

        if account_origin == account_destination:
            raise forms.ValidationError("Accounts cannot be the same")

        return cleaned_data
