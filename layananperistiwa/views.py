from rest_framework import permissions

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from dynamic_rest.viewsets import DynamicModelViewSet

from api_sad_sig.util import CustomView
from users.permissions import IsAdminUserOrReadOnly

from .utils import render_mail
from .models import (
    SuratDomisili,
    SuratKelahiran,
    SuratSkck,
    SadKelahiran,
    SadKematian,
    SadLahirmati,
    JenisPindah,
    AlasanPindah,
    KlasifikasiPindah,
    StatusKKPindah,
    StatusKKTinggal,
    SadPindahKeluar,
    SadPindahMasuk,
    SadPecahKK,
)
from .serializers import (
    AdminSuratDomisiliSerializer,
    AdminSuratKelahiranSerializer,
    AdminSuratSkckSerializer,
    SuratDomisiliSerializer,
    SuratKelahiranSerializer,
    SuratSkckSerializer,
    SadKelahiranSerializer,
    SadKematianSerializer,
    SadLahirmatiSerializer,
    AlasanPindahSerializer,
    KlasifikasiPindahSerializer,
    JenisPindahSerializer,
    StatusKKPindahSerializer,
    StatusKKTinggalSerializer,
    SadPindahKeluarSerializer,
    SadPindahMasukSerializer,
    SadPecahKKSerializer,
)


class SuratKelahiranViewSet(DynamicModelViewSet):
    queryset = SuratKelahiran.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.groups.first().name == "admin":
            return AdminSuratKelahiranSerializer
        return SuratKelahiranSerializer

    @action(detail=True, methods=["get"])
    def print(self, request, pk=None):
        data = self.get_object()
        pdf = render_mail("skl", data)
        return HttpResponse(pdf, content_type="application/pdf")


class SuratSkckViewSet(DynamicModelViewSet):
    queryset = SuratSkck.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.groups.first().name == "admin":
            return AdminSuratSkckSerializer
        return SuratSkckSerializer

    @action(detail=True, methods=["get"])
    def print(self, request, pk=None):
        data = self.get_object()
        pdf = render_mail("skck", data)
        return HttpResponse(pdf, content_type="application/pdf")


class SuratDomisiliViewSet(DynamicModelViewSet):
    queryset = SuratDomisili.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.groups.first().name == "admin":
            return AdminSuratDomisiliSerializer
        return SuratDomisiliSerializer

    @action(detail=True, methods=["get"])
    def print(self, request, pk=None):
        data = self.get_object()
        pdf = render_mail("skd", data)
        return HttpResponse(pdf, content_type="application/pdf")


class SadKelahiranViewSet(CustomView):
    queryset = SadKelahiran.objects.all().order_by("id")
    serializer_class = SadKelahiranSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class SadKematianViewSet(CustomView):
    queryset = SadKematian.objects.all().order_by("id")
    serializer_class = SadKematianSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class SadLahirmatiViewSet(CustomView):
    queryset = SadLahirmati.objects.all().order_by("id")
    serializer_class = SadLahirmatiSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class JenisPindahViewSet(CustomView):
    queryset = JenisPindah.objects.all()
    serializer_class = JenisPindahSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class AlasanPindahViewSet(CustomView):
    queryset = AlasanPindah.objects.all()
    serializer_class = AlasanPindahSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class KlasifikasiPindahViewSet(CustomView):
    queryset = KlasifikasiPindah.objects.all()
    serializer_class = KlasifikasiPindahSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class StatusKKTinggalViewSet(CustomView):
    queryset = StatusKKTinggal.objects.all()
    serializer_class = StatusKKTinggalSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class StatusKKPindahViewSet(CustomView):
    queryset = StatusKKPindah.objects.all()
    serializer_class = StatusKKPindahSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class SadPindahKeluarViewSet(CustomView):
    queryset = SadPindahKeluar.objects.all().order_by("id")
    serializer_class = SadPindahKeluarSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def retrieve(self, request, pk=None):
        queryset = SadPindahKeluar.objects.all()
        sad_pindah = get_object_or_404(queryset, pk=pk)
        serializer = SadPindahKeluarSerializer(sad_pindah)
        data = serializer.data

        penduduk_s = sad_pindah.anggota_keluar()
        penduduk_data = []
        for item in penduduk_s:
            temp_data = {"nik": item.nik, "nama": item.nama}
            penduduk_data.append(temp_data)

        data["anggota_keluar"] = penduduk_data
        return Response(data)


class SadPindahMasukViewSet(CustomView):
    queryset = SadPindahMasuk.objects.all().order_by("id")
    serializer_class = SadPindahMasukSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class SadPecahKKViewSet(CustomView):
    queryset = SadPecahKK.objects.order_by("id").all()
    serializer_class = SadPecahKKSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["update", "retrieve", "delete"]:
            raise NotFound("Operasi ini tidak tersedia")
        return SadPecahKKSerializer
