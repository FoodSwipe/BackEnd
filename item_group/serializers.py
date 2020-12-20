from rest_framework import serializers

from backend.settings import MAX_UPLOAD_IMAGE_SIZE
from item.models import MenuItem
from item_group.models import MenuItemGroup
from utils.file import check_size


class ItemSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = MenuItem
        fields = ["id", "name", "image", "price", "item_type"]
        depth = 1


class ItemGroupSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    menu_items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = MenuItemGroup
        fields = ["id", "name", "image", "menu_items"]
        depth = 1


class MenuItemGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemGroup
        fields = "__all__"
        depth = 1


class MenuItemGroupPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemGroup
        fields = "__all__"

    def get_fields(self, *args, **kwargs):
        fields = super(MenuItemGroupPOSTSerializer, self).get_fields()
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields['image'].required = False
        return fields

    def validate_image(self, obj):
        check_size(obj, MAX_UPLOAD_IMAGE_SIZE)
        return obj

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)
