# Django Imports
from django.urls import path

# Model Imports
from expenses import api as api_views


urlpatterns = [
    path(
        "currency/convertions/",
        api_views.CurrencyConvertionViewSet.as_view({"get": "list"}),
        name="currency-convertions",
    ),
    path(
        "currency/create_usd_exchange/",
        api_views.CreateDollarConvertionView.as_view(),
        name="create-dollar-convertion",
    ),
]
