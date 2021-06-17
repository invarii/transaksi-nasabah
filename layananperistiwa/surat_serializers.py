import locale
from datetime import datetime

from rest_framework import serializers
from dynamic_rest.fields import DynamicRelationField


from api_sad_sig.util import (
    CustomSerializer,
)
from v1.models import SadPenduduk, SadDusun, Pegawai
from v1.serializers import SadPendudukMiniSerializer, SadDusunSerializer
from .models import LayananSurat, SadKematian, SadKelahiran
from .serializers import SadKematianSuratSerializer, SadKelahiranSerializer


class PendudukListSurat(CustomSerializer):
    class Meta:
        model = SadPenduduk
        fields = ["id", "nik", "nama"]


class PegawaiListSurat(CustomSerializer):
    class Meta:
        model = Pegawai
        fields = ["id", "nip", "nama", "jabatan"]


class ListSuratSerializer(CustomSerializer):
    pemohon = DynamicRelationField(
        "PendudukListSurat", source="penduduk", deferred=False, embed=True
    )
    pegawai = DynamicRelationField(
        "PegawaiListSurat", deferred=False, embed=True
    )

    class Meta:
        model = LayananSurat
        name = "data"
        exclude = [
            "atribut",
            "jenis",
            "created_by",
            "created_at",
            "deleted_by",
            "deleted_at",
            "updated_by",
            "updated_at",
        ]


class BaseAdminSuratSerializer(CustomSerializer):
    pemohon = DynamicRelationField(
        "PendudukListSurat", source="penduduk", deferred=False, embed=True
    )
    pegawai = DynamicRelationField(
        "PegawaiListSurat", deferred=False, embed=True
    )

    def create(self, data):
        surat = LayananSurat(jenis=self.Meta.jenis_surat, **data)
        if not data.get("atribut"):
            surat.atribut = {}
        surat.save()
        return surat

    class Meta:
        model = LayananSurat
        name = "data"
        exclude = [
            "penduduk",
            "jenis",
            "created_by",
            "created_at",
            "deleted_by",
            "deleted_at",
            "updated_by",
            "updated_at",
        ]


class BasePendudukSuratSerializer(CustomSerializer):
    def create(self, data):
        surat = LayananSurat(jenis=self.Meta.jenis_surat, **data)
        surat.penduduk = self.context["request"].user.profile
        if not data.get("atribut"):
            surat.atribut = {}
        surat.save()
        return surat

    class Meta:
        model = LayananSurat
        name = "data"
        exclude = [
            "pegawai",
            "penduduk",
            "no_surat",
            "jenis",
            "created_by",
            "created_at",
            "deleted_by",
            "deleted_at",
            "updated_by",
            "updated_at",
        ]


class AtributHakMilikTanah(serializers.Serializer):
    luas_tanah_angka = serializers.IntegerField()
    luas_tanah_kalimat = serializers.CharField()
    dusun_id = serializers.IntegerField()
    batas_utara = serializers.CharField()
    batas_selatan = serializers.CharField()
    batas_timur = serializers.CharField()
    batas_barat = serializers.CharField()
    nama_saksi1 = serializers.CharField()
    nama_saksi2 = serializers.CharField()
    nama_saksi3 = serializers.CharField()
    dusun = serializers.SerializerMethodField()

    def get_dusun(self, obj):
        if not obj.get("dusun_id", None):
            return {}
        inst = SadDusun.objects.get(pk=obj["dusun_id"])
        return SadDusunSerializer(inst).data


class AdminHakMilikTanahSerializer(BaseAdminSuratSerializer):
    atribut = AtributHakMilikTanah()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "shm"


class PendudukHakMilikTanahSerializer(BasePendudukSuratSerializer):
    atribut = AtributHakMilikTanah()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "shm"


class AtributSKCK(serializers.Serializer):
    keperluan = serializers.CharField(required=False)
    keterangan = serializers.CharField(required=False)


class AdminSKCKSerializer(BaseAdminSuratSerializer):
    atribut = AtributSKCK()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "skck"


class PendudukSKCKSerializer(BasePendudukSuratSerializer):
    atribut = AtributSKCK()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "skck"


