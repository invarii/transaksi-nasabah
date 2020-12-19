from django.utils import timezone
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicRelationField
from rest_framework import serializers
from .models import (
    Pegawai,
    SadProvinsi,
    SadKabKota,
    SadKecamatan,
    SadDesa,
    BatasDesa,
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
    SigPemilik,
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
    SuratKelahiran,
    SuratSkck,
    SuratDomisili,
    JenisPindah,
    KlasifikasiPindah,
    AlasanPindah,
    StatusKKTinggal,
    StatusKKPindah,
)

util_columns = [
    "created_by",
    "updated_by",
    "deleted_by",
    "created_at",
    "updated_at",
    "deleted_at",
]

status_keluarga = [
    "Kepala Keluarga",
    "Suami",
    "Istri",
    "Anak",
    "Menantu",
    "Cucu",
    "Orang Tua",
    "Famili Lain",
    "Lainnya",
]


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


class JenisPindahSerializer(CustomSerializer):
    class Meta:
        model = JenisPindah
        name = "data"
        exclude = []


class AlasanPindahSerializer(CustomSerializer):
    class Meta:
        model = AlasanPindah
        name = "data"
        exclude = []


class KlasifikasiPindahSerializer(CustomSerializer):
    class Meta:
        model = KlasifikasiPindah
        name = "data"
        exclude = []


class StatusKKTinggalSerializer(CustomSerializer):
    class Meta:
        model = StatusKKTinggal
        name = "data"
        exclude = []


class StatusKKPindahSerializer(CustomSerializer):
    class Meta:
        model = StatusKKPindah
        name = "data"
        exclude = []


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
    kecamatan_id = serializers.IntegerField(
        source="kecamatan.id", read_only=True
    )

    class Meta:
        model = SadDesa
        name = "data"
        exclude = ["kecamatan"]


class BatasDesaSerializer(CustomSerializer):
    desa = DynamicRelationField(
        "SadDesaSerializer", deferred=False, embed=True
    )

    class Meta:
        model = BatasDesa
        name = "data"
        exclude = []


class SadDusunSerializer(CustomSerializer):
    class Meta:
        model = SadDusun
        name = "data"
        exclude = []


class SadRwSerializer(CustomSerializer):
    dusun = DynamicRelationField("SadDusunSerializer", deferred=False)

    class Meta:
        model = SadRw
        name = "data"
        exclude = []


class SadRtSerializer(CustomSerializer):
    rw = DynamicRelationField("SadRwSerializer", deferred=False)

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
    kelurahan_tujuan = DynamicRelationField(SadDesaSerializer)
    anggota_pindah = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    def create(self, validated_data):
        nik_pindah = validated_data.pop("anggota_pindah")

        validated_data["nik_pindah"] = ",".join(str(i) for i in nik_pindah)
        sad_pindah = SadPindahKeluar.objects.create(**validated_data)

        keluarga_id = validated_data.get("nomor_kk")
        keluarga = SadKeluarga.objects.get(no_kk=keluarga_id)

        if validated_data.get("status_kk_pindah"):
            if validated_data["status_kk_pindah"].nama == "kk_baru":
                penduduk_pindah = keluarga.anggota.filter(pk__in=nik_pindah)
                for penduduk in penduduk_pindah:
                    penduduk.deleted_at = timezone.now()
                    penduduk.deleted_by = self.context["request"].user
                    penduduk.save()
        if validated_data.get("status_kk_tinggal"):
            if validated_data["status_kk_tinggal"].nama == "kk_baru":
                penduduk_tinggal = keluarga.anggota.exclude(pk__in=nik_pindah)
                for penduduk in penduduk_tinggal:
                    penduduk.deleted_at = timezone.now()
                    penduduk.deleted_by = self.context["request"].user
                    penduduk.save()
        keluarga.refresh_from_db()
        if not keluarga.anggota.count():
            keluarga.deleted_at = timezone.now()
            keluarga.deleted_by = self.context["request"].user
            keluarga.save()
        sad_pindah.save()
        return sad_pindah

    class Meta:
        model = SadPindahKeluar
        name = "data"
        exclude = util_columns + ["nik_pindah"]


