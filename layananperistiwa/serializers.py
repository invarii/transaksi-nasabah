from rest_framework import serializers

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicRelationField

from api_sad_sig.util import (
    CustomSerializer,
    util_columns,
    create_or_reactivate,
    create_or_reactivate_user,
)
from v1.models import SadKeluarga, SadPenduduk, Alamat
from v1.serializers import (
    PegawaiSerializer,
    SadDesaSerializer,
)

from .models import (
    SuratDomisili,
    SuratKelahiran,
    SuratSkck,
    SadKelahiran,
    SadKematian,
    SadLahirmati,
    SadPindahKeluar,
    SadPindahMasuk,
    JenisPindah,
    AlasanPindah,
    KlasifikasiPindah,
    StatusKKPindah,
    StatusKKTinggal,
    SadPecahKK,
)

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


class AdminSuratKelahiranSerializer(DynamicModelSerializer):
    pegawai = DynamicRelationField(PegawaiSerializer)
    keterangan_penolong_kelahiran = serializers.CharField(read_only=True)
    keterangan_tempat_dilahirkan = serializers.CharField(read_only=True)
    keterangan_jenis_kelahiran = serializers.CharField(read_only=True)

    class Meta:
        model = SuratKelahiran
        name = "data"
        include = ["pegawai"]
        exclude = []


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
        exclude = []


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
        exclude = []


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


jenis_kelahiran = ["Tunggal", "Kembar 2", "Kembar 3", "Kembar 4", "Lainnya"]
tempat_dilahirkan = ["RS/RB", "Puskesmas", "Polindes", "Rumah", "Lainnya"]
jenis_kelamin = ["Laki-laki", "Perempuan"]
penolong_kelahiran = ["Dokter", "Bidan/Perawat", "Dukun", "Lainnya"]


class SuratKelahiranSerializer(CustomSerializer):
    jk = serializers.ChoiceField(jenis_kelamin)
    keterangan_penolong_kelahiran = serializers.CharField(read_only=True)
    keterangan_tempat_dilahirkan = serializers.CharField(read_only=True)
    keterangan_jenis_kelahiran = serializers.CharField(read_only=True)

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


class OrangTuaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SadPenduduk
        fields = ["nik", "nama", "tempat_lahir", "tgl_lahir", "alamat"]


class LaporanMonografiSerializer(CustomSerializer):
    class Meta:
        model = SadPenduduk
        name = "data"
        fields = ["no_kk", "nik", "nama", "jk", "status_kawin", "alamat"]


class LaporanKelahiranSerializer(CustomSerializer):
    tanggal_kawin = serializers.CharField()

    class Meta:
        model = SadKelahiran
        name = "data"
        exclude = util_columns + [
            "nama_pelapor",
            "nik_saksi_satu",
            "nik_saksi_dua",
        ]


class SadKelahiranSerializer(CustomSerializer):
    class Meta:
        model = SadKelahiran
        name = "data"
        exclude = []


class PendudukMeninggal(CustomSerializer):
    class Meta:
        model = SadPenduduk
        name = "data"
        fields = [
            "nama",
            "nik",
            "jk",
            "tempat_lahir",
            "tgl_lahir",
            "pekerjaan",
            "alamat",
            "no_kk",
        ]


class LaporanKematianSerializer(CustomSerializer):
    nama = serializers.CharField(source="penduduk.nama", read_only=True)
    nik = serializers.CharField(source="penduduk.nik", read_only=True)
    jenis_kelamin = serializers.CharField(source="penduduk.jk", read_only=True)
    tgl_lahir = serializers.CharField(
        source="penduduk.tgl_lahir", read_only=True
    )
    pekerjaan = serializers.CharField(
        source="penduduk.pekerjaan", read_only=True
    )
    alamat = serializers.CharField(source="penduduk.alamat", read_only=True)
    no_kk = serializers.CharField(
        source="penduduk.keluarga.no_kk", read_only=True
    )

    class Meta:
        model = SadKematian
        name = "data"
        exclude = util_columns + [
            "nama_saksi_satu",
            "nama_saksi_dua",
            "nama_pelapor",
        ]


class SadKematianSuratSerializer(DynamicModelSerializer):
    penduduk = DynamicRelationField(
        "v1.serializers.SadPendudukMiniSerializer", deferred=False, embed=True
    )

    class Meta:
        model = SadKematian
        name = "data"
        fields = ["penduduk", "tanggal_kematian"]

class SadKematianSerializer(CustomSerializer):
    nama = serializers.CharField(source="penduduk.nama", read_only=True)
    nik = serializers.CharField(source="penduduk.nik", read_only=True)
    jenis_kelamin = serializers.CharField(source="penduduk.jk", read_only=True)
    tgl_lahir = serializers.CharField(
        source="penduduk.tgl_lahir", read_only=True
    )
    pekerjaan = serializers.CharField(
        source="penduduk.pekerjaan", read_only=True
    )
    alamat = serializers.CharField(source="penduduk.alamat", read_only=True)
    no_kk = serializers.CharField(
        source="penduduk.keluarga.no_kk", read_only=True
    )

    def create(self, validated_data):
        obj = SadKematian(**validated_data)
        obj.save()
        obj.penduduk.delete()
        obj.penduduk.save()
        return obj

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
    kelurahan_tujuan = DynamicRelationField(
        SadDesaSerializer, deferred=False, embed=True
    )
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