class AtributDomisili(serializers.Serializer):
    keperluan = serializers.CharField()


class AdminDomisiliSerializer(BaseAdminSuratSerializer):
    atribut = AtributDomisili()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "domisili"


class PendudukDomisiliSerializer(BasePendudukSuratSerializer):
    atribut = AtributDomisili()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "domisili"


class AtributUsaha(serializers.Serializer):
    nama_usaha = serializers.CharField()


class AdminUsahaSerializer(BaseAdminSuratSerializer):
    atribut = AtributUsaha()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "usaha"


class PendudukUsahaSerializer(BasePendudukSuratSerializer):
    atribut = AtributUsaha()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "usaha"


class AtributRapidTest(serializers.Serializer):
    tempat_rapid_test = serializers.CharField()


class AdminRapidTestSerializer(BaseAdminSuratSerializer):
    atribut = AtributRapidTest()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "rapidtest"


class PendudukRapidTestSerializer(BasePendudukSuratSerializer):
    atribut = AtributRapidTest()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "rapidtest"


class AdminKetPendudukSerializer(BaseAdminSuratSerializer):
    atribut = serializers.DictField(required=False)

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "ket_penduduk"


class PendudukKetPendudukSerializer(BasePendudukSuratSerializer):
    atribut = serializers.DictField(required=False)

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "ket_penduduk"


class AdminTempatTinggalSerializer(BaseAdminSuratSerializer):
    atribut = serializers.DictField(required=False)

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "ktt"


class PendudukTempatTinggalSerializer(BasePendudukSuratSerializer):
    atribut = serializers.DictField(required=False)

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "ktt"


class AtributLuarDaerah(serializers.Serializer):
    nama_daerah = serializers.CharField()
    jenis_perjalanan = serializers.CharField()
    jenis_rangka_perjalanan = serializers.CharField()


class AdminLuarDaerahSerializer(BaseAdminSuratSerializer):
    atribut = AtributLuarDaerah()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "kld"


class PendudukLuarDaerahSerializer(BasePendudukSuratSerializer):
    atribut = AtributLuarDaerah()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "kld"


class AtributKetSiswaTidakMampu(serializers.Serializer):
    orangtua_id = serializers.IntegerField()
    orangtua = serializers.SerializerMethodField()

    def get_orangtua(self, obj):
        penduduk = SadPenduduk.objects.get(pk=obj["orangtua_id"])
        return SadPendudukMiniSerializer(penduduk).data


class AdminKetSiswaTidakMampuSerializer(BaseAdminSuratSerializer):
    atribut = AtributKetSiswaTidakMampu()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "sktm"


class PendudukKetSiswaTidakMampuSerializer(BasePendudukSuratSerializer):
    atribut = AtributKetSiswaTidakMampu()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "sktm"


class AdminBelumMenikahSerializer(BaseAdminSuratSerializer):
    atribut = AtributKetSiswaTidakMampu()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "belummenikah"


class PendudukBelumMenikahSerializer(BasePendudukSuratSerializer):
    atribut = AtributKetSiswaTidakMampu()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "belummenikah"


class AtributSuratPenguburan(serializers.Serializer):
    nama_jenazah = serializers.CharField()
    tanggal_penguburan = serializers.CharField()
    tanggal = serializers.SerializerMethodField()

    def get_tanggal(self, obj):
        return datetime.strptime(obj["tanggal_penguburan"], "%Y-%m-%d")


class AdminSuratPenguburanSerializer(BaseAdminSuratSerializer):
    atribut = AtributSuratPenguburan()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "penguburan"


class PendudukSuratPenguburanSerializer(BasePendudukSuratSerializer):
    atribut = AtributSuratPenguburan()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "penguburan"


class AtributPelakuPerikananSerializer(serializers.Serializer):
    orangtua_id = serializers.IntegerField()
    orangtua = serializers.SerializerMethodField()
    keperluan = serializers.CharField()

    def get_orangtua(self, obj):
        penduduk = SadPenduduk.objects.get(pk=obj["orangtua_id"])
        return SadPendudukMiniSerializer(penduduk).data


