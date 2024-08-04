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

from expenses.utils.tools import create_dollar_conversion


class CurrencyConvertViewSet(viewsets.ModelViewSet):
    queryset = CurrencyConvert.objects.all()
    serializer_class = CurrencyConvertSerializer


class CreateDollarConversionView(APIView):
    def post(self, request, *args, **kwargs):
        data, status = create_dollar_conversion()
        return Response(data, status=status)