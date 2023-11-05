# common imports
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

# django drf imports
from django.conf import settings
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
        if not CurrencyConvert.objects.filter(date=datetime.today()).exists():
            try:
                exchange = self._get_exchange()
            except Exception as e:
                return Response(
                    data={"message": "Problem capturing exchange"},
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            serializer = CurrencyConvertSerializer(
                data={
                    "currency": Currency.objects.filter(alpha3="USD").first().pk,
                    "exchange": exchange,
                }
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_exchange(self) -> float:
        req = Request(settings.SCRAPING_URL, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req)
        soup = BeautifulSoup(page, "html.parser")
        result = soup.find(id=settings.SCRAPING_TAG_ID)
        result_text = result.text.strip()
        tokens = result_text.split(settings.SCRAPING_TOKEN_SPLIT)
        value = float(tokens[-1].strip().replace("L", ""))
        return value
