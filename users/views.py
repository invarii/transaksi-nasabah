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
        data = UserSerializer(request.user)
        return Response(data.data)


class GroupViewSet(DynamicModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def me(self, request):
        data = GroupSerializer(request.user)
        return Response(data.data)
