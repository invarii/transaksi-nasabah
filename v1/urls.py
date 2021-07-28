from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r"nasabah", NasabahViewSet)
router.register(r"transaksi", TransaksiViewSet)
