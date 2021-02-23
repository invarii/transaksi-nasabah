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


class PegawaiSerializer(CustomSerializer):
    absensi = DynamicRelationField(
        "AbsensiSerializer", many=True, deferred=True, embed=True
    )

    def to_representation(self, instance):
        data = super(PegawaiSerializer, self).to_representation(instance)
        totalabsensi = instance.absensi.aggregate(total_absensi=Count("pegawai__id"))

        data["totalabsensi"] = totalabsensi["total_absensi"]
        return data

    class Meta:
        model = Pegawai
        name = "data"
        fields = [
            "id",
            "nip",
            "chip_ektp",
            "nama",
            "jabatan",
            "status",
            "golongan",
            "gambar",
            "absensi",
        ]


class SadProvinsiSerializer(CustomSerializer):
    class Meta:
        model = SadProvinsi
        name = "data"
        exclude = []


class SadKabKotaSerializer(CustomSerializer):
    provinsi = DynamicRelationField(SadProvinsiSerializer)

    class Meta:
        model = SadKabKota
        name = "data"
        exclude = util_columns


class SadKecamatanSerializer(CustomSerializer):
    kab_kota = DynamicRelationField(SadKabKotaSerializer)

    class Meta:
        model = SadKecamatan
        name = "data"
        exclude = util_columns


class SadDesaSerializer(CustomSerializer):
    kecamatan = DynamicRelationField(SadKecamatanSerializer)

    class Meta:
        model = SadDesa
        name = "data"
        exclude = util_columns


class BatasDesaSerializer(CustomSerializer):
    desa = DynamicRelationField("SadDesaSerializer", deferred=False, embed=True)

    class Meta:
        model = BatasDesa
        name = "data"
        exclude = []


class SadDusunSerializer(CustomSerializer):
    desa = DynamicRelationField(SadDesaSerializer)

    class Meta:
        model = SadDusun
        name = "data"
        exclude = util_columns


class SadRwSerializer(CustomSerializer):
    dusun = DynamicRelationField("SadDusunSerializer", deferred=True, embed=True)

    class Meta:
        model = SadRw
        name = "data"
        exclude = util_columns


class SadRtSerializer(CustomSerializer):
    rw = DynamicRelationField("SadRwSerializer", deferred=True, embed=True)

    class Meta:
        model = SadRt
        name = "data"
        exclude = util_columns


class MiniSadRtSerializer(CustomSerializer):
    class Meta:
        model = SadRt
        name = "data"
        fields = ["rw", "id", "rt"]


class MiniSadRwSerializer(CustomSerializer):
    class Meta:
        model = SadRw
        name = "data"
        fields = ["id", "rw"]


class MiniSadDusunSerializer(CustomSerializer):
    class Meta:
        model = SadDusun
        name = "data"
        fields = ["id", "nama"]


class SadKeluargaSerializer(CustomSerializer):
    anggota = DynamicRelationField(
        "SadPendudukSerializer", many=True, deferred=True, embed=True
    )
    kepala_keluarga = serializers.DictField(read_only=True)

    dusun_id = serializers.IntegerField(write_only=True, required=False)
    rt_id = serializers.IntegerField(write_only=True, required=False)
    alamat_lengkap = serializers.CharField(
        source="alamat.alamat_lengkap", read_only=True
    )
    alamat_id = serializers.DictField(source="alamat.alamat_id", read_only=True)
    jalan_blok = serializers.CharField(source="alamat.jalan_blok", required=False)

    def create(self, data):
        alamat = Alamat()
        if data.get("dusun_id"):
            alamat.set_from_dusun(data.get("dusun_id"))
        elif data.get("rt_id"):
            alamat.set_from_rt(data.get("rt_id"))
        else:
            raise ValidationError("Need dusun_id or rt_id", 400)

        if data.get("alamat"):
            jalan_blok = data.pop("alamat").pop("jalan_blok", None)
            if jalan_blok:
                alamat.jalan_blok = jalan_blok

        keluarga_data = data.copy()
        keluarga_data.pop("dusun_id", None)
        keluarga_data.pop("rt_id", None)
        keluarga = SadKeluarga(**keluarga_data)

        alamat.save()
        keluarga.alamat = alamat
        keluarga.save()
        return keluarga

    def update(self, instance, data):
        if data.get("dusun_id"):
            instance.alamat.set_from_dusun(data.get("dusun_id"))
        elif data.get("rt_id"):
            instance.alamat.set_from_rt(data.get("rt_id"))

        if data.get("alamat"):
            jalan_blok = data.pop("alamat").pop("jalan_blok", None)
            if jalan_blok:
                instance.alamat.jalan_blok = jalan_blok

        instance.alamat.save()
        keluarga_data = data.copy()
        keluarga_data.pop("dusun_id", None)
        keluarga_data.pop("rt_id", None)
        keluarga_data.pop("alamat", None)
        for key, value in keluarga_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = SadKeluarga
        name = "data"
        exclude = util_columns + ["alamat"]
        extra_kwargs = {"created_by": {"default": serializers.CurrentUserDefault()}}


