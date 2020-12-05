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
)

class GroupSerializer(DynamicModelSerializer):
  class Meta:
    model = Group
    name = 'data'
    fields = ['id', 'name']


class UserSerializer(DynamicModelSerializer):
  group = DynamicRelationField('GroupSerializer', deferred=False, embed=True)
  class Meta:
    model = User
    name = 'data'
    exclude = []
  
  def create(self, validated_data):
    user = super().create(validated_data)
    user.is_active = True
    user.set_password(validated_data['password'])
    user.save()

    return user

  def update(self, instance, validated_data):
    user = super().update(instance, validated_data)
    user.set_password(validated_data['password'])
    user.save()

    return user

class PegawaiSerializer(DynamicModelSerializer):
  class Meta:
    model = Pegawai
    name = 'data'
    fields = ['id', 'nama', 'jabatan']

class SadProvinsiSerializer(DynamicModelSerializer):
  class Meta:
    model = SadProvinsi
    name = 'data'
    fields = ['id', 'kode_provinsi', 'nama_provinsi']

class SadKabKotaSerializer(DynamicModelSerializer):
  class Meta:
    model = SadKabKota
    name = 'data'
    fields = ['id', 'kode_kab_kota', 'nama_kab_kota']

class SadKecamatanSerializer(DynamicModelSerializer):
  kab_kota = DynamicRelationField('SadKabKotaSerializer', deferred=False, embed=True)
  class Meta:
    model = SadKecamatan
    name = 'data'
    fields = ['id', 'kode_kecamatan', 'nama_kecamatan', 'kab_kota']
  
class SadDesaSerializer(DynamicModelSerializer):
  kecamatan = DynamicRelationField('SadKecamatanSerializer', deferred=False, embed=True)
  class Meta:
    model = SadDesa
    name = 'data'
    fields = ['id', 'kode_desa', 'nama_desa', 'kecamatan']

class SadDusunDukuhSerializer(DynamicModelSerializer):
  class Meta:
    model = SadDusunDukuh
    name = 'data'
    fields = ['id', 'nama']

class SadRwSerializer(DynamicModelSerializer):
  class Meta:
    model = SadRw
    name = 'data'
    fields = ['id', 'rw']

class SadRtSerializer(DynamicModelSerializer):
  class Meta:
    model = SadRt
    name = 'data'
    fields = ['id', 'rt']

class SadKeluargaSerializer(DynamicModelSerializer):
  anggota = DynamicRelationField('SadPendudukSerializer', many=True, deferred=True, embed=True)
  class Meta:
    model = SadKeluarga
    name = 'data'
    exclude = []
    extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

class SadPendudukSerializer(DynamicModelSerializer):
  keluarga = DynamicRelationField('SadKeluargaSerializer', deferred=True, embed=True)
  class Meta:
    model = SadPenduduk
    name = 'data'
    exclude = []

class SadKelahiranSerializer(DynamicModelSerializer):
  class Meta:
    model = SadKelahiran
    name = 'data'
    exclude = []

class SadKematianSerializer(DynamicModelSerializer):
  penduduk = DynamicRelationField('SadPendudukSerializer', deferred=True, embed=True)
  class Meta:
    model = SadKematian
    name = 'data'
    exclude = []

class SadLahirmatiSerializer(DynamicModelSerializer):
  class Meta:
    model = SadLahirmati
    name = 'data'
    exclude = []

class SadPindahKeluarSerializer(DynamicModelSerializer):
  class Meta:
    model = SadPindahKeluar
    name = 'data'
    exclude = []

class SadPindahMasukSerializer(DynamicModelSerializer):
  class Meta:
    model = SadPindahMasuk
    name = 'data'
    fields = ['id', 'no_kk', 'nik_kepala_keluarga']

class SadSarprasSerializer(DynamicModelSerializer):
  class Meta:
    model = SadSarpras
    name = 'data'
    fields = ['id', 'nama_sarpras', 'asal']

class SadInventarisSerializer(DynamicModelSerializer):
  class Meta:
    model = SadInventaris
    name = 'data'
    fields = ['id', 'nama_inventaris', 'asal']

class SadSuratSerializer(DynamicModelSerializer):
  class Meta:
    model = SadSurat
    name = 'data'
    fields = ['id', 'judul', 'sifat']

class SadDetailSuratSerializer(DynamicModelSerializer):
  class Meta:
    model = SadDetailSurat
    name = 'data'
    fields = ['id', 'no_surat', 'keterangan']

class SigDesaSerializer(DynamicModelSerializer):
  class Meta:
    model = SigDesa
    name = 'data'
    exclude = []

class SigDusunSerializer(DynamicModelSerializer):
  sig_desa = DynamicRelationField('SigDesaSerializer', deferred=True, embed=True)
  class Meta:
    model = SigDusun
    name = 'data'
    exclude = []

class SigDukuhSerializer(DynamicModelSerializer):
  sig_dusun = DynamicRelationField('SigDusunSerializer', deferred=True, embed=True)
  class Meta:
    model = SigDukuh
    name = 'data'
    exclude = []

class SigDukuh2Serializer(DynamicModelSerializer):
  sig_desa = DynamicRelationField('SigDesaSerializer', deferred=True, embed=True)
  class Meta:
    model = SigDukuh2
    name = 'data'
    exclude = []

class SigRwSerializer(DynamicModelSerializer):
  sig_dukuh = DynamicRelationField('SigDukuhSerializer', deferred=True, embed=True)
  class Meta:
    model = SigRw
    name = 'data'
    exclude = []

class SigRtSerializer(DynamicModelSerializer):
  sig_rw = DynamicRelationField('SigRwSerializer', deferred=True, embed=True)
  class Meta:
    model = SigRt
    name = 'data'
    exclude = []

class SigRw2Serializer(DynamicModelSerializer):
  sig_dukuh2 = DynamicRelationField('SigDukuh2Serializer', deferred=True, embed=True)
  class Meta:
    model = SigRw2
    name = 'data'
    exclude = []

class SigRt2Serializer(DynamicModelSerializer):
  sig_rw2 = DynamicRelationField('SigRw2Serializer', deferred=True, embed=True)
  class Meta:
    model = SigRt2
    name = 'data'
    exclude = []

class SigBidangSerializer(DynamicModelSerializer):
  desa = DynamicRelationField('SigDesaSerializer', deferred=True, embed=True)
  class Meta:
    model = SigBidang
    name = 'data'
    exclude = []