class AdminPelakuPerikananSerializer(BaseAdminSuratSerializer):
    atribut = AtributPelakuPerikananSerializer()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "ketnelayan"


class PendudukPelakuPerikananSerializer(BasePendudukSuratSerializer):
    atribut = AtributPelakuPerikananSerializer()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "ketnelayan"


# Template not made yet
class AtributPernyataanKebenaranData(serializers.Serializer):
    keperluan = serializers.CharField(default="Seleksi Perguruan Tinggi")


class AdminPernyataanKebenaranSerializer(BaseAdminSuratSerializer):
    atribut = AtributPernyataanKebenaranData()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "spkd"


class PendudukPernyataanKebenaranSerializer(BasePendudukSuratSerializer):
    atribut = AtributPernyataanKebenaranData()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "spkd"


class AtributKelahiran(serializers.Serializer):
    kelahiran_id = serializers.IntegerField()
    kelahiran = serializers.SerializerMethodField()

    def get_kelahiran(self, obj):
        inst = SadKelahiran.objects.get(pk=obj["kelahiran_id"])
        return SadKelahiranSerializer(inst).data


class AdminSuratKelahiranSerializer(BaseAdminSuratSerializer):
    atribut = AtributKelahiran()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "kelahiran"


class PendudukSuratKelahiranSerializer(BasePendudukSuratSerializer):
    atribut = AtributKelahiran()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "kelahiran"


class AtributKematian(serializers.Serializer):
    kematian_id = serializers.IntegerField()
    kematian = serializers.SerializerMethodField()

    def get_kematian(self, obj):
        inst = SadKematian.objects.get(pk=obj["kematian_id"])
        return SadKematianSuratSerializer(inst).data


class AdminSuratKematianSerializer(BaseAdminSuratSerializer):
    atribut = AtributKematian()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "kematian"


class PendudukSuratKematianSerializer(BasePendudukSuratSerializer):
    atribut = AtributKematian()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "kematian"


class AtributIzinPesta(serializers.Serializer):
    tanggal = serializers.CharField()
    waktu_mulai = serializers.CharField()
    tempat = serializers.CharField()
    jenis_pesta = serializers.ListField(
        child=serializers.CharField(max_length=64)
    )

    tanggal_pesta = serializers.SerializerMethodField()

    def get_tanggal_pesta(self, obj):
        locale.setlocale(locale.LC_TIME, "id_ID.UTF-8")
        return datetime.strptime(obj["tanggal"], "%Y-%m-%d")


class AdminIzinPestaSerializer(BaseAdminSuratSerializer):
    atribut = AtributIzinPesta()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "izinpesta"


class PendudukIzinPestaSerializer(BasePendudukSuratSerializer):
    atribut = AtributIzinPesta()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "izinpesta"


class AtributIzinKeramaian(serializers.Serializer):
    tanggal = serializers.CharField()
    waktu_mulai = serializers.CharField()
    tempat = serializers.CharField()
    jenis_pesta = serializers.CharField()

    tanggal_pesta = serializers.SerializerMethodField()

    def get_tanggal_pesta(self, obj):
        locale.setlocale(locale.LC_TIME, "id_ID.UTF-8")
        return datetime.strptime(obj["tanggal"], "%Y-%m-%d")


class AdminIzinKeramaianSerializer(BaseAdminSuratSerializer):
    atribut = AtributIzinKeramaian()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "izinkeramaian"


class PendudukIzinKeramaianSerializer(BasePendudukSuratSerializer):
    atribut = AtributIzinKeramaian()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "izinkeramaian"


class AtributKehilangan(serializers.Serializer):
    nama_barang = serializers.CharField()
    detail_barang = serializers.CharField()


class AdminKehilanganSerializer(BaseAdminSuratSerializer):
    atribut = AtributKehilangan()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "kehilangan"


class PendudukKehilanganSerializer(BasePendudukSuratSerializer):
    atribut = AtributKehilangan()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "kehilangan"


class AtributDudaJanda(serializers.Serializer):
    nama_mantan_pasangan = serializers.CharField()
    tahun_berpisah = serializers.CharField()


