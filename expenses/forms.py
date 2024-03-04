from django import forms
from django.core.validators import FileExtensionValidator

from expenses.models import Account, Transaction


class TransactionUploadForm(forms.Form):
    file = forms.FileField(
        label="Archivo",
        help_text="Seleccione un archivo CSV para cargar",
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
    )

    class Meta:
        model = Transaction
        fields = (
            "periodo",
            "description",
            "payment_date",
            "account",
            "currency",
            "amount",
            "created",
        )


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "description",
            "payment_date",
            "period",
            "account",
            "currency",
            "amount",
        ]


class AccountTransferForm(forms.Form):
    account_origin = forms.ModelChoiceField(queryset=Account.objects.order_by("name"))
    account_destination = forms.ModelChoiceField(queryset=Account.objects.order_by("name"))

    def clean(self):
        cleaned_data = super().clean()
        account_origin = cleaned_data.get("account_origin")
        account_destination = cleaned_data.get("account_destination")

        if account_origin == account_destination:
            raise forms.ValidationError("Accounts cannot be the same")

        return cleaned_data
