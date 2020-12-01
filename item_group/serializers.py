from rest_framework import serializers

from backend.settings import MAX_UPLOAD_IMAGE_SIZE
from item_group.models import MenuItemGroup, MenuItemGroupImage
from utils.file import check_size


class MenuItemGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemGroup
        fields = "__all__"
        depth = 1


class MenuItemGroupPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemGroup
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)


class MenuItemGroupImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemGroupImage
        fields = "__all__"

    def validate_image(self, obj):
        check_size(obj, MAX_UPLOAD_IMAGE_SIZE)
        return obj
