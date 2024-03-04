# Django Imports
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


# Model Imports
from expenses import views


urlpatterns = [
    path(
        "accounts/",
        views.AccountListView.as_view(),
        name="account-list",
    ),
    path(
        "accounts/transfer/",
        views.AccountTransferView.as_view(),
        name="account-transfer",
    ),
    path(
        "currency/convert/",
        views.CurrencyConvertListView.as_view(),
        name="currency-convert-list",
    ),
    path(
        "",
        views.TransactonListView.as_view(),
        name="transaction-list",
    ),
    path(
        "add/",
        views.TransactionCreateView.as_view(),
        name="transaction-add",
    ),
    path(
        "<int:pk>/edit/",
        views.TransactionUpdateView.as_view(),
        name="transaction-edit",
    ),
    path(
        "<int:pk>/delete/",
        views.TransactionDeleteView.as_view(),
        name="transaction-delete",
    ),
    path(
        "upload/",
        views.TransactionUploadView.as_view(),
        name="transaction-upload-start",
    ),
    path(
        "upload/result/<int:pk>/",
        views.TransactionUploadResult.as_view(),
        name="transaction-upload-result",
    ),
    path(
        "periods/",
        views.PeriodListView.as_view(),
        name="period-list",
    ),
    path(
        "periods/<int:period>/",
        views.TransactionGroupListView.as_view(),
        name="period-expense-group",
    ),
    path(
        "periods/<int:pk>/close/",
        views.PeriodCloseView.as_view(),
        name="period-close",
    ),
    path(
        "periods/<int:pk>/open/",
        views.PeriodOpenView.as_view(),
        name="period-open",
    ),
    path(
        "uploads/",
        views.UploadListView.as_view(),
        name="upload-list",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
