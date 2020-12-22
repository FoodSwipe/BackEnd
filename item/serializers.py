from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from backend.settings import MAX_UPLOAD_IMAGE_SIZE, ALLOWED_IMAGES_EXTENSIONS
from item.models import MenuItem, ItemType
from utils.file import check_size


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"
        depth = 1

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)


class MenuItemPOSTSerializer(serializers.ModelSerializer):
    image = serializers.FileField(validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)])

    class Meta:
        model = MenuItem
        fields = "__all__"

    def get_fields(self, *args, **kwargs):
        fields = super(MenuItemPOSTSerializer, self).get_fields()
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields['image'].required = False
        return fields

    @staticmethod
    def validate_image(image):
        if image:
            check_size(image, MAX_UPLOAD_IMAGE_SIZE)
        return image

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        item_types = validated_data["item_type"]
        del validated_data["item_type"]
        menu_item = MenuItem.objects.create(**validated_data)
        menu_item.save()
        for item_type in item_types:
            menu_item.item_type.add(item_type)
        menu_item.save()
        return menu_item

    def update(self, instance, validated_data):
        print("here")
        validated_data["updated_by"] = self.context["request"].user
        print(validated_data.get("image"))
        print(validated_data)
        return super().update(instance, validated_data)


class ItemTypeSerializer(serializers.ModelSerializer):
    badge = serializers.FileField(validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)])

    class Meta:
        model = ItemType
        fields = "__all__"

    @staticmethod
    def validate_badge(image):
        if image:
            check_size(image, MAX_UPLOAD_IMAGE_SIZE)
        return image


class OrderNowListSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    group = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ["id", "name", "group", "image", "price"]

    @staticmethod
    def get_group(menu_item):
        return menu_item.menu_item_group.name
