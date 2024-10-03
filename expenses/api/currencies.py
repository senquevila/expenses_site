# django drf imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

# models import
from expenses.models import CurrencyConvert
from expenses.serializers import CurrencyConvertSerializer

from expenses.utils.tools import create_dollar_conversion


class CurrencyConvertViewSet(viewsets.ModelViewSet):
    queryset = CurrencyConvert.objects.all()
    serializer_class = CurrencyConvertSerializer


class CreateDollarConversionView(APIView):
    def post(self, request, *args, **kwargs):
        data, _status = create_dollar_conversion()
        return Response(data, status=_status)
