from datetime import timedelta
from decimal import Decimal

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import F
from django.db.models.functions import Abs
from django.utils import timezone

from expenses.mixins import CreationModificationDateMixin


class Period(models.Model):
    month = models.IntegerField(_("Mes"))
    year = models.IntegerField(_("Año"))
    closed = models.BooleanField(_("Solo lectura"), default=False)
    total = models.DecimalField(_("Monto total"), max_digits=13, decimal_places=2, default=0)
    active = models.BooleanField(_("Es visible"), default=True)

    class Meta:
        verbose_name = _("Periodo")
        verbose_name_plural = _("Periodos")

    def __str__(self) -> str:
        return f"{self.year}-{self.month:02}"

    @staticmethod
    def get_period_from_date(payment_date):
        try:
            return Period.objects.get(year=payment_date.year, month=payment_date.month)
        except Period.DoesNotExist:
            return None


class Currency(models.Model):
    name = models.CharField(_("Nombre"), max_length=100)
    alpha3 = models.CharField(_("Codigo alpha-3"), max_length=3, blank=True, null=True)

    class Meta:
        verbose_name = _("Moneda")
        verbose_name_plural = _("Monedas")

    def __str__(self) -> str:
        return self.name


class CurrencyConvert(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    exchange = models.DecimalField(_("Tasa de conversión"), max_digits=10, decimal_places=4)
    date = models.DateField(_("Fecha de conversión"), auto_now_add=True)

    class Meta:
        verbose_name = _("Conversion de moneda")
        verbose_name_plural = _("Conversiones de monedas")

    def __str__(self) -> str:
        return f"{self.date} > {self.currency}"


class Account(models.Model):
    DEBE = -1
    HABER = 1
    SIGN_TYPE = (
        (DEBE, "Debe (-)"),
        (HABER, "Haber (+)"),
    )
    FIXED = "FIX"
    VARIABLE = "VAR"
    ACCOUNT_TYPE = (
        (FIXED, "Fijo"),
        (VARIABLE, "Variable"),
    )
    name = models.CharField(_("Nombre"), max_length=100)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    sign = models.IntegerField(_("Signo"), choices=SIGN_TYPE)
    account_type = models.CharField(
        _("Tipo de cuenta"), max_length=5, choices=ACCOUNT_TYPE, default=VARIABLE
    )

    class Meta:
        verbose_name = _("Cuenta")
        verbose_name_plural = _("Cuentas")

    def __str__(self) -> str:
        _sign = "-" if self.sign == -1 else "+"
        p_name = f" < {self.parent.name}" if self.parent else ""
        return f"{self.name} {p_name} [{_sign}{self.account_type}]"

class Accountable(CreationModificationDateMixin):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = models.DecimalField(_("Monto"), max_digits=13, decimal_places=2)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.period} => {self.account}: {self.currency.alpha3} {self.amount}"

    @property
    def amount_str(self):
        return f"{self.currency.alpha3} {self.amount}"

    @property
    def get_signed_value(self) -> float:
        return self.amount * self.account.sign


def expense_upload_path(instance, filename):
    now = timezone.now()
    return f"expenses/{now.strftime('%Y/%m')}/{filename}"


class Upload(CreationModificationDateMixin):
    file = models.FileField(_("Archivo"), blank=True, null=True, upload_to=expense_upload_path)
    lines = models.IntegerField(_("Número de líneas"), default=0)
    result = models.JSONField(_("Resultado"), blank=True, null=True)

    class Meta:
        verbose_name = _("Subida de archivo")
        verbose_name_plural = _("Subidas de archivos")

    def __str__(self) -> str:
        return str(self.file.name)


class Expense(Accountable):
    description = models.CharField(_("Descripción"), max_length=255, blank=True, null=True)
    payment_date = models.DateField(_("Fecha de pago"), default=timezone.now, blank=True, null=True)
    local_amount = models.DecimalField(
        _("Monto local"), max_digits=13, decimal_places=2, default=0, editable=False
    )
    upload = models.ForeignKey(
        Upload,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = _("Gasto")
        verbose_name_plural = _("Gastos")

    def __str__(self) -> str:
        return super().__str__()

    @property
    def get_local_amount(self) -> Decimal:
        data = (
            CurrencyConvert.objects.filter(
                currency=self.currency,
                date__lte=self.payment_date + timedelta(days=30),
                date__gte=self.payment_date - timedelta(days=30),
            )
            .annotate(date_difference=Abs(F("date") - self.payment_date))
            .order_by("date_difference")
            .values("exchange")[:1]
        )
        exchange = data[0]["exchange"] if data else 1
        return Decimal(self.amount) * Decimal(self.account.sign) * Decimal(exchange)

    def save(self, *args, **kwargs):
        self.local_amount = self.get_local_amount
        super(Expense, self).save(*args, **kwargs)


class AccountAsociation(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    token = models.CharField(_("Token para asociar"), max_length=100)

    class Meta:
        verbose_name = _("Asociacion de cuenta")
        verbose_name_plural = _("Asociaciones de cuentas")

    def __str__(self) -> str:
        return f"{self.account.name} -> {self.token}"


class UploadData(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    json = models.JSONField()