class MiniUserSerializer(DynamicModelSerializer):
    status_dalam_keluarga = serializers.ChoiceField(status_keluarga)

    class Meta:
        model = SadPenduduk
        fields = ["nik", "nama", "tgl_lahir", "status_dalam_keluarga"]


def create_or_reactivate(model, filter_param, data):
    instance = model.all_objects.filter(**filter_param).dead().first()

    if instance:
        instance.deleted_by = None
        instance.deleted_at = None
        instance.save()

        model.objects.filter(pk=instance.pk).update(**data)
        instance.refresh_from_db()
    else:
        instance = model.objects.create(**data)
    instance.save()
    return instance


def create_or_reactivate_user(username, password):
    user = User.objects.filter(username=username).first()
    group = Group.objects.get(name="penduduk")

    if not user:
        user = User.objects.create(username=username)
        user.set_password(password)
        user.groups.add(group)
        user.save()
    elif not user.is_active:
        user.is_active = True
        user.set_password(password)
        user.save()
    return user


class SadPindahMasukSerializer(CustomSerializer):
    rt_id = DynamicRelationField(SadRtSerializer)
    anggota = serializers.ListField(
        child=MiniUserSerializer(), write_only=True
    )

    def create(self, validated_data):
        anggota = validated_data.pop("anggota")

        print("This 0")
        if SadKeluarga.objects.filter(no_kk=validated_data["no_kk"]).exists():
            print("This x")
            raise APIException("Nomor KK Sudah terdaftar", 400)

        sad_masuk = SadPindahMasuk.objects.create(**validated_data)

        keluarga_data = validated_data.copy()
        print("This 1")
        print(keluarga_data)
        keluarga_data["status_kk"] = keluarga_data.pop(
            "status_kk_pindah"
        ).label
        keluarga_data["rt"] = keluarga_data.pop("rt_id")
        keluarga_data.pop("tanggal_kedatangan")
        keluarga_filter = {"no_kk": keluarga_data["no_kk"]}
        try:
            keluarga = create_or_reactivate(
                SadKeluarga, keluarga_filter, keluarga_data
            )
        except Exception:
            return Response({"msg": "Gagal menyimpan data keluarga"}, 400)
        keluarga.save()

        for item in anggota:
            penduduk_filter = {"nik": item["nik"]}
            try:
                penduduk = create_or_reactivate(
                    SadPenduduk, penduduk_filter, item
                )
            except Exception:
                keluarga.delete()
                return Response({"msg": "Data Penduduk Gagal"})
            print(str(item["tgl_lahir"]))
            user = create_or_reactivate_user(
                item["nik"], str(item["tgl_lahir"]).replace("-", "")
            )
            penduduk.user = user
            penduduk.save()
        print("This 2")

        sad_masuk.save()
        return sad_masuk

    class Meta:
        model = SadPindahMasuk
        name = "data"
        exclude = util_columns + ["nik_datang"]


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


class SigPemilikSerializer(CustomSerializer):
    pemilik = DynamicRelationField(
        "SadPendudukSerializer", deferred=True, embed=True
    )

    class Meta:
        model = SigPemilik
        name = "data"
        exclude = []


class SigBidangSerializer(CustomSerializer):
    sig_rt = DynamicRelationField("SigRtSerializer", deferred=True, embed=True)
    pemilik_warga = DynamicRelationField(
        "SigPemilikSerializer", deferred=True, embed=True
    )

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
    kategori = serializers.IntegerField(source="kategori.id", read_only=True)

    class Meta:
        model = Potensi
        name = "data"
        exclude = []


