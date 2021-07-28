from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicRelationField

from .models import *

class NasabahSerializer(DynamicModelSerializer):
    class Meta:
        model = Nasabah
        name = "data"
        exclude = []


class TransaksiSerializer(DynamicModelSerializer):
    nasabah = DynamicRelationField(
        "NasabahSerializer", deferred=False, embed=True
    )
    class Meta:
        model = Transaksi
        name = "data"
        exclude = []