class SadPendudukSerializer(CustomSerializer):
    keluarga = DynamicRelationField("SadKeluargaSerializer", deferred=True, embed=True)

    class Meta:
        model = SadPenduduk
        name = "data"
        exclude = []

    def create(self, data):
        penduduk = create_or_reactivate(SadPenduduk, {"nik": data["nik"]}, data)
        password = str(data["tgl_lahir"]).replace("-", "")
        penduduk_user = create_or_reactivate_user(data["nik"], password)
        penduduk.user = penduduk_user
        penduduk.save()
        penduduk.user.save()

        request_data = self.context["request"].data
        if request_data.get("kelahiran_id") is not None:
            Kelahiran = apps.get_model("layananperistiwa.SadKelahiran")
            kelahiran = Kelahiran.objects.get(id=request_data["kelahiran_id"])
            kelahiran.penduduk = penduduk
            kelahiran.save()

        return penduduk


class SadSarprasSerializer(CustomSerializer):
    alamat = Alamat()

    class Meta:
        model = SadSarpras
        name = "data"
        exclude = []


class SadInventarisSerializer(CustomSerializer):
    class Meta:
        model = SadInventaris
        name = "data"
        exclude = []


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
    sig_desa = DynamicRelationField("SigDesaSerializer", deferred=True, embed=True)

    class Meta:
        model = SigDusun
        name = "data"
        exclude = []


class SigDukuhSerializer(CustomSerializer):
    sig_dusun = DynamicRelationField("SigDusunSerializer", deferred=True, embed=True)

    class Meta:
        model = SigDukuh
        name = "data"
        exclude = []


class SigRwSerializer(CustomSerializer):
    sig_dukuh = DynamicRelationField("SigDukuhSerializer", deferred=True, embed=True)

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


class SigKawasanHutanSerializer(CustomSerializer):
    class Meta:
        model = SigKawasanHutan
        name = "data"
        exclude = []


class SigPenggunaanTanahSerializer(CustomSerializer):
    class Meta:
        model = SigPenggunaanTanah
        name = "data"
        exclude = []


class SigStatusTanahSerializer(CustomSerializer):
    class Meta:
        model = SigStatusTanah
        name = "data"
        exclude = []


class SigPemilikSerializer(CustomSerializer):
    pemilik = DynamicRelationField("SadPendudukSerializer", deferred=True, embed=True)

    class Meta:
        model = SigPemilik
        name = "data"
        exclude = []


class PemilikBidangSerializer(serializers.Serializer):
    nik = serializers.CharField(allow_null=True, allow_blank=True)
    nama = serializers.CharField()
    namabidang = serializers.CharField()
    is_warga = serializers.BooleanField(default=False)


class PenguasaBidangSerializer(serializers.Serializer):
    no_kk = serializers.CharField()
    is_warga = serializers.BooleanField(default=False)
    kepala_keluarga = serializers.CharField(required=False)


class SigBidangSerializerMini(CustomSerializer):
    sig_rt = DynamicRelationField("SigRtSerializer", deferred=False, embed=True)
    sig_dusun = DynamicRelationField("SigDusunSerializer", deferred=True, embed=True)
    alamat_lengkap = serializers.CharField(read_only=True)

    class Meta:
        model = SigBidang
        name = "data"
        fields = [
            "id",
            "nbt",
            "longitude",
            "latitude",
            "gambar_atas",
            "gambar_depan",
            "daftar_pemilik",
            "daftar_penguasa",
            "geometry",
            "sig_rt",
            "sig_dusun",
            "alamat_lengkap",
        ]


class SigBidangSerializerFull(CustomSerializer):
    sig_rt = DynamicRelationField("SigRtSerializer", deferred=False, embed=True)
    sig_dusun = DynamicRelationField("SigDusunSerializer", deferred=True, embed=True)
    daftar_pemilik = serializers.ListField(
        child=PemilikBidangSerializer(), required=False
    )
    daftar_penguasa = serializers.ListField(
        child=PenguasaBidangSerializer(), required=False
    )
    alamat_lengkap = serializers.CharField(read_only=True)

    class Meta:
        model = SigBidang
        name = "data"
        fields = [
            "id",
            "nbt",
            "gambar_atas",
            "gambar_depan",
            "sig_rt",
            "sig_dusun",
            "daftar_pemilik",
            "daftar_penguasa",
            "alamat_lengkap",
        ]


class SigSadBidangSerializer(CustomSerializer):
    sad_penduduk = DynamicRelationField(
        "SadPendudukSerializer", deferred=True, embed=True
    )
    sig_bidang = DynamicRelationField("SigBidangSerializer", deferred=True, embed=True)

    class Meta:
        model = SigSadBidang
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


class StatusLaporSerializer(DynamicModelSerializer):
    class Meta:
        model = StatusLapor
        name = "data"
        exclude = []


class LaporSerializer(CustomSerializer):
    kategori = DynamicRelationField(
        "KategoriLaporSerializer", deferred=True, embed=True
    )
    status = DynamicRelationField("StatusLaporSerializer", deferred=True, embed=True)

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


