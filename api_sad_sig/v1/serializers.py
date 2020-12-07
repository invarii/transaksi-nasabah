from django.contrib.auth.models import User, Group
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicRelationField
from rest_framework import serializers
from .models import (
  Pegawai,
  SadProvinsi,
  SadKabKota,
  SadKecamatan,
  SadDesa,
  SadDusunDukuh,
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


class GroupSerializer(DynamicModelSerializer):
    class Meta:
        model = Group
        name = "data"
        fields = ["id", "name"]


class UserSerializer(DynamicModelSerializer):
    role = serializers.CharField(source="groups.first")

    class Meta:
        model = User
        name = "data"
        fields = ["id", "username", "email", "groups", "role"]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.is_active = True
        user.set_password(validated_data["password"])
        user.save()

        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user


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
        print(user)
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
        fields = ["id", "nama", "jabatan"]


class SadProvinsiSerializer(CustomSerializer):
    class Meta:
        model = SadProvinsi
        name = "data"
        fields = ["id", "kode_provinsi", "nama_provinsi"]


class SadKabKotaSerializer(CustomSerializer):
    class Meta:
        model = SadKabKota
        name = "data"
        fields = ["id", "provinsi", "kode_kab_kota", "nama_kab_kota"]


class SadKecamatanSerializer(CustomSerializer):
    kab_kota = DynamicRelationField(
        "SadKabKotaSerializer", deferred=False, embed=True
    )

    class Meta:
        model = SadKecamatan
        name = "data"
        fields = ["id", "kode_kecamatan", "nama_kecamatan", "kab_kota"]


class SadDesaSerializer(CustomSerializer):
    kecamatan = DynamicRelationField(
        "SadKecamatanSerializer", deferred=False, embed=True
    )

    class Meta:
        model = SadDesa
        name = "data"
        fields = ["id", "kode_desa", "nama_desa", "kecamatan"]


class SadDusunDukuhSerializer(CustomSerializer):
    class Meta:
        model = SadDusunDukuh
        name = "data"
        fields = ["id", "nama"]


class SadRwSerializer(CustomSerializer):
    class Meta:
        model = SadRw
        name = "data"
        fields = ["id", "rw"]


class SadRtSerializer(CustomSerializer):
    class Meta:
        model = SadRt
        name = "data"
        fields = ["id", "rt"]


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

class SliderSerializer(DynamicModelSerializer):
  class Meta:
    model = Slider
    name = 'data'
    exclude = []

class KategoriArtikelSerializer(DynamicModelSerializer):
  class Meta:
    model = KategoriArtikel
    name = 'data'
    exclude = []

class KategoriInformasiSerializer(DynamicModelSerializer):
  class Meta:
    model = KategoriInformasi
    name = 'data'
    exclude = []

class KategoriPotensiSerializer(DynamicModelSerializer):
  class Meta:
    model = KategoriPotensi
    name = 'data'
    exclude = []

class KategoriLaporSerializer(DynamicModelSerializer):
  class Meta:
    model = KategoriLapor
    name = 'data'
    exclude = []

class LaporSerializer(DynamicModelSerializer):
  kategori = DynamicRelationField('KategoriLaporSerializer', deferred=True, embed=True)
  class Meta:
    model = Lapor
    name = 'data'
    exclude = []

class ArtikelSerializer(DynamicModelSerializer):
  kategori = DynamicRelationField('KategoriArtikelSerializer', deferred=True, embed=True)
  class Meta:
    model = Artikel
    name = 'data'
    exclude = []

class InformasiSerializer(DynamicModelSerializer):
  kategori = DynamicRelationField('KategoriInformasiSerializer', deferred=True, embed=True)
  class Meta:
    model = Informasi
    name = 'data'
    exclude = []

class PotensiSerializer(DynamicModelSerializer):
  kategori = DynamicRelationField('KategoriPotensiSerializer', deferred=True, embed=True)
  class Meta:
    model = Potensi
    name = 'data'
    exclude = []

