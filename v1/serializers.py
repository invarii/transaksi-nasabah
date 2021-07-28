from django.contrib.postgres import fields
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicRelationField
from django.db.models import Count
from django.apps import apps

from api_sad_sig.util import (
    CustomSerializer,
    util_columns,
    create_or_reactivate,
    create_or_reactivate_user,
)
from .models import *



class NasabahSerializer(DynamicModelSerializer):
    class Meta:
        model = Nasabah
        name = "data"
        exclude = []


class TransaksiSerializer(DynamicModelSerializer):
    class Meta:
        model = Transaksi
        name = "data"
        exclude = []

