from django.urls import include, path
from rest_framework import routers

from .views import (
  UserViewSet,
  GroupViewSet,
  TokenObtainPairView,
  TokenRefreshView,
  PegawaiViewSet,
  SadProvinsiViewSet,
  SadKabKotaViewSet,
  SadKecamatanViewSet,
  SadDesaViewSet,
  SadDusunDukuhViewSet,
  SadRwViewSet,
  SadRtViewSet,
  SadKeluargaViewSet,
  SadPendudukViewSet,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'pegawai', PegawaiViewSet)
router.register(r'sadprovinsi', SadProvinsiViewSet)
router.register(r'sadkabkota', SadKabKotaViewSet)
router.register(r'sadkecamatan', SadKecamatanViewSet)
router.register(r'saddesa', SadDesaViewSet)
router.register(r'saddusundukuh', SadDusunDukuhViewSet)
router.register(r'sadrw', SadRwViewSet)
router.register(r'sadrt', SadRtViewSet)
router.register(r'sadkeluarga', SadKeluargaViewSet)
router.register(r'penduduk', SadPendudukViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]