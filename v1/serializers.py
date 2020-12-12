from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicRelationField
from rest_framework import serializers
from .models import (
    Pegawai,
    SadProvinsi,
    SadKabKota,
    SadKecamatan,
    SadDesa,
    SadDusun,
    SadRw,
    SadRt,
    SadKeluarga,
    SadPenduduk,
    SadKelahiran,
    SadKematian,
    SadLahirmati,
    SadPindahKeluar,
    SadPindahMasuk,
    SadSarpras,
    SadInventaris,
    SadSurat,
    SadDetailSurat,
    SigSadBidang,
    SigSadBidang2,
    SigBidang,
    SigDesa,
    SigRw,
    SigRt,
    SigRw2,
    SigRt2,
    SigDusun,
    SigDukuh,
    SigDukuh2,
    Slider,
    KategoriArtikel,
    Artikel,
    KategoriInformasi,
    Informasi,
    KategoriPotensi,
    Potensi,
    KategoriLapor,
    Lapor,
)


class CustomSerializer(DynamicModelSerializer):
    extra_kwargs = {"created_by": {"write_only": True}}

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["updated_by"] = user
        data = super().update(instance, validated_data)
        data.save()
        return data

    class Meta:
        model = None


class PegawaiSerializer(CustomSerializer):
    class Meta:
        model = Pegawai
        name = "data"
        exclude = []


class SadProvinsiSerializer(CustomSerializer):
    class Meta:
        model = SadProvinsi
        name = "data"
        exclude = []


class SadKabKotaSerializer(CustomSerializer):
    class Meta:
        model = SadKabKota
        name = "data"
        exclude = []


class SadKecamatanSerializer(CustomSerializer):
    kab_kota = DynamicRelationField(
        "SadKabKotaSerializer", deferred=False, embed=True
    )

    class Meta:
        model = SadKecamatan
        name = "data"
        exclude = []


class SadDesaSerializer(CustomSerializer):
    kecamatan = DynamicRelationField(
        "SadKecamatanSerializer", deferred=False, embed=True
    )

    class Meta:
        model = SadDesa
        name = "data"
        exclude = []


class SadDusunSerializer(CustomSerializer):
    desa = DynamicRelationField(
        "SadDesaSerializer", deferred=False, embed=True
    )

    class Meta:
        model = SadDusun
        name = "data"
        exclude = []


class SadRwSerializer(CustomSerializer):
    dusun = DynamicRelationField(
        "SadDusunSerializer", deferred=False, embed=True
    )

    class Meta:
        model = SadRw
        name = "data"
        exclude = []


class SadRtSerializer(CustomSerializer):
    rw = DynamicRelationField("SadRwSerializer", deferred=False, embed=True)

    class Meta:
        model = SadRt
        name = "data"
        exclude = []


class SadKeluargaSerializer(CustomSerializer):
    anggota = DynamicRelationField(
        "SadPendudukSerializer", many=True, deferred=True, embed=True
    )

    class Meta:
        model = SadKeluarga
        name = "data"
        exclude = []
        extra_kwargs = {
            "created_by": {"default": serializers.CurrentUserDefault()}
        }


class SadPendudukSerializer(CustomSerializer):
    keluarga = DynamicRelationField(
        "SadKeluargaSerializer", deferred=True, embed=True
    )

    class Meta:
        model = SadPenduduk
        name = "data"
        exclude = []


class SadKelahiranSerializer(CustomSerializer):
    class Meta:
        model = SadKelahiran
        name = "data"
        exclude = []


class SadKematianSerializer(CustomSerializer):
    penduduk = DynamicRelationField(
        "SadPendudukSerializer", deferred=True, embed=True
    )

    class Meta:
        model = SadKematian
        name = "data"
        exclude = []


class SadLahirmatiSerializer(CustomSerializer):
    class Meta:
        model = SadLahirmati
        name = "data"
        exclude = []


class SadPindahKeluarSerializer(CustomSerializer):
    class Meta:
        model = SadPindahKeluar
        name = "data"
        exclude = []


class SadPindahMasukSerializer(CustomSerializer):
    class Meta:
        model = SadPindahMasuk
        name = "data"
        fields = ["id", "no_kk", "nik_kepala_keluarga"]


class SadSarprasSerializer(CustomSerializer):
    class Meta:
        model = SadSarpras
        name = "data"
        fields = ["id", "nama_sarpras", "asal"]


class SadInventarisSerializer(CustomSerializer):
    class Meta:
        model = SadInventaris
        name = "data"
        fields = ["id", "nama_inventaris", "asal"]


class SadSuratSerializer(CustomSerializer):
    class Meta:
        model = SadSurat
        name = "data"
        fields = ["id", "judul", "sifat"]


