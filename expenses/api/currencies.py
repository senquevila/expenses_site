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
from expenses.models import CurrencyConvert, Currency
from expenses.serializers import CurrencyConvertSerializer


class CurrencyConvertViewSet(viewsets.ModelViewSet):
    queryset = CurrencyConvert.objects.all()
    serializer_class = CurrencyConvertSerializer


class CreateDollarConvertionView(APIView):
    def post(self, request, *args, **kwargs):
        data = CurrencyConvert.objects.filter(date=datetime.datetime.today())
        if not data.exists():
            currency_convert = CurrencyConvert()
            currency_convert.currency = get_object_or_404(Currency, alpha3="USD")
            currency_convert.date = datetime.datetime.today()
            try:
                currency_convert.exchange = self._get_exchange()
            except Exception as e:
                return Response(
                    data={"message": "Problem capturing exchange"},
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )
            currency_convert.save()
        return Response(status=status.HTTP_200_OK)

    def _get_exchange(self) -> float:
        req = Request(settings.SCRAPING_URL, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req)
        soup = BeautifulSoup(page, "html.parser")
        result = soup.find(id=settings.SCRAPING_TAG_ID)
        result_text = result.text.strip()
        tokens = result_text.split(settings.SCRAPING_TOKEN_SPLIT)
        value = float(tokens[-1].strip().replace("L", ""))
        return value
