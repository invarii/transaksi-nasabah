from django.contrib.auth.models import User, Group
from dynamic_rest.serializers import DynamicModelSerializer, fields


class GroupSerializer(DynamicModelSerializer):
    class Meta:
        model = Group
        name = "data"
        fields = ["id", "name"]


class UserSerializer(DynamicModelSerializer):
    role = fields.CharField(source="groups.first")

    class Meta:
        model = User
        name = "data"
        fields = ["id", "username", "email", "groups", "role"]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.is_active = True
        user.set_password(validated_data["password"])
        user.save()

        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user
