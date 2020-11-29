from rest_framework import serializers

from accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        depth = 1


class ProfilePOSTSerializer(serializers.ModelSerializer):
    contacts = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Profile
        fields = "__all__"
