from io import BytesIO
import numpy as np

from django.conf import settings
from django.db.utils import IntegrityError
from django.db.models import F, Count, Avg, Sum
from django.http import HttpResponse
from dynamic_rest.viewsets import DynamicModelViewSet
import pytz
from rest_framework.permissions import AllowAny

from .serializers import *
from .models import *


class NasabahViewSet(DynamicModelViewSet):
    queryset = Nasabah.objects.all().order_by("id")
    serializer_class = NasabahSerializer
    permission_classes = [AllowAny]


class TransaksiViewSet(DynamicModelViewSet):
    queryset = Transaksi.objects.all().order_by("id")
    serializer_class = TransaksiSerializer
    permission_classes = [AllowAny]