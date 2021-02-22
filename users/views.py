from rest_framework import permissions
from django.contrib.auth.models import User, Group
from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer


class UserViewSet(DynamicModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def me(self, request):
        user = request.user
        payload = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.groups.first().name,
            'password': user.password
        }

        if hasattr(user, 'profile'):
            profile = {
                'id': user.profile.id,
                'nama': user.profile.nama,
                'nik': user.profile.nik,
                'tempat_lahir': user.profile.tempat_lahir,
                'tanggal_lahir': user.profile.tgl_lahir,
                'kelamin': user.profile.jk,
                'pendidikan': user.profile.pendidikan,
                'potensi': user.profile.potensi_diri if user.profile.potensi_diri else "",
                'agama': user.profile.agama,
                'alamat': user.profile.alamat if user.profile.alamat else "",
                'pekerjaan': user.profile.pekerjaan,
                'no_hp': user.profile.no_hp if user.profile.no_hp else "",
            }
            payload['profile'] = profile
        return Response(payload)


class GroupViewSet(DynamicModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def me(self, request):
        data = GroupSerializer(request.user)
        return Response(data.data)