class KategoriPendapatanSerializer(DynamicModelSerializer):
    class Meta:
        model = KategoriPendapatan
        name = "data"
        exclude = []


class KategoriTahunSerializer(DynamicModelSerializer):
    class Meta:
        model = KategoriTahun
        name = "data"
        exclude = []


class KategoriBelanjaSerializer(DynamicModelSerializer):
    class Meta:
        model = KategoriBelanja
        name = "data"
        exclude = []


class PendapatanSerializer(DynamicModelSerializer):
    kategori = DynamicRelationField(
        "KategoriPendapatanSerializer", deferred=True, embed=True
    )
    tahun = DynamicRelationField("KategoriTahunSerializer", deferred=True, embed=True)

    class Meta:
        model = Pendapatan
        name = "data"
        exclude = []


class BelanjaSerializer(DynamicModelSerializer):
    kategori = DynamicRelationField(
        "KategoriBelanjaSerializer", deferred=True, embed=True
    )
    tahun = DynamicRelationField("KategoriTahunSerializer", deferred=True, embed=True)

    class Meta:
        model = Belanja
        name = "data"
        exclude = []


class SuratMasukSerializer(DynamicModelSerializer):
    class Meta:
        model = SuratMasuk
        name = "data"
        exclude = []


class SuratKeluarSerializer(DynamicModelSerializer):
    class Meta:
        model = SuratKeluar
        name = "data"
        exclude = []


class PekerjaanSerializer(DynamicModelSerializer):
    class Meta:
        model = Pekerjaan
        name = "data"
        exclude = []


class PendidikanSerializer(DynamicModelSerializer):
    class Meta:
        model = Pendidikan
        name = "data"
        exclude = []


class AgamaSerializer(DynamicModelSerializer):
    class Meta:
        model = Agama
        name = "data"
        exclude = []


class KelainanFisikSerializer(DynamicModelSerializer):
    class Meta:
        model = KelainanFisik
        name = "data"
        exclude = []


class CacatSerializer(DynamicModelSerializer):
    class Meta:
        model = Cacat
        name = "data"
        exclude = []


class StatusPerkawinanSerializer(DynamicModelSerializer):
    class Meta:
        model = StatusPerkawinan
        name = "data"
        exclude = []


class KewarganegaraanSerializer(DynamicModelSerializer):
    class Meta:
        model = Kewarganegaraan
        name = "data"
        exclude = []


class GoldarSerializer(DynamicModelSerializer):
    class Meta:
        model = Goldar
        name = "data"
        exclude = []


class StatusDlmKeluargaSerializer(DynamicModelSerializer):
    class Meta:
        model = StatusDlmKeluarga
        name = "data"
        exclude = []


class StatusKesejahteraanSerializer(DynamicModelSerializer):
    class Meta:
        model = StatusKesejahteraan
        name = "data"
        exclude = []


class StatusWargaSerializer(DynamicModelSerializer):
    class Meta:
        model = StatusWarga
        name = "data"
        exclude = []


class StatusDatangMasukSerializer(DynamicModelSerializer):
    class Meta:
        model = StatusDatangMasuk
        name = "data"
        exclude = []


class AsalSerializer(DynamicModelSerializer):
    class Meta:
        model = Asal
        name = "data"
        exclude = []


class KeadaanAwalSerializer(DynamicModelSerializer):
    class Meta:
        model = KeadaanAwal
        name = "data"
        exclude = []


class JabatanSerializer(DynamicModelSerializer):
    class Meta:
        model = Jabatan
        name = "data"
        exclude = []


class StatusPnsSerializer(DynamicModelSerializer):
    class Meta:
        model = StatusPns
        name = "data"
        exclude = []


class GolonganSerializer(DynamicModelSerializer):
    class Meta:
        model = Golongan
        name = "data"
        exclude = []


class JenisKelahiranSerializer(DynamicModelSerializer):
    class Meta:
        model = JenisKelahiran
        name = "data"
        exclude = []


class JenisTempatSerializer(DynamicModelSerializer):
    class Meta:
        model = JenisTempat
        name = "data"
        exclude = []


class TenagaKesehatanSerializer(DynamicModelSerializer):
    class Meta:
        model = TenagaKesehatan
        name = "data"
        exclude = []


class AbsensiSerializer(DynamicModelSerializer):
    pegawai = DynamicRelationField("PegawaiSerializer", deferred=True, embed=True)

    class Meta:
        model = Absensi
        name = "data"
        exclude = []


class AlasanIzinSerializer(DynamicModelSerializer):
    class Meta:
        model = AlasanIzin
        name = "data"
        exclude = []


class LaporanAbsensiSerializer(DynamicModelSerializer):
    class Meta:
        model = Absensi
        name = "data"
        exclude = []


class DashboardSerializer(serializers.Serializer):
    dusun = serializers.IntegerField()
    penduduk = serializers.IntegerField()
    keluarga = serializers.IntegerField()


class CctvSerializer(DynamicModelSerializer):
    class Meta:
        model = Cctv
        name = "data"
        exclude = []