class SadDetailSuratSerializer(CustomSerializer):
    class Meta:
        model = SadDetailSurat
        name = "data"
        fields = ["id", "no_surat", "keterangan"]


class SigDesaSerializer(CustomSerializer):
    class Meta:
        model = SigDesa
        name = "data"
        exclude = []


class SigDusunSerializer(CustomSerializer):
    sig_desa = DynamicRelationField(
        "SigDesaSerializer", deferred=True, embed=True
    )

    class Meta:
        model = SigDusun
        name = "data"
        exclude = []


class SigDukuhSerializer(CustomSerializer):
    sig_dusun = DynamicRelationField(
        "SigDusunSerializer", deferred=True, embed=True
    )

    class Meta:
        model = SigDukuh
        name = "data"
        exclude = []


class SigDukuh2Serializer(CustomSerializer):
    sig_desa = DynamicRelationField(
        "SigDesaSerializer", deferred=True, embed=True
    )

    class Meta:
        model = SigDukuh2
        name = "data"
        exclude = []


class SigRwSerializer(CustomSerializer):
    sig_dukuh = DynamicRelationField(
        "SigDukuhSerializer", deferred=True, embed=True
    )

    class Meta:
        model = SigRw
        name = "data"
        exclude = []


class SigRtSerializer(CustomSerializer):
    sig_rw = DynamicRelationField("SigRwSerializer", deferred=True, embed=True)

    class Meta:
        model = SigRt
        name = "data"
        exclude = []


class SigRw2Serializer(CustomSerializer):
    sig_dukuh2 = DynamicRelationField(
        "SigDukuh2Serializer", deferred=True, embed=True
    )

    class Meta:
        model = SigRw2
        name = "data"
        exclude = []


class SigRt2Serializer(CustomSerializer):
    sig_rw2 = DynamicRelationField(
        "SigRw2Serializer", deferred=True, embed=True
    )

    class Meta:
        model = SigRt2
        name = "data"
        exclude = []


class SigBidangSerializer(CustomSerializer):
    desa = DynamicRelationField("SigDesaSerializer", deferred=True, embed=True)

    class Meta:
        model = SigBidang
        name = "data"
        exclude = []


class SigSadBidangSerializer(CustomSerializer):
    sad_penduduk = DynamicRelationField(
        "SadPendudukSerializer", deferred=True, embed=True
    )
    sig_bidang = DynamicRelationField(
        "SigBidangSerializer", deferred=True, embed=True
    )

    class Meta:
        model = SigSadBidang
        name = "data"
        exclude = []


class SigSadBidang2Serializer(CustomSerializer):
    sad_penduduk = DynamicRelationField(
        "SadPendudukSerializer", deferred=True, embed=True
    )
    sig_bidang2 = DynamicRelationField(
        "SigBidang2Serializer", deferred=True, embed=True
    )

    class Meta:
        model = SigSadBidang2
        name = "data"
        exclude = []


class SliderSerializer(DynamicModelSerializer):
    class Meta:
        model = Slider
        name = "data"
        exclude = []


class KategoriArtikelSerializer(DynamicModelSerializer):
    class Meta:
        model = KategoriArtikel
        name = "data"
        exclude = []


class KategoriInformasiSerializer(DynamicModelSerializer):
    class Meta:
        model = KategoriInformasi
        name = "data"
        exclude = []


class KategoriPotensiSerializer(DynamicModelSerializer):
    class Meta:
        model = KategoriPotensi
        name = "data"
        exclude = []


class KategoriLaporSerializer(DynamicModelSerializer):
    class Meta:
        model = KategoriLapor
        name = "data"
        exclude = []


class LaporSerializer(DynamicModelSerializer):
    kategori = DynamicRelationField(
        "KategoriLaporSerializer", deferred=True, embed=True
    )

    class Meta:
        model = Lapor
        name = "data"
        exclude = []


class ArtikelSerializer(DynamicModelSerializer):
    kategori = DynamicRelationField(
        "KategoriArtikelSerializer", deferred=True, embed=True
    )

    class Meta:
        model = Artikel
        name = "data"
        exclude = []


class InformasiSerializer(DynamicModelSerializer):
    kategori = DynamicRelationField(
        "KategoriInformasiSerializer", deferred=True, embed=True
    )

    class Meta:
        model = Informasi
        name = "data"
        exclude = []


class PotensiSerializer(DynamicModelSerializer):
    kategori = DynamicRelationField(
        "KategoriPotensiSerializer", deferred=True, embed=True
    )

    class Meta:
        model = Potensi
        name = "data"
        exclude = []
