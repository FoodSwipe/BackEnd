from rest_framework import serializers

from backend.settings import MAX_UPLOAD_IMAGE_SIZE
from item.models import MenuItem, MenuItemImage, ItemType, MenuItemType
from utils.file import check_size


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"
        depth = 1


class MenuItemPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return MenuItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)


class MenuItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemImage
        fields = "__all__"

    def validate_image(self, obj):
        check_size(obj, MAX_UPLOAD_IMAGE_SIZE)
        return obj


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = "__all__"

    def validate_badge(self, obj):
        check_size(obj, MAX_UPLOAD_IMAGE_SIZE)
        return obj


class MenuItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemType
        fields = "__all__"
