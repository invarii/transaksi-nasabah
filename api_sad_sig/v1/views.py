from django.contrib.auth.models import User, Group
from rest_framework import permissions
from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
  UserSerializer,
  GroupSerializer,
  PegawaiSerializer,
  SadProvinsiSerializer,
  SadKabKotaSerializer,
  SadKecamatanSerializer,
  SadDesaSerializer,
  SadDusunDukuhSerializer,
  SadRwSerializer,
  SadRtSerializer,
  SadKeluargaSerializer,
  SadPendudukSerializer,
)
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


class UserViewSet(DynamicModelViewSet):
  queryset = User.objects.all().order_by('-date_joined')
  serializer_class = UserSerializer
  permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(DynamicModelViewSet):
  queryset = Group.objects.all()
  serializer_class = GroupSerializer
  permission_classes = [permissions.IsAuthenticated]


class PegawaiViewSet(DynamicModelViewSet):
  queryset = Pegawai.objects.all().order_by('id')
  serializer_class = PegawaiSerializer
  permission_classes = [permissions.IsAuthenticated]

class SadProvinsiViewSet(DynamicModelViewSet):
  queryset = SadProvinsi.objects.all().order_by('id')
  serializer_class = SadProvinsiSerializer
  permission_classes = [permissions.IsAuthenticated]

class SadKabKotaViewSet(DynamicModelViewSet):
  queryset = SadKabKota.objects.all().order_by('id')
  serializer_class = SadKabKotaSerializer
  permission_classes = [permissions.IsAuthenticated]

class SadKecamatanViewSet(DynamicModelViewSet):
  queryset = SadKecamatan.objects.all().order_by('id')
  serializer_class = SadKecamatanSerializer
  permission_classes = [permissions.IsAuthenticated]

class SadDesaViewSet(DynamicModelViewSet):
  queryset = SadDesa.objects.all().order_by('id')
  serializer_class = SadDesaSerializer
  permission_classes = [permissions.IsAuthenticated]

class SadDusunDukuhViewSet(DynamicModelViewSet):
  queryset = SadDusunDukuh.objects.all().order_by('id')
  serializer_class = SadDusunDukuhSerializer
  permission_classes = [permissions.IsAuthenticated]

class SadRwViewSet(DynamicModelViewSet):
  queryset = SadRw.objects.all().order_by('id')
  serializer_class = SadRwSerializer
  permission_classes = [permissions.IsAuthenticated]

class SadRtViewSet(DynamicModelViewSet):
  queryset = SadRt.objects.all().order_by('id')
  serializer_class = SadRtSerializer
  permission_classes = [permissions.IsAuthenticated]

class SadKeluargaViewSet(DynamicModelViewSet):
  queryset = SadKeluarga.objects.all().order_by('id')
  serializer_class = SadKeluargaSerializer
  permission_classes = [permissions.IsAuthenticated]

class SadPendudukViewSet(DynamicModelViewSet):
  queryset = SadPenduduk.objects.all().order_by('id')
  serializer_class = SadPendudukSerializer
  permission_classes = [permissions.IsAuthenticated]