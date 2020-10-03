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
router.register(r'provinsi', SadProvinsiViewSet)
router.register(r'kabkota', SadKabKotaViewSet)
router.register(r'kecamatan', SadKecamatanViewSet)
router.register(r'desa', SadDesaViewSet)
router.register(r'saddusundukuh', SadDusunDukuhViewSet)
router.register(r'sadrw', SadRwViewSet)
router.register(r'sadrt', SadRtViewSet)
router.register(r'keluarga', SadKeluargaViewSet)
router.register(r'penduduk', SadPendudukViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]