class AdminDudaJandaSerializer(BaseAdminSuratSerializer):
    atribut = AtributDudaJanda()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "dudajanda"


class PendudukDudaJandaSerializer(BasePendudukSuratSerializer):
    atribut = AtributDudaJanda()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "dudajanda"


class AtributKeteranganPisah(serializers.Serializer):
    nama_pasangan = serializers.CharField()
    nama_instansi_pengadilan = serializers.CharField()
    keperluan = serializers.CharField()


class AdminKetPisahSerializer(BaseAdminSuratSerializer):
    atribut = AtributKeteranganPisah()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "ket_pisah"


class PendudukKetPisahSerializer(BasePendudukSuratSerializer):
    atribut = AtributKeteranganPisah()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "ket_pisah"


class DaftarKayu(serializers.Serializer):
    jenis = serializers.CharField()
    panjang = serializers.FloatField(required=False)
    lebar = serializers.FloatField(required=False)
    tebal = serializers.FloatField(required=False)
    jumlah = serializers.IntegerField()
    volume = serializers.SerializerMethodField()

    def get_volume(self, obj):
        if (
            obj.get("panjang", None)
            and obj.get("lebar", None)
            and obj.get("tebal", None)
        ):
            return obj["panjang"] * obj["lebar"] * obj["tebal"]
        return None


class AtributAsalUsulKayu(serializers.Serializer):
    nama = serializers.CharField()
    umur = serializers.IntegerField()
    pekerjaan = serializers.CharField()
    alamat = serializers.CharField()
    kota_tujuan = serializers.CharField()
    daftar_kayu = DaftarKayu(many=True)
    total_jumlah_kayu = serializers.SerializerMethodField()

    def get_total_jumlah_kayu(self, obj):
        total = 0
        for item in obj["daftar_kayu"]:
            total += item["jumlah"]
        return int(total)


class AdminSKAUSerializer(BaseAdminSuratSerializer):
    atribut = AtributAsalUsulKayu()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "skau"


class PendudukSKAUSerializer(BasePendudukSuratSerializer):
    atribut = AtributAsalUsulKayu()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "skau"


class PendudukMiniSuratSerializer(serializers.Serializer):
    nama = serializers.CharField()
    pekerjaan = serializers.CharField()
    umur = serializers.IntegerField()
    alamat = serializers.CharField()


class PasanganMeninggal(serializers.Serializer):
    nama = serializers.CharField()
    pekerjaan = serializers.CharField(required=False)
    umur = serializers.IntegerField(required=False)
    alamat = serializers.CharField(required=False)
    tanggal_meninggal = serializers.CharField(required=False)


class AtributAhliWaris(serializers.Serializer):
    kematian_id = serializers.IntegerField()
    pasangan = PasanganMeninggal()
    ahli_waris = PendudukMiniSuratSerializer(many=True)
    saksi = PendudukMiniSuratSerializer(many=True)

    kematian = serializers.SerializerMethodField()
    jumlah_ahliwaris = serializers.SerializerMethodField()

    def get_kematian(self, obj):
        kematian = SadKematian.objects.get(pk=obj["kematian_id"])
        return SadKematianSuratSerializer(kematian).data

    def get_jumlah_ahliwaris(self, obj):
        return len(obj["ahli_waris"])


class AdminAhliWarisSerializer(BaseAdminSuratSerializer):
    atribut = AtributAhliWaris()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "skaw"


class PendudukAhliWarisSerializer(BasePendudukSuratSerializer):
    atribut = AtributAhliWaris()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "skaw"


class AtributDokumenBedaNama(serializers.Serializer):
    nama_dokumen = serializers.CharField()
    nama_orang = serializers.CharField()


class AtributBedaNama(serializers.Serializer):
    dokumen_salah = AtributDokumenBedaNama()
    dokumen_benar = AtributDokumenBedaNama(required=False)
    penyebab = serializers.CharField(required=False)


class AdminBedaNamaSerializer(BaseAdminSuratSerializer):
    atribut = AtributBedaNama()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "bedanama"


