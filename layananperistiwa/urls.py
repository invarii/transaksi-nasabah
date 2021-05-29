from rest_framework import routers

from .views import (
    SuratKelahiranViewSet,
    SuratSkckViewSet,
    SuratDomisiliViewSet,
    JenisPindahViewSet,
    KlasifikasiPindahViewSet,
    AlasanPindahViewSet,
    StatusKKTinggalViewSet,
    StatusKKPindahViewSet,
    SadKelahiranViewSet,
    SadKematianViewSet,
    SadLahirmatiViewSet,
    SadPindahKeluarViewSet,
    SadPindahMasukViewSet,
    SadPecahKKViewSet,
    LaporanKelahiranViewSet,
    LaporanKematianViewSet,
    LaporanMonografiViewSet,
    LayananSuratViewSet,
)

router = routers.DefaultRouter()

router.register(r"layanansurat/(?P<jenis_surat>[^/.]+)", LayananSuratViewSet)
router.register(r"suratkelahiran", SuratKelahiranViewSet)
router.register(r"suratskck", SuratSkckViewSet)
router.register(r"domisili", SuratDomisiliViewSet)
router.register(r"jenispindah", JenisPindahViewSet)
router.register(r"klasifikasipindah", KlasifikasiPindahViewSet)
router.register(r"alasanpindah", AlasanPindahViewSet)
router.register(r"statuskktinggal", StatusKKTinggalViewSet)
router.register(r"statuskkpindah", StatusKKPindahViewSet)
router.register(r"kelahiran", SadKelahiranViewSet)
router.register(r"kematian", SadKematianViewSet)
router.register(r"lahirmati", SadLahirmatiViewSet)
router.register(r"pindahkeluar", SadPindahKeluarViewSet)
router.register(r"pindahmasuk", SadPindahMasukViewSet)
router.register(r"pecahkk", SadPecahKKViewSet)
router.register(
    r"laporan-kelahiran", LaporanKelahiranViewSet, basename="rekap_kelahiran"
)
router.register(
    r"laporan-kematian", LaporanKematianViewSet, basename="rekap_kematian"
)
router.register(
    r"laporan-monografi", LaporanMonografiViewSet, basename="laporan_monografi"
)
