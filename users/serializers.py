from django.contrib.auth.models import User, Group
from dynamic_rest.serializers import DynamicModelSerializer, fields


class GroupSerializer(DynamicModelSerializer):
    class Meta:
        model = Group
        name = "data"
        fields = ["id", "name"]


class UserSerializer(DynamicModelSerializer):
    role = fields.CharField(source="groups.first")
    group_name = fields.CharField(write_only=True)

    class Meta:
        model = User
        name = "data"
        fields = ["id", "username", "email", "role", 'group_name', 'password']
        read_only_fields = ['role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            group = Group.objects.get(name=validated_data['group_name'])
        except Exception:
            group = Group.objects.get(name='penduduk')
        validated_data.pop('group_name')

        user = super().create(validated_data)
        user.is_active = True
        user.set_password(validated_data["password"])

        user.groups.add(group)
        user.save()

        return user

    def update(self, instance, validated_data):
        try:
            group = Group.objects.get(name=validated_data['group_name'])
        except Exception:
            group = Group.objects.get(name='penduduk')
        validated_data.pop('group_name')

        user = super().update(instance, validated_data)
        user.set_password(validated_data["password"])

        user.groups.remove(user.groups.first())
        user.groups.add(group)
        user.save()

        return user