class PendudukBedaNamaSerializer(BasePendudukSuratSerializer):
    atribut = AtributBedaNama()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "bedanama"


class AtributPerekaman(serializers.Serializer):
    nama_subject = serializers.CharField()
    keterangan = serializers.CharField()


class AdminPerekamanSerializer(BaseAdminSuratSerializer):
    atribut = AtributPerekaman()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "perekaman"


class PendudukPerekamanSerializer(BasePendudukSuratSerializer):
    atribut = AtributPerekaman()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "perekaman"


jenis_listriks = ["prabayar", "pascabayar"]


class AtributBalikNamaTokenListrik(serializers.Serializer):
    jenis_listrik = serializers.ChoiceField(jenis_listriks)
    nama_awal = serializers.CharField()
    id_pelanggan = serializers.CharField()
    daya_listrik = serializers.IntegerField()
    nama_cabang = serializers.CharField()


class AdminBalikNamaTokenListrik(BaseAdminSuratSerializer):
    atribut = AtributBalikNamaTokenListrik()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "bntl"


class PendudukBalikNamaTokenListrik(BasePendudukSuratSerializer):
    atribut = AtributBalikNamaTokenListrik()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "bntl"


class AdminSKTMKeluargaSerializer(BaseAdminSuratSerializer):
    atribut = serializers.DictField(required=False)

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "sktm_keluarga"


class PendudukSKTMKeluargaSerializer(BasePendudukSuratSerializer):
    atribut = serializers.DictField(required=False)

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "sktm_keluarga"


class BRISuratKuasa(serializers.Serializer):
    nama = serializers.CharField()
    umur = serializers.IntegerField()
    pekerjaan = serializers.CharField()
    alamat = serializers.CharField()
    objek_jaminan = serializers.CharField()


class AtributSuratBRI(serializers.Serializer):
    ibu_kandung = serializers.CharField()
    bantuan_kalimat = serializers.CharField()
    bantuan_angka = serializers.IntegerField()
    jangka_waktu = serializers.IntegerField()
    nama_usaha = serializers.CharField()
    unit_bri = serializers.CharField()
    lokasi_bri = serializers.CharField()
    surat_kuasa = BRISuratKuasa(required=False)
    daftar_lampiran = serializers.ListField(child=serializers.CharField())


class AdminPermohonanBRI(BaseAdminSuratSerializer):
    atribut = AtributSuratBRI()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "perm_bri"


class PendudukPermohonanBRI(BasePendudukSuratSerializer):
    atribut = AtributSuratBRI()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "perm_bri"


class AtributKeteranganAhliWaris(serializers.Serializer):
    kematian_id = serializers.IntegerField()
    kematian = serializers.SerializerMethodField()
    hubungan_dengan_almarhum = serializers.CharField()
    reg_dtks = serializers.CharField()

    def get_kematian(self, obj):
        inst = SadKematian.objects.get(pk=obj["kematian_id"])
        return SadKematianSuratSerializer(inst).data


class AdminKeteranganAhliWarisTunggalSerializer(BaseAdminSuratSerializer):
    atribut = AtributKeteranganAhliWaris()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "kaw_tunggal"


class PendudukKeteranganAhliWarisTunggalSerializer(
    BasePendudukSuratSerializer
):
    atribut = AtributKeteranganAhliWaris()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "kaw_tunggal"


class AdminKeteranganAhliWarisNonTunggalSerializer(BaseAdminSuratSerializer):
    atribut = AtributKeteranganAhliWaris()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "kaw_nontunggal"


class PendudukKeteranganAhliWarisNonTunggalSerializer(
    BasePendudukSuratSerializer
):
    atribut = AtributKeteranganAhliWaris()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "kaw_nontunggal"


class AtributTidakMemilikiBantuanSosial(serializers.Serializer):
    jenis_yang_tidak_dimiliki = serializers.ListField(
        child=serializers.CharField(max_length=32)
    )


class AdminNoDanaSosialSerialzer(BaseAdminSuratSerializer):
    atribut = AtributTidakMemilikiBantuanSosial()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "nds"