class AdminSuratKelahiranSerializer(DynamicModelSerializer):
    pegawai = DynamicRelationField(PegawaiSerializer)

    class Meta:
        model = SuratKelahiran
        name = "data"
        include = ["pegawai"]
        exclude = [
            "created_by",
            "created_at",
            "updated_at",
            "deleted_by",
            "deleted_at",
        ]
        read_only_fields = [
            "ayah",
            "ibu",
            "saksi1",
            "saksi2",
            "nama",
            "jk",
            "tempat_dilahirkan",
            "tempat_kelahiran",
            "tgl",
            "jenis_kelahiran",
            "kelahiran_ke",
            "penolong_kelahiran",
            "berat",
            "panjang",
        ]


class AdminSuratSkckSerializer(DynamicModelSerializer):
    nama = serializers.CharField(source="penduduk.nama", read_only=True)
    tempat_lahir = serializers.CharField(
        source="penduduk.tempat_lahir", read_only=True
    )
    jenis_kelamin = serializers.CharField(source="penduduk.jk", read_only=True)
    kewarganegaraan = serializers.CharField(
        source="penduduk.kewargananegaraan", read_only=True
    )
    agama = serializers.CharField(source="penduduk.agama", read_only=True)
    status_kawin = serializers.CharField(
        source="penduduk.status_kawin", read_only=True
    )
    pekerjaan = serializers.CharField(
        source="penduduk.pekerjaan", read_only=True
    )
    pendidikan = serializers.CharField(
        source="penduduk.pendidikan", read_only=True
    )
    no_ktp = serializers.CharField(source="penduduk.nik", read_only=True)
    no_kk = serializers.CharField(
        source="penduduk.keluarga.no_kk", read_only=True
    )
    alamat = serializers.CharField(source="penduduk.alamat", read_only=True)

    class Meta:
        model = SuratSkck
        name = "data"
        exclude = [
            "penduduk",
            "created_by",
            "created_at",
            "updated_at",
            "updated_by",
            "deleted_by",
            "deleted_at",
        ]
        read_only_fields = ["keperluan", "keterangan"]


class AdminSuratDomisiliSerializer(DynamicModelSerializer):
    nama = serializers.CharField(source="penduduk.nama", read_only=True)
    no_ktp = serializers.CharField(source="penduduk.nik", read_only=True)
    jenis_kelamin = serializers.CharField(source="penduduk.jk", read_only=True)
    status_kawin = serializers.CharField(
        source="penduduk.status_kawin", read_only=True
    )
    pekerjaan = serializers.CharField(
        source="penduduk.pekerjaan", read_only=True
    )
    agama = serializers.CharField(source="penduduk.agama", read_only=True)
    alamat = serializers.CharField(source="penduduk.alamat", read_only=True)

    class Meta:
        model = SuratDomisili
        name = "data"
        exclude = [
            "penduduk",
            "created_by",
            "created_at",
            "updated_at",
            "updated_by",
            "deleted_by",
            "deleted_at",
        ]
        read_only_fields = ["keperluan", "penduduk"]


class SuratMeta:
    name = "data"
    exclude = [
        "pegawai",
        "no_surat",
        "created_by",
        "created_at",
        "deleted_by",
        "deleted_at",
        "updated_by",
        "updated_at",
    ]


class SuratKelahiranSerializer(CustomSerializer):
    class Meta(SuratMeta):
        model = SuratKelahiran


class SuratSkckSerializer(CustomSerializer):
    class Meta(SuratMeta):
        model = SuratSkck

    def create(self, validated_data):
        surat = SuratSkck(**validated_data)
        surat.created_by = self.context["request"].user
        surat.penduduk = self.context["request"].user.profile
        surat.save()
        return surat


class SuratDomisiliSerializer(CustomSerializer):
    class Meta(SuratMeta):
        model = SuratDomisili

    def create(self, validated_data):
        surat = SuratDomisili(**validated_data)
        surat.created_by = self.context["request"].user
        surat.penduduk = self.context["request"].user.profile
        surat.save()
        return surat
