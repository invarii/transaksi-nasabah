from django.urls import include, path
from rest_framework import routers

from .views import (
    UserViewSet,
    GroupViewSet,
    TokenObtainPairView,
    TokenRefreshView,
    PegawaiViewSet,
    SadProvinsiList,
    SadKabKotaViewSet,
    SadKecamatanViewSet,
    SadDesaViewSet,
    SadDusunDukuhViewSet,
    SadRwViewSet,
    SadRtViewSet,
    SadKeluargaViewSet,
    SadPendudukViewSet,
    SadKelahiranViewSet,
    SadKematianViewSet,
    SadLahirmatiViewSet,
    SadPindahKeluarViewSet,
    SadPindahMasukViewSet,
    SadSarprasViewSet,
    SadInventarisViewSet,
    SadSuratViewSet,
    SadDetailSuratViewSet,
    SigBidangViewSet,
    SigDesaViewSet,
    SigDusunViewSet,
    SigDukuhViewSet,
    SigRtViewSet,
    SigRwViewSet,
    SigDukuh2ViewSet,
    SigRt2ViewSet,
    SigRw2ViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"pegawai", PegawaiViewSet)
router.register(r"provinsi", SadProvinsiList)
router.register(r"kabkota", SadKabKotaViewSet)
router.register(r"kecamatan", SadKecamatanViewSet)
router.register(r"desa", SadDesaViewSet)
router.register(r"saddusundukuh", SadDusunDukuhViewSet)
router.register(r"sadrw", SadRwViewSet)
router.register(r"sadrt", SadRtViewSet)
router.register(r"keluarga", SadKeluargaViewSet)
router.register(r"penduduk", SadPendudukViewSet)
router.register(r"kelahiran", SadKelahiranViewSet)
router.register(r"kematian", SadKematianViewSet)
router.register(r"lahirmati", SadLahirmatiViewSet)
router.register(r"pindahkeluar", SadPindahKeluarViewSet)
router.register(r"pindahmasuk", SadPindahMasukViewSet)
router.register(r"sarpras", SadSarprasViewSet)
router.register(r"inventaris", SadInventarisViewSet)
router.register(r"surat", SadSuratViewSet)
router.register(r"detailsurat", SadDetailSuratViewSet)
router.register(r"sigbidang", SigBidangViewSet)
router.register(r"sigdesa", SigDesaViewSet)
router.register(r"sigdusun", SigDusunViewSet)
router.register(r"sigdukuh", SigDukuhViewSet)
router.register(r"sigrw", SigRwViewSet)
router.register(r"sigrt", SigRtViewSet)
router.register(r"sigdukuh2", SigDukuh2ViewSet)
router.register(r"sigrw2", SigRw2ViewSet)
router.register(r"sigrt2", SigRt2ViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]