class PendudukNoDanaSosialSerialzer(BasePendudukSuratSerializer):
    atribut = AtributTidakMemilikiBantuanSosial()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "nds"


class AtributBukuNikah(serializers.Serializer):
    menikah_dengan = serializers.CharField()
    tgl_menikah = serializers.CharField()
    alasan_hilang = serializers.CharField()


class AdminBukuNikahSerializer(BaseAdminSuratSerializer):
    atribut = AtributBukuNikah()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "bukunikah"


class PendudukBukuNikahSerializer(BasePendudukSuratSerializer):
    atribut = AtributBukuNikah()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "bukunikah"

class AtributItemPemakaman(serializers.Serializer):
    nama = serializers.CharField()
    volume = serializers.IntegerField(default=1)
    satuan = serializers.CharField()
    harga = serializers.IntegerField()
    keterangan = serializers.CharField(required=False)
    jumlah = serializers.SerializerMethodField()

    def get_jumlah(self, obj):
        return obj["volume"] * obj["harga"]


class AtributPengeluaranPemakaman(serializers.Serializer):
    hubungan_keluarga = serializers.CharField()
    uang_nominal = serializers.IntegerField()
    uang_kalimat = serializers.CharField()
    nama_almarhum = serializers.CharField()
    item_pemakaman = serializers.ListField(child=AtributItemPemakaman())
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return sum(i["volume"] * i["harga"] for i in obj["item_pemakaman"])


class AdminPengeluaranPemakamanSerializer(BaseAdminSuratSerializer):
    atribut = AtributPengeluaranPemakaman()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "biayapemakaman"


class PendudukPengeluaranPemakamanSerializer(BasePendudukSuratSerializer):
    atribut = AtributPengeluaranPemakaman()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "biayapemakaman"

class PendudukPembagianWaris(serializers.Serializer):
    nama = serializers.CharField()
    umur = serializers.IntegerField()


class ItemJatahWarisan(serializers.Serializer):
    nama = serializers.CharField()
    keterangan = serializers.CharField(allow_blank=True)


class PenjatahanItemWarisan(serializers.Serializer):
    nama = serializers.CharField()
    items = ItemJatahWarisan(many=True)


class PembagianWarisanPasangan(serializers.Serializer):
    nama = serializers.CharField()
    tanggal_meninggal = serializers.CharField(allow_blank=True)


class AtributPembagianWarisan(serializers.Serializer):
    kematian_id = serializers.IntegerField()
    pasangan = PembagianWarisanPasangan()
    ahli_waris = PendudukPembagianWaris(many=True)
    saksi = serializers.ListField(child=serializers.CharField())
    item_warisan = serializers.ListField(child=serializers.CharField())
    pembagian_warisan = PenjatahanItemWarisan(many=True)
    tanggal_kesepakatan = serializers.CharField()
    tempat_kesepakatan = serializers.CharField()

    kematian = serializers.SerializerMethodField()

    def get_kematian(self, obj):
        inst = SadKematian.objects.get(pk=obj["kematian_id"])
        return SadKematianSuratSerializer(inst).data


class AdminPembagianWarisanSerializer(BaseAdminSuratSerializer):
    atribut = AtributPembagianWarisan()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "bagi_warisan"


class PendudukPembagianWarisanSerializer(BasePendudukSuratSerializer):
    atribut = AtributPembagianWarisan()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "bagi_warisan"


class PendudukPembagianWaris(serializers.Serializer):
    nama = serializers.CharField()
    umur = serializers.IntegerField()


class ItemJatahWarisan(serializers.Serializer):
    nama = serializers.CharField()
    keterangan = serializers.CharField(allow_blank=True)


class PenjatahanItemWarisan(serializers.Serializer):
    nama = serializers.CharField()
    items = ItemJatahWarisan(many=True)


class PembagianWarisanPasangan(serializers.Serializer):
    nama = serializers.CharField()
    tanggal_meninggal = serializers.CharField(allow_blank=True)


