from rest_framework import routers

from .views import (
    PegawaiViewSet,
    SadProvinsiViewSet,
    SadKabKotaViewSet,
    SadKecamatanViewSet,
    SadDesaViewSet,
    SadDusunViewSet,
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
    SigSadBidangViewSet,
    SigSadBidang2ViewSet,
    SigDesaViewSet,
    SigDusunViewSet,
    SigDukuhViewSet,
    SigRtViewSet,
    SigRwViewSet,
    SigDukuh2ViewSet,
    SigRt2ViewSet,
    SigRw2ViewSet,
    KategoriArtikelViewSet,
    KategoriInformasiViewSet,
    KategoriLaporViewSet,
    KategoriPotensiViewSet,
    ArtikelViewSet,
    LaporViewSet,
    InformasiViewSet,
    PotensiViewSet,
    SuratKelahiranViewSet,
    SuratSkckViewSet,
    SuratDomisiliViewSet,
)

router = routers.DefaultRouter()
router.register(r'pegawai', PegawaiViewSet)
router.register(r'provinsi', SadProvinsiViewSet)
router.register(r'kabkota', SadKabKotaViewSet)
router.register(r'kecamatan', SadKecamatanViewSet)
router.register(r'desa', SadDesaViewSet)
router.register(r'saddusun', SadDusunViewSet)
router.register(r'sadrw', SadRwViewSet)
router.register(r'sadrt', SadRtViewSet)
router.register(r'keluarga', SadKeluargaViewSet)
router.register(r'penduduk', SadPendudukViewSet)
router.register(r'kelahiran', SadKelahiranViewSet)
router.register(r'kematian', SadKematianViewSet)
router.register(r'lahirmati', SadLahirmatiViewSet)
router.register(r'pindahkeluar', SadPindahKeluarViewSet)
router.register(r'pindahmasuk', SadPindahMasukViewSet)
router.register(r'sarpras', SadSarprasViewSet)
router.register(r'inventaris', SadInventarisViewSet)
router.register(r'surat', SadSuratViewSet)
router.register(r'detailsurat', SadDetailSuratViewSet)
router.register(r'sigbidang', SigBidangViewSet)
router.register(r'sigsadbidang', SigSadBidangViewSet)
router.register(r'sigsadbidang2', SigSadBidang2ViewSet)
router.register(r'sigdesa', SigDesaViewSet)
router.register(r'sigdusun', SigDusunViewSet)
router.register(r'sigdukuh', SigDukuhViewSet)
router.register(r'sigrw', SigRwViewSet)
router.register(r'sigrt', SigRtViewSet)
router.register(r'sigdukuh2', SigDukuh2ViewSet)
router.register(r'sigrw2', SigRw2ViewSet)
router.register(r'sigrt2', SigRt2ViewSet)
router.register(r'kategorilapor', KategoriLaporViewSet)
router.register(r'kategoriinformasi', KategoriInformasiViewSet)
router.register(r'kategoriartikel', KategoriArtikelViewSet)
router.register(r'kategoripotensi', KategoriPotensiViewSet)
router.register(r'artikel', ArtikelViewSet)
router.register(r'informasi', InformasiViewSet)
router.register(r'potensi', PotensiViewSet)
router.register(r'lapor', LaporViewSet)
router.register(r'suratkelahiran', SuratKelahiranViewSet)
router.register(r'suratskck', SuratSkckViewSet)
router.register(r'domisili', SuratDomisiliViewSet)

