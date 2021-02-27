from datetime import date

from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from api_sad_sig.util import CustomModel, file_destination


class Pegawai(CustomModel):
    nip = models.CharField(max_length=18, blank=True, null=True)
    chip_ektp = models.CharField(max_length=20, blank=True, null=True)
    nama = models.CharField(max_length=100, blank=True, null=True)
    jabatan = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    golongan = models.CharField(max_length=30, blank=True, null=True)
    gambar = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )

    class Meta(CustomModel.Meta):

        db_table = "pegawai"


class Absensi(models.Model):
    pegawai = models.ForeignKey(
        "Pegawai",
        to_field="id",
        on_delete=models.DO_NOTHING,
        related_name="absensi",
        blank=True,
        null=True,
    )
    # jam_masuk = models.DateTimeField(blank=True,
    # auto_now_add=True, null=True)
    # jam_keluar = models.DateTimeField(blank=True,
    # auto_now=True, null=True)
    jam_masuk = models.DateTimeField(blank=True, null=True)
    jam_keluar = models.DateTimeField(blank=True, null=True)
    alasan_izin = models.ForeignKey(
        "AlasanIzin", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:

        db_table = "absensi"


class AlasanIzin(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)

    class Meta:

        db_table = "alasan_izin"


class SadProvinsi(CustomModel):
    kode_provinsi = models.CharField(max_length=5, blank=True, null=True)
    nama_provinsi = models.CharField(max_length=100, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_provinsi"


class SadKabKota(CustomModel):
    provinsi = models.ForeignKey(
        "SadProvinsi", models.DO_NOTHING, blank=True, null=True
    )
    kode_kab_kota = models.CharField(max_length=5, blank=True, null=True)
    nama_kab_kota = models.CharField(max_length=100, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_kab_kota"


class SadKecamatan(CustomModel):
    kab_kota = models.ForeignKey(
        SadKabKota, models.DO_NOTHING, blank=True, null=True
    )
    kode_kecamatan = models.CharField(max_length=5, blank=True, null=True)
    nama_kecamatan = models.CharField(max_length=250, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_kecamatan"


class SadDesa(CustomModel):
    id = models.BigAutoField(primary_key=True)
    kecamatan = models.ForeignKey(
        "SadKecamatan", models.DO_NOTHING, blank=True, null=True
    )
    kode_desa = models.CharField(max_length=25, blank=True, null=True)
    nama_desa = models.CharField(max_length=250, blank=True, null=True)
    alamat = models.CharField(max_length=150, blank=True, null=True)
    no_telp = models.CharField(max_length=12, blank=True, null=True)
    kode_pos = models.CharField(max_length=5, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    visi_misi = models.TextField(blank=True, null=True)
    sejarah = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to=file_destination, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_desa"


class BatasDesa(CustomModel):
    desa = models.ForeignKey(
        "SadDesa", models.DO_NOTHING, blank=True, null=True
    )
    utara = models.CharField(max_length=50, blank=True, null=True)
    selatan = models.CharField(max_length=50, blank=True, null=True)
    timur = models.CharField(max_length=50, blank=True, null=True)
    barat = models.CharField(max_length=50, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "batas_desa"


class SadDusun(CustomModel):
    desa = models.ForeignKey(
        "SadDesa", models.DO_NOTHING, blank=True, null=True
    )
    nama = models.CharField(max_length=70, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_dusun"


class SadRt(CustomModel):
    rw = models.ForeignKey("SadRw", models.DO_NOTHING, blank=True, null=True)
    rt = models.CharField(max_length=10, blank=True, null=True)
    namart = models.CharField(max_length=100, blank=True, null=True)

    @classmethod
    def find_rt(cls, rt, rw, dukuh, dusun):
        rt = cls.objects.filter(
            rt=rt,
            rw__rw=rw,
            rw__dukuh__nama=dukuh,
            rw__dukuh__dusun__nama=dusun,
            rw__dukuh__dusun__desa__id=settings.DESA_ID,
        ).first()
        return rt

    class Meta(CustomModel.Meta):

        db_table = "sad_rt"


class SadDukuh(CustomModel):
    dusun = models.ForeignKey(
        "SadDusun", models.DO_NOTHING, blank=True, null=True
    )
    nama = models.CharField(max_length=70, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_dukuh"


class SadRw(CustomModel):
    dukuh = models.ForeignKey(
        SadDukuh, models.DO_NOTHING, blank=True, null=True
    )
    rw = models.CharField(max_length=10, blank=True, null=True)
    namarw = models.CharField(max_length=100, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_rw"


class Alamat(CustomModel):
    desa = models.ForeignKey(
        SadDesa, models.DO_NOTHING, related_name="data_alamat"
    )
    dusun = models.ForeignKey(SadDusun, models.DO_NOTHING)
    dukuh = models.ForeignKey(
        SadDukuh, models.DO_NOTHING, blank=True, null=True
    )
    rw = models.ForeignKey(SadRw, models.DO_NOTHING, blank=True, null=True)
    rt = models.ForeignKey(SadRt, models.DO_NOTHING, blank=True, null=True)
    jalan_blok = models.CharField(max_length=128, blank=True, null=True)

    def alamat_lengkap(self):
        if self.rt:
            return f"""RT {self.rt.rt} RT {self.rw.rw},
        Dusun {self.dusun.nama}, Desa {self.desa.nama_desa}"""
        elif self.dusun:
            return f"Dusun {self.dusun.nama}, Desa {self.desa.nama_desa}"
        return None

    def alamat_id(self):
        data = {"desa_id": self.desa.id, "dusun_id": self.dusun.id}
        if self.rt:
            data["rw_id"] = self.rw.id
            data["rt_id"] = self.rt.id
        return data

    def set_from_rt(self, rt_id):
        rt = get_object_or_404(SadRt, pk=rt_id)
        self.rt = rt
        self.rw = rt.rw
        self.dusun = rt.rw.dusun
        self.desa = rt.rw.dusun.desa

    def set_from_dusun(self, dusun_id):
        dusun = get_object_or_404(SadDusun, pk=dusun_id)
        self.dusun = dusun
        self.desa = dusun.desa

    def set_from_excel(self, dusun=None, dukuh=None, rw=None, rt=None):
        rt = SadRt.find_rt(rt, rw, dukuh, dusun)
        if not rt:
            return False
        self.rt = rt
        self.rw = rt.rw
        self.dukuh = rt.rw.dukuh
        self.dusun = rt.rw.dukuh.dusun
        self.desa = rt.rw.dukuh.dusun.desa
        return True

    class Meta(CustomModel.Meta):
        db_table = "alamat"


class SadKeluarga(CustomModel):
    no_kk = models.CharField(max_length=16, unique=True)
    jalan_blok = models.CharField(max_length=100, blank=True, null=True)
    alamat = models.OneToOneField(
        "Alamat", models.DO_NOTHING, blank=True, null=True
    )
    kode_pos = models.CharField(max_length=5, blank=True, null=True)
    status_kesejahteraan = models.CharField(
        max_length=30, blank=True, null=True
    )
    penghasilan = models.IntegerField(blank=True, null=True)
    status_kk = models.CharField(max_length=20, blank=True, null=True)
    menguasai = models.ForeignKey(
        "SigBidang",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="dikuasai",
    )

    @property
    def kepala_keluarga(self):
        kepala_keluarga = self.anggota.filter(
            status_dalam_keluarga="Kepala Keluarga"
        ).first()
        if kepala_keluarga:
            return {"nama": kepala_keluarga.nama, "nik": kepala_keluarga.nik}
        return {}

    def __str__(self):
        return self.no_kk

    class Meta(CustomModel.Meta):

        db_table = "sad_keluarga"


class SadPenduduk(CustomModel):
    keluarga = models.ForeignKey(
        SadKeluarga,
        to_field="no_kk",
        on_delete=models.DO_NOTHING,
        related_name="anggota",
        blank=True,
        null=True,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="profile",
    )

    nik = models.CharField(max_length=16, unique=True)
    chip_ektp = models.CharField(max_length=10, blank=True, null=True)
    nama = models.CharField(max_length=100, blank=True, null=True)
    tgl_lahir = models.DateField(blank=True, null=True)
    tempat_lahir = models.CharField(max_length=50, blank=True, null=True)
    jk = models.CharField(max_length=12, blank=True, null=True)
    alamat = models.CharField(max_length=200, blank=True, null=True)
    agama = models.CharField(max_length=20, blank=True, null=True)
    pendidikan = models.CharField(max_length=100, blank=True, null=True)
    pekerjaan = models.CharField(max_length=100, blank=True, null=True)
    status_kawin = models.CharField(max_length=20, blank=True, null=True)
    status_penduduk = models.CharField(max_length=20, blank=True, null=True)
    kewarganegaraan = models.CharField(max_length=20, blank=True, null=True)
    anak_ke = models.CharField(max_length=5, blank=True, null=True)
    golongan_darah = models.CharField(max_length=5, blank=True, null=True)
    status_dalam_keluarga = models.CharField(
        max_length=20, blank=True, null=True
    )
    no_paspor = models.CharField(max_length=20, blank=True, null=True)
    suku = models.CharField(max_length=20, blank=True, null=True)
    potensi_diri = models.CharField(max_length=50, blank=True, null=True)
    no_hp = models.CharField(max_length=13, blank=True, null=True)
    nik_ayah = models.CharField(max_length=18, blank=True, null=True)
    nik_ibu = models.CharField(max_length=18, blank=True, null=True)
    nama_ayah = models.CharField(max_length=100, blank=True, null=True)
    nama_ibu = models.CharField(max_length=100, blank=True, null=True)
    tgl_exp_paspor = models.DateField(blank=True, null=True)
    akta_lahir = models.CharField(max_length=18, blank=True, null=True)
    akta_kawin = models.CharField(max_length=18, blank=True, null=True)
    tgl_kawin = models.DateField(blank=True, null=True)
    akta_cerai = models.CharField(max_length=18, blank=True, null=True)
    tgl_cerai = models.DateField(blank=True, null=True)
    kelainan_fisik = models.CharField(max_length=100, blank=True, null=True)
    cacat = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(upload_to=file_destination, blank=True, null=True)
    pass_field = models.CharField(
        db_column="pass", max_length=20, blank=True, null=True
    )  # Field renamed because it was a Python reserved word.

    @property
    def no_kk(self):
        return self.keluarga.no_kk

    @property
    def age(self):
        if not self.tgl_lahir:
            return None

        today = date.today()
        birthday = self.tgl_lahir
        age = (
            today.year
            - birthday.year
            - ((today.month, today.day) < (birthday.month, birthday.day))
        )
        return age

    def __str__(self):
        return f"{self.nama} ({self.nik})"

    class Meta(CustomModel.Meta):

        db_table = "sad_penduduk"


class SadSarpras(CustomModel):
    nama_sarpras = models.CharField(max_length=100, blank=True, null=True)
    asal = models.CharField(max_length=50, blank=True, null=True)
    tgl_awal = models.DateField(blank=True, null=True)
    keadaan_awal = models.CharField(max_length=50, blank=True, null=True)
    tgl_hapus = models.DateField(blank=True, null=True)
    ket_hapus = models.CharField(max_length=50, blank=True, null=True)
    keadaan_akhir = models.CharField(max_length=50, blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    tahun = models.CharField(max_length=4, blank=True, null=True)
    foto = models.ImageField(upload_to=file_destination, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_sarpras"


class SadInventaris(CustomModel):
    nama_inventaris = models.CharField(max_length=100, blank=True, null=True)
    asal = models.CharField(max_length=50, blank=True, null=True)
    tgl_awal = models.DateField(blank=True, null=True)
    keadaan_awal = models.CharField(max_length=50, blank=True, null=True)
    tgl_hapus = models.DateField(blank=True, null=True)
    ket_hapus = models.CharField(max_length=50, blank=True, null=True)
    keadaan_akhir = models.CharField(max_length=50, blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    tahun = models.CharField(max_length=4, blank=True, null=True)
    foto = models.ImageField(upload_to=file_destination, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_inventaris"


class SadSurat(CustomModel):
    judul = models.CharField(max_length=100, blank=True, null=True)
    sifat = models.CharField(max_length=50, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sad_surat"


class SadDetailSurat(CustomModel):
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    surat = models.ForeignKey(
        "SadSurat", models.DO_NOTHING, blank=True, null=True
    )
    pegawai = models.ForeignKey(
        Pegawai, models.DO_NOTHING, blank=True, null=True
    )
    lampiran = models.CharField(max_length=50, blank=True, null=True)
    keterangan = models.CharField(max_length=50, blank=True, null=True)
    tempat_tujuan = models.CharField(max_length=50, blank=True, null=True)
    pengikut_pindah = models.CharField(max_length=50, blank=True, null=True)
    asal = models.CharField(max_length=50, blank=True, null=True)
    barang_yg_hilang = models.CharField(max_length=50, blank=True, null=True)
    tgl_jam_kehilangan = models.CharField(max_length=50, blank=True, null=True)
    pelapor = models.CharField(max_length=50, blank=True, null=True)
    nama_yg_sama = models.CharField(max_length=50, blank=True, null=True)
    keperluan = models.CharField(max_length=50, blank=True, null=True)
    berlaku_mulai = models.DateField(blank=True, null=True)
    sampai_dengan = models.DateField(blank=True, null=True)
    nama_acara = models.CharField(max_length=50, blank=True, null=True)
    tgl_acara = models.DateField(blank=True, null=True)
    tempat_acara = models.CharField(max_length=50, blank=True, null=True)
    jenis_hiburan = models.CharField(max_length=50, blank=True, null=True)
    nama_grup = models.CharField(max_length=50, blank=True, null=True)
    pimpinan_acara = models.CharField(max_length=50, blank=True, null=True)
    jumlah_keluarga_yg_pindah = models.CharField(
        max_length=50, blank=True, null=True
    )
    hubungan = models.CharField(max_length=50, blank=True, null=True)
    data_penduduk_luar_desa = models.CharField(
        max_length=50, blank=True, null=True
    )

    class Meta(CustomModel.Meta):

        db_table = "sad_detail_surat"


class SettingDesa(CustomModel):
    desa = models.ForeignKey(SadDesa, models.DO_NOTHING, blank=True, null=True)
    key = models.CharField(max_length=20, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "setting_desa"


class SigPemilik(CustomModel):
    pemilik = models.ForeignKey(
        SadPenduduk, models.DO_NOTHING, blank=True, null=True
    )
    penguasa = models.CharField(max_length=100, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_pemilik"


class PemilikNonWarga(models.Model):
    nik = models.CharField(max_length=32, blank=True, null=True)
    nama = models.CharField(max_length=64)
    namabidang = models.CharField(max_length=64, blank=True, null=True)

    class Meta(CustomModel.Meta):
        db_table = "pemilik_non_warga"


class KepemilikanNonWarga(models.Model):
    non_penduduk = models.ForeignKey("PemilikNonWarga", models.DO_NOTHING)
    bidang = models.ForeignKey("SigBidang", on_delete=models.DO_NOTHING)
    namabidang = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        db_table = "kepemilikan_non_warga"


class KepemilikanWarga(models.Model):
    penduduk = models.ForeignKey("SadPenduduk", on_delete=models.DO_NOTHING)
    bidang = models.ForeignKey("SigBidang", on_delete=models.DO_NOTHING)
    namabidang = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        db_table = "kepemilikan"


class SigBidang(CustomModel):
    nbt = models.CharField(max_length=20, blank=True, null=True)
    longitude = JSONField(blank=True, null=True)
    latitude = JSONField(blank=True, null=True)
    luas = models.CharField(max_length=20, blank=True, null=True)
    status_hak = models.CharField(max_length=50, blank=True, null=True)
    penggunaan_tanah = models.CharField(max_length=100, blank=True, null=True)
    pemanfaatan_tanah = models.CharField(max_length=100, blank=True, null=True)
    rtrw = models.CharField(max_length=100, blank=True, null=True)
    gambar_atas = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )
    gambar_depan = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )
    sig_rt = models.ForeignKey(
        "SigRt", on_delete=models.DO_NOTHING, blank=True, null=True
    )
    sig_dusun = models.ForeignKey(
        "SigDusun", on_delete=models.DO_NOTHING, blank=True, null=True
    )
    pemilikwarga = models.ManyToManyField(
        "SadPenduduk", through="KepemilikanWarga"
    )
    pemiliknonwarga = models.ManyToManyField(
        "PemilikNonWarga", through="KepemilikanNonWarga"
    )
    penguasa_nonwarga = JSONField(max_length=64, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    def alamat_lengkap(self):
        alamat_s = []
        if self.sig_rt:
            alamat_s.extend([self.sig_rt.rt, self.sig_rt.sig_rw.rw])
            if self.sig_rt.sig_rw.sig_dukuh:
                alamat_s.extend(
                    [
                        self.sig_rt.sig_rw.sig_dukuh.nama_dukuh,
                        self.sig_rt.sig_rw.sig_dukuh.sig_dusun.nama_dusun,
                    ]
                )
            else:
                alamat_s.append(self.sig_rt.sig_rw.sig_dusun.nama_dusun)
        elif self.sig_dusun:
            alamat_s.append(self.sig_dusun.nama_dusun)
        return ", ".join(alamat_s)

    @property
    def daftar_pemilik(self):
        pemilik_warga = [
            {
                "nik": i.penduduk.nik,
                "nama": i.penduduk.nama,
                "namabidang": i.namabidang,
                "is_warga": True,
            }
            for i in self.kepemilikanwarga_set.all()
        ]
        pemilik_non_warga = [
            {
                # "nik": i.non_penduduk.nik,
                "nama": i.non_penduduk.nama,
                "namabidang": i.namabidang,
                "is_warga": False,
            }
            for i in self.kepemilikannonwarga_set.all()
        ]
        return pemilik_warga + pemilik_non_warga

    @daftar_pemilik.setter
    def daftar_pemilik(self, value):
        warga_nik = []
        non_warga_nama = []
        for item in value:
            if item.get("is_warga"):
                pemilik = SadPenduduk.objects.get(nik=item["nik"])

                kepemilikan, created = KepemilikanWarga.objects.get_or_create(
                    penduduk=pemilik,
                    bidang=self,
                    defaults={"namabidang": item["namabidang"]},
                )
                (
                    kepemilikan,
                    created,
                ) = KepemilikanWarga.objects.update_or_create(
                    penduduk=pemilik,
                    bidang=self,
                    defaults={"namabidang": item["namabidang"]},
                )
                warga_nik.append(pemilik.nik)
                continue
            pemilik, created = PemilikNonWarga.objects.get_or_create(
                nama=item["nama"], defaults={"nama": item["nama"]}
            )
            pemilik, created = PemilikNonWarga.objects.update_or_create(
                nama=item["nama"], defaults={"nama": item["nama"]}
            )

            kepemilikan, created = KepemilikanNonWarga.objects.get_or_create(
                non_penduduk=pemilik,
                bidang=self,
                defaults={"namabidang": item["namabidang"]},
            )
            (
                kepemilikan,
                created,
            ) = KepemilikanNonWarga.objects.update_or_create(
                non_penduduk=pemilik,
                bidang=self,
                defaults={"namabidang": item["namabidang"]},
            )
            non_warga_nama.append(item["nama"])
        self.kepemilikanwarga_set.exclude(penduduk__nik__in=warga_nik).delete()
        self.kepemilikannonwarga_set.exclude(
            non_penduduk__nama__in=non_warga_nama
        ).delete()
        PemilikNonWarga.objects.annotate(
            kepemilikan_s=models.Count("kepemilikannonwarga")
        ).filter(kepemilikan_s=0).delete()

    @property
    def daftar_penguasa(self):
        penguasa_warga = [
            {
                "no_kk": i.no_kk,
                "is_warga": True,
                "kepala_keluarga": i.kepala_keluarga.get("nama"),
            }
            for i in self.dikuasai.all()
        ]
        if not self.penguasa_nonwarga:
            return penguasa_warga
        return penguasa_warga + self.penguasa_nonwarga

    @daftar_penguasa.setter
    def daftar_penguasa(self, value):
        penguasa_non_warga = []
        penguasa_warga = []
        for item in value:
            if item.get("is_warga"):
                keluarga = SadKeluarga.objects.get(no_kk=item["no_kk"])
                self.dikuasai.add(keluarga)
                penguasa_warga.append(item["no_kk"])
                continue
            penguasa_non_warga.append(item)
        self.penguasa_nonwarga = penguasa_non_warga

        # Remove relationship from ex-penguasa
        ex_penguasa = self.dikuasai.exclude(no_kk__in=penguasa_warga)
        for penguasa in ex_penguasa:
            penguasa.menguasai_id = None
            penguasa.save()

    class Meta(CustomModel.Meta):

        db_table = "sig_bidang"


class SigDesa(CustomModel):
    nama_desa = models.CharField(max_length=250, blank=True, null=True)
    luas = models.CharField(max_length=10, blank=True, null=True)
    keliling = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_desa"


class SigDusun(CustomModel):
    sig_desa = models.ForeignKey(
        SigDesa, models.DO_NOTHING, blank=True, null=True
    )
    nama_dusun = models.CharField(max_length=70, blank=True, null=True)
    luas = models.CharField(max_length=10, blank=True, null=True)
    keliling = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_dusun"


class SigDukuh(CustomModel):
    sig_dusun = models.ForeignKey(
        SigDusun, models.DO_NOTHING, blank=True, null=True
    )
    nama_dukuh = models.CharField(max_length=70, blank=True, null=True)
    luas = models.CharField(max_length=10, blank=True, null=True)
    keliling = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_dukuh"


class SigDukuh2(CustomModel):
    sig_desa = models.ForeignKey(
        SigDesa, models.DO_NOTHING, blank=True, null=True
    )
    nama_dukuh = models.CharField(max_length=70, blank=True, null=True)
    luas = models.CharField(max_length=10, blank=True, null=True)
    keliling = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_dukuh2"


class SigRw(CustomModel):
    sig_dukuh = models.ForeignKey(
        SigDukuh, models.DO_NOTHING, blank=True, null=True
    )
    sig_dusun = models.ForeignKey(
        SigDusun, models.DO_NOTHING, blank=True, null=True
    )
    rw = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_rw"


class SigRt(CustomModel):
    sig_rw = models.ForeignKey(
        "SigRw", models.DO_NOTHING, blank=True, null=True
    )
    rt = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_rt"


class SigKawasanHutan(CustomModel):
    fungsi = models.CharField(max_length=100, blank=True, null=True)
    luas = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_kawasan_hutan"


class SigPenggunaanTanah(CustomModel):
    dusun = models.CharField(max_length=100, blank=True, null=True)
    penggunaan = models.CharField(max_length=100, blank=True, null=True)
    luas = models.CharField(max_length=10, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_penggunaan_tanah"


class SigStatusTanah(CustomModel):
    tipe = models.CharField(max_length=100, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_status_tanah"


class SigArahan(CustomModel):
    luas = models.CharField(max_length=100, blank=True, null=True)
    arahan = models.CharField(max_length=100, blank=True, null=True)
    pola_ruang = models.CharField(max_length=100, blank=True, null=True)
    fungsi = models.CharField(max_length=100, blank=True, null=True)
    geometry = JSONField(blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_arahan"


class SigSadDesa(CustomModel):
    sad_desa = models.ForeignKey(
        SadDesa, models.DO_NOTHING, blank=True, null=True
    )
    sig_desa = models.ForeignKey(
        SigDesa, models.DO_NOTHING, blank=True, null=True
    )

    class Meta(CustomModel.Meta):

        db_table = "sig_sad_desa"


class SigSadBidang(CustomModel):
    sad_penduduk = models.ForeignKey(
        SadPenduduk, models.DO_NOTHING, blank=True, null=True
    )
    sig_bidang = models.ForeignKey(
        SigBidang, models.DO_NOTHING, blank=True, null=True
    )
    pemilik = models.CharField(max_length=100, blank=True, null=True)
    penguasa = models.CharField(max_length=100, blank=True, null=True)

    class Meta(CustomModel.Meta):

        db_table = "sig_sad_bidang"


class Slider(CustomModel):
    judul = models.CharField(max_length=100, blank=True, null=True)
    deskripsi = models.TextField(blank=True, null=True)
    gambar = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )

    class Meta(CustomModel.Meta):

        db_table = "slider"


class KategoriArtikel(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nama

    class Meta:

        db_table = "KategoriArtikel"


class Artikel(models.Model):
    kategori = models.ForeignKey(
        KategoriArtikel, models.DO_NOTHING, blank=True, null=True
    )
    tgl = models.DateField(blank=True, null=True)
    judul = models.CharField(max_length=100, blank=True, null=True)
    isi = models.TextField(blank=True, null=True)
    gambar = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )

    class Meta:

        db_table = "Artikel"


class KategoriPotensi(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nama

    class Meta:
        db_table = "KategoriPotensi"


class Potensi(models.Model):
    kategori = models.ForeignKey(
        KategoriPotensi, models.DO_NOTHING, blank=True, null=True
    )
    nama_usaha = models.CharField(max_length=100, blank=True, null=True)
    harga = models.CharField(max_length=100, blank=True, null=True)
    jenis_promosi = models.CharField(max_length=100, blank=True, null=True)
    no_telp = models.CharField(max_length=100, blank=True, null=True)
    judul = models.CharField(max_length=100, blank=True, null=True)
    isi = models.TextField(blank=True, null=True)
    koordinat = models.TextField(blank=True, null=True)
    gambar = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )

    class Meta:

        db_table = "Potensi"


class KategoriInformasi(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nama

    class Meta:

        db_table = "KategoriInformasi"


class Informasi(models.Model):
    kategori = models.ForeignKey(
        KategoriInformasi, models.DO_NOTHING, blank=True, null=True
    )
    judul = models.CharField(max_length=100, blank=True, null=True)
    tempat = models.CharField(max_length=100, blank=True, null=True)
    tanggal = models.DateField(blank=True, null=True)
    mulai = models.CharField(max_length=10, blank=True, null=True)
    selesai = models.CharField(max_length=10, blank=True, null=True)
    gambar = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )

    class Meta:

        db_table = "Informasi"


class KategoriLapor(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)
    gambar = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )

    def __str__(self):
        return self.nama

    class Meta:

        db_table = "KategoriLapor"


class StatusLapor(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)
    warna = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nama

    class Meta:

        db_table = "StatusLapor"


class Lapor(CustomModel):
    kategori = models.ForeignKey(
        KategoriLapor, models.DO_NOTHING, blank=True, null=True
    )
    judul = models.CharField(max_length=100, blank=True, null=True)
    isi = models.TextField(blank=True, null=True)
    gambar = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )
    status = models.ForeignKey(
        StatusLapor, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:

        db_table = "Lapor"


class KategoriPendapatan(models.Model):
    kode = models.CharField(max_length=10, blank=True, null=True)
    nama = models.CharField(max_length=100, blank=True, null=True)
    jumlah_anggaran = models.TextField(blank=True, null=True)

    class Meta:

        db_table = "kategori_pendapatan"


class KategoriTahun(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)

    class Meta:

        db_table = "kategori_tahun"


class Pendapatan(models.Model):
    kategori = models.ForeignKey(
        KategoriPendapatan, models.DO_NOTHING, blank=True, null=True
    )
    tahun = models.ForeignKey(
        KategoriTahun, models.DO_NOTHING, blank=True, null=True
    )
    kode = models.CharField(max_length=20, blank=True, null=True)
    nama = models.CharField(max_length=100, blank=True, null=True)
    anggaran = models.CharField(max_length=100, blank=True, null=True)
    sumber_dana = models.CharField(max_length=100, blank=True, null=True)
    tgl = models.DateField(blank=True, null=True)

    class Meta:

        db_table = "pendapatan"


class KategoriBelanja(models.Model):
    kode = models.CharField(max_length=10, blank=True, null=True)
    nama = models.CharField(max_length=100, blank=True, null=True)
    jumlah_anggaran = models.TextField(blank=True, null=True)

    class Meta:

        db_table = "kategori_belanja"


class Belanja(models.Model):
    kategori = models.ForeignKey(
        KategoriBelanja, models.DO_NOTHING, blank=True, null=True
    )
    tahun = models.ForeignKey(
        KategoriTahun, models.DO_NOTHING, blank=True, null=True
    )
    kode = models.CharField(max_length=20, blank=True, null=True)
    nama = models.CharField(max_length=100, blank=True, null=True)
    anggaran = models.CharField(max_length=100, blank=True, null=True)
    sumber_dana = models.CharField(max_length=100, blank=True, null=True)
    deskripsi = models.TextField(blank=True, null=True)
    tgl = models.DateField(blank=True, null=True)
    foto_sebelum = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )
    foto_sesudah = models.ImageField(
        upload_to=file_destination, blank=True, null=True
    )
    progres = models.CharField(max_length=100, blank=True, null=True)
    koordinat = models.TextField(blank=True, null=True)

    class Meta:

        db_table = "belanja"


class SuratMasuk(models.Model):
    no_surat = models.CharField(max_length=100, blank=True, null=True)
    tgl_terima = models.DateField(blank=True, null=True)
    tgl_surat = models.DateField(blank=True, null=True)
    pengirim = models.CharField(max_length=100, blank=True, null=True)
    kepada = models.CharField(max_length=100, blank=True, null=True)
    perihal = models.CharField(max_length=100, blank=True, null=True)
    keterangan = models.CharField(max_length=100, blank=True, null=True)
    arsip_suratmasuk = models.FileField(
        upload_to=file_destination, blank=True, null=True
    )

    def __str__(self):
        return self.nama

    class Meta:

        db_table = "surat_masuk"


class SuratKeluar(models.Model):
    no_surat = models.CharField(max_length=100, blank=True, null=True)
    tgl_kirim = models.DateField(blank=True, null=True)
    tgl_surat = models.DateField(blank=True, null=True)
    pengirim = models.CharField(max_length=100, blank=True, null=True)
    kepada = models.CharField(max_length=100, blank=True, null=True)
    perihal = models.CharField(max_length=100, blank=True, null=True)
    keterangan = models.CharField(max_length=100, blank=True, null=True)
    arsip_suratkeluar = models.FileField(
        upload_to=file_destination, blank=True, null=True
    )

    def __str__(self):
        return self.nama

    class Meta:

        db_table = "surat_keluar"


class Pekerjaan(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        db_table = "pekerjaan"


class Pendidikan(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        db_table = "pendidikan"


class Agama(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        db_table = "agama"


class KelainanFisik(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        db_table = "kelainanfisik"


class Cacat(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        db_table = "cacat"


class StatusPerkawinan(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        db_table = "status_perkawinan"


class Kewarganegaraan(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        db_table = "kewarganegaraan"


class Goldar(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        db_table = "goldar"


class StatusDlmKeluarga(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        db_table = "status_dalam_keluarga"


class StatusKesejahteraan(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "status_kesejahteraan"


class StatusWarga(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "status_warga"


class StatusDatangMasuk(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "status_datang_masuk"


class Asal(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "asal"


class KeadaanAwal(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "keadaan_awal"


class Jabatan(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "jabatan"


class StatusPns(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "status_pns"


class Golongan(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "golongan"


class JenisKelahiran(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "jenis_kelahiran"


class JenisTempat(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "jenis_tempat"


class TenagaKesehatan(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "tenaga_kesehatan"


class Dashboard:
    def __init__(self, dusun, penduduk, keluarga):
        self.penduduk = penduduk
        self.dusun = dusun
        self.keluarga = keluarga


class Cctv(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    koordinat = JSONField(blank=True, null=True)

    class Meta:
        db_table = "cctv"
