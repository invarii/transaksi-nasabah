from django.contrib.auth.models import User, Group
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicRelationField
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
)

class UserSerializer(DynamicModelSerializer):
  class Meta:
    model = User
    name = 'data'
    fields = ['id', 'username', 'email', 'groups']

class GroupSerializer(DynamicModelSerializer):
  class Meta:
    model = Group
    name = 'data'
    fields = ['id', 'name']

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
    fields = ['id', 'no_kk', 'anggota']

class SadPendudukSerializer(DynamicModelSerializer):
  keluarga = DynamicRelationField('SadKeluargaSerializer', deferred=True, embed=True)
  class Meta:
    model = SadPenduduk
    name = 'data'
    fields = ['id', 'nik', 'nama', 'keluarga']