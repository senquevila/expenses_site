# common imports
import datetime
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


# django drf imports
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

# models import
from expenses.models import CurrencyConvertion, Currency
from expenses.serializers import CurrencyConvertionSerializer


class CurrencyConvertionViewSet(viewsets.ModelViewSet):
    queryset = CurrencyConvertion.objects.all()
    serializer_class = CurrencyConvertionSerializer


class CreateDollarConvertionView(APIView):
    def post(self, request, *args, **kwargs):
        data = CurrencyConvertion.objects.filter(date=datetime.datetime.today())
        if not data.exists():
            currency_convert = CurrencyConvertion()
            currency_convert.currency = get_object_or_404(Currency, alpha3="USD")
            currency_convert.date = datetime.datetime.today()
            currency_convert.exchange = self._get_exchange()
            currency_convert.save()
        return Response(status=status.HTTP_200_OK)

    def _get_exchange(self) -> float:
        req = Request(settings.SCRAPING_URL, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req)
        soup = BeautifulSoup(page)
        result = soup.find(id=settings.SCRAPING_TAG_ID)
        result_text = result.text.strip()
        tokens = result_text.split(settings.SCRAPING_TOKEN_SPLIT)
        value_str = tokens[-1].strip().replace("L", "")
        value = float(value_str)
        return value