class SadPindahMasukSerializer(CustomSerializer):
    status_kk_pindah = DynamicRelationField(
        "StatusKKPindahSerializer", deferred=False, embed=True, write_only=True
    )
    anggota = serializers.ListField(
        child=MiniUserSerializer(), write_only=True
    )
    nama_alamat = serializers.CharField(write_only=True)
    rt_id = serializers.IntegerField(write_only=True, required=False)
    dusun_id = serializers.IntegerField(write_only=True, required=False)

    def create(self, validated_data):
        anggota = validated_data.pop("anggota")

        print("This 0")
        if SadKeluarga.objects.filter(no_kk=validated_data["no_kk"]).exists():
            print("This x")
            raise APIException("Nomor KK Sudah terdaftar", 400)

        data_alamat = {
            "rt": validated_data.pop("rt_id", None),
            "dusun": validated_data.pop("dusun_id", None),
        }
        nama_alamat = validated_data.pop("nama_alamat")
        if not data_alamat.get("rt") and not data_alamat.get("dusun"):
            raise APIException("Need dusun_id or rt_id", 400)

        keluarga_data = validated_data.copy()
        print("This 1")
        keluarga_data["status_kk"] = keluarga_data.pop(
            "status_kk_pindah"
        ).label

        keluarga_data.pop("tanggal_kedatangan")
        keluarga_filter = {"no_kk": keluarga_data["no_kk"]}
        try:
            keluarga = create_or_reactivate(
                SadKeluarga, keluarga_filter, keluarga_data
            )
            print(keluarga_data)
        except Exception:
            return Response({"msg": "Gagal menyimpan data keluarga"}, 400)
        keluarga.save()

        rt_id = data_alamat.get("rt")
        dusun_id = data_alamat.get("dusun_id")
        if keluarga.alamat:
            if rt_id:
                keluarga.alamat.set_from_rt(rt_id)
            else:
                keluarga.alamat.set_from_dusun(dusun_id)
        else:
            keluarga.alamat = Alamat()
            if rt_id:
                keluarga.alamat.set_from_rt(rt_id)
            else:
                keluarga.alamat.set_from_dusun(dusun_id)
        keluarga.alamat.alamat = nama_alamat
        keluarga.alamat.save()
        print(validated_data)
        sad_masuk = SadPindahMasuk(**validated_data)
        sad_masuk.alamat = keluarga.alamat

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
            penduduk.keluarga = keluarga
            penduduk.save()
        print("This 2")

        sad_masuk.save()
        return sad_masuk

    class Meta:
        model = SadPindahMasuk
        name = "data"
        exclude = util_columns + ["nik_datang"]


class MiniPendudukSerializer(serializers.Serializer):
    nik = serializers.CharField(write_only=True)
    status_dalam_keluarga = serializers.ChoiceField(
        status_keluarga, write_only=True
    )


class PecahKKPenduduk(serializers.ModelSerializer):
    class Meta:
        model = SadPenduduk
        fields = ["nama", "nik"]
        read_only_fields = ["nama", "nik"]


class PecahKKKeluarga(serializers.ModelSerializer):
    class Meta:
        model = SadKeluarga
        fields = ["kepala_keluarga", "no_kk"]
        read_only_fields = ["kepala_keluarga", "no_kk"]


class SadPecahKKSerializer(CustomSerializer):
    no_kk = serializers.CharField(write_only=True)
    anggota_kk = MiniPendudukSerializer(many=True, write_only=True)
    rt = serializers.IntegerField(write_only=True, required=False)
    dusun = serializers.IntegerField(write_only=True, required=False)
    penduduk = PecahKKPenduduk(many=True, read_only=True)
    keluarga = PecahKKKeluarga(read_only=True)

    def create(self, validated_data):
        rt = validated_data.get("rt")
        dusun = validated_data.get("dusun")
        if not rt and not dusun:
            raise APIException("Need rt or dusun")

        alamat = Alamat()
        if rt:
            alamat.set_from_rt(rt)
        else:
            alamat.set_from_dusun(dusun)

        new_kk = SadKeluarga(no_kk=validated_data["no_kk"])
        new_kk.save()

        alamat.save()
        new_kk.alamat = alamat
        new_kk.save()

        pecahkk_record = SadPecahKK(keluarga=new_kk)
        pecahkk_record.save()

        for item in validated_data["anggota_kk"]:
            penduduk = SadPenduduk.objects.filter(nik=item["nik"]).first()
            if not penduduk:
                continue

            penduduk.status_dalam_keluarga = item["status_dalam_keluarga"]
            penduduk.keluarga = new_kk
            penduduk.save()

            pecahkk_record.penduduk.add(penduduk)

        return pecahkk_record

    class Meta:
        model = SadPecahKK
        name = "data"
        read_only_fields = ["keluarga", "penduduk"]
        exclude = util_columns