class AtributPembagianWarisan(serializers.Serializer):
    kematian_id = serializers.IntegerField()
    pasangan = PembagianWarisanPasangan()
    ahli_waris = PendudukPembagianWaris(many=True)
    saksi = serializers.ListField(child=serializers.CharField())
    item_warisan = serializers.ListField(child=serializers.CharField())
    pembagian_warisan = PenjatahanItemWarisan(many=True)
    tanggal_kesepakatan = serializers.CharField()
    tempat_kesepakatan = serializers.CharField()

    kematian = serializers.SerializerMethodField()

    def get_kematian(self, obj):
        inst = SadKematian.objects.get(pk=obj["kematian_id"])
        return SadKematianSuratSerializer(inst).data


class AdminPembagianWarisanSerializer(BaseAdminSuratSerializer):
    atribut = AtributPembagianWarisan()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "bagi_warisan"


class PendudukPembagianWarisanSerializer(BasePendudukSuratSerializer):
    atribut = AtributPembagianWarisan()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "bagi_warisan"


class KeluargaMiskinAnggota(serializers.Serializer):
    nama = serializers.CharField()
    status_dalam_keluarga = serializers.CharField(allow_blank=True)
    ttl = serializers.CharField()
    nik = serializers.CharField()


class AtributKeluargaMiskin(serializers.Serializer):
    kematian_id = serializers.IntegerField()

    kematian = serializers.SerializerMethodField()
    keluarga = serializers.SerializerMethodField()

    def get_kematian(self, obj):
        inst = SadKematian.objects.get(pk=obj["kematian_id"])
        return SadKematianSuratSerializer(inst).data

    def get_keluarga(self, obj):
        inst = SadKematian.objects.get(pk=obj["kematian_id"])
        data_anggota = []
        for item in inst.penduduk.keluarga.anggota.all():
            item.ttl = (
                f"{item.tempat_lahir}, {item.tgl_lahir.strftime('%d %B %Y')}"
            )
            data_anggota.append(KeluargaMiskinAnggota(item).data)
        return data_anggota


class AdminKeteranganKeluargaMiskin(BaseAdminSuratSerializer):
    atribut = AtributKeluargaMiskin()

    class Meta(BaseAdminSuratSerializer.Meta):
        jenis_surat = "keluarga_miskin"


class PendudukKeteranganKeluargaMiskin(BasePendudukSuratSerializer):
    atribut = AtributKeluargaMiskin()

    class Meta(BasePendudukSuratSerializer.Meta):
        jenis_surat = "keluarga_miskin"


serializer_list = {
    "keluarga_miskin": (
        AdminKeteranganKeluargaMiskin,
        PendudukKeteranganKeluargaMiskin,
        "Surat Keterangan Keluarga Miskin (Santunan Duka)",
    ),
    "bagi_warisan": (
        AdminPembagianWarisanSerializer,
        PendudukPembagianWarisanSerializer,
        "Surat Pembagian Warisan",
    ),
    "biayapemakaman": (
        AdminPengeluaranPemakamanSerializer,
        PendudukPengeluaranPemakamanSerializer,
        "Laporan Penggunaan Biaya Pemakaman",
    ),
    "nds": (
        AdminNoDanaSosialSerialzer,
        PendudukNoDanaSosialSerialzer,
        "Keterangan Tidak Memiliki Bantuan Sosial (Santunan Duka)",
    ),
    "kaw_nontunggal": (
        AdminKeteranganAhliWarisNonTunggalSerializer,
        PendudukKeteranganAhliWarisNonTunggalSerializer,
        "Surat Keterangan Ahli Waris Non Tunggal (Santunan Duka)",
    ),
    "kaw_tunggal": (
        AdminKeteranganAhliWarisTunggalSerializer,
        PendudukKeteranganAhliWarisTunggalSerializer,
        "Surat Keterangan Ahli Waris Tunggal (Santunan Duka)",
    ),
    "perm_bri": (
        AdminPermohonanBRI,
        PendudukPermohonanBRI,
        "Permohonan Peminjaman BRI",
    ),
    "sktm_keluarga": (
        AdminSKTMKeluargaSerializer,
        PendudukSKTMKeluargaSerializer,
        "SKTM - Keluarga",
    ),
    "bntl": (
        AdminBalikNamaTokenListrik,
        PendudukBalikNamaTokenListrik,
        "Surat Pengantar Balik Nama Token Listrik",
    ),
    "perekaman": (
        AdminPerekamanSerializer,
        PendudukPerekamanSerializer,
        "Surat Keterangan Perekaman",
    ),
    "bedanama": (
        AdminBedaNamaSerializer,
        PendudukBedaNamaSerializer,
        "Orang Yang Sama (Perbedaan Nama)",
    ),
    "skaw": (
        AdminAhliWarisSerializer,
        PendudukAhliWarisSerializer,
        "Surat Keterangan Ahli Waris",
    ),
    "shm": (
        AdminHakMilikTanahSerializer,
        PendudukHakMilikTanahSerializer,
        "Surat Keterangan Hak Milik",
    ),
    "skau": (
        AdminSKAUSerializer,
        PendudukSKAUSerializer,
        "Surat Keterangan Asal Usul Kayu",
    ),
    "kelahiran": (
        AdminSuratKelahiranSerializer,
        PendudukSuratKelahiranSerializer,
        "Surat Keterangan Kelahiran",
    ),
    "ket_pisah": (
        AdminKetPisahSerializer,
        PendudukKetPisahSerializer,
        "Surat Keterangan Pisah (Belum Cerai)",
    ),
    "dudajanda": (
        AdminDudaJandaSerializer,
        PendudukDudaJandaSerializer,
        "Surat Keterangan Duda / Janda",
    ),
    "kehilangan": (
        AdminKehilanganSerializer,
        PendudukKehilanganSerializer,
        "Surat Kehilangan",
    ),
    "izinkeramaian": (
        AdminIzinKeramaianSerializer,
        PendudukIzinKeramaianSerializer,
        "Surat Izin Keramaian",
    ),
    "izinpesta": (
        AdminIzinPestaSerializer,
        PendudukIzinPestaSerializer,
        "Surat Izin Pesta",
    ),
    "kematian": (
        AdminSuratKematianSerializer,
        PendudukSuratKematianSerializer,
        "Surat Keterangan Kematian",
    ),
    "ketnelayan": (
        AdminPelakuPerikananSerializer,
        PendudukPelakuPerikananSerializer,
        "Surat Keterangan Pelaku Perikanan",
    ),
    "penguburan": (
        AdminSuratPenguburanSerializer,
        PendudukSuratPenguburanSerializer,
        "Surat Keterangan Penguburan",
    ),
    "skck": (
        AdminSKCKSerializer,
        PendudukSKCKSerializer,
        "Surat Keterangan Catatan Kepolisian",
    ),
    "domisili": (
        AdminDomisiliSerializer,
        PendudukDomisiliSerializer,
        "Surat Keterangan Domisili",
    ),
    "rapidtest": (
        AdminRapidTestSerializer,
        PendudukRapidTestSerializer,
        "Surat Pengantar Rapid Test",
    ),
    "ket_penduduk": (
        AdminKetPendudukSerializer,
        PendudukKetPendudukSerializer,
        "Surat Keterangan Penduduk",
    ),
    "ktt": (
        AdminTempatTinggalSerializer,
        PendudukTempatTinggalSerializer,
        "Surat Keterangan Tempat Tinggal",
    ),
    "kld": (
        AdminLuarDaerahSerializer,
        PendudukLuarDaerahSerializer,
        "Surat Keterangan Di Luar Daerah",
    ),
    "sktm": (
        AdminKetSiswaTidakMampuSerializer,
        PendudukKetSiswaTidakMampuSerializer,
        "Surat Keterangan Siswa Tidak Mampu",
    ),
    "belummenikah": (
        AdminBelumMenikahSerializer,
        PendudukBelumMenikahSerializer,
        "Surat Keterangan Belum Menikah",
    ),
    "usaha": (
        AdminUsahaSerializer,
        PendudukUsahaSerializer,
        "Surat Keterangan Usaha",
    ),
    "bukunikah": (
        AdminBukuNikahSerializer,
        PendudukBukuNikahSerializer,
        "Surat Keterangan Buku Nikah Hilang",
    ),
}
