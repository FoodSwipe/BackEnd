from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE
from item.models import ItemType, MenuItem, TopAndRecommendedItem
from log.models import Log
from utils.file import check_size


class MenuItemSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime("%Y/%m/%d %H:%M:%S")

    @staticmethod
    def get_updated_at(obj):
        return obj.updated_at.strftime("%Y/%m/%d %H:%M:%S")

    class Meta:
        model = MenuItem
        fields = "__all__"
        depth = 1

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)


class MenuItemPOSTSerializer(serializers.ModelSerializer):
    image = serializers.FileField(
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)]
    )

    class Meta:
        model = MenuItem
        fields = "__all__"

    def get_fields(self, *args, **kwargs):
        fields = super(MenuItemPOSTSerializer, self).get_fields()
        request = self.context.get("request", None)
        if request and getattr(request, "method", None) == "PUT":
            fields["image"].required = False
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
        Log.objects.create(
            mode="create",
            actor=validated_data["created_by"],
            detail="New menu item added. ({})".format(menu_item.name),
        )
        return menu_item

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)


class ItemTypeSerializer(serializers.ModelSerializer):
    badge = serializers.FileField(
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)]
    )

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


class TopAndRecommendedMenuItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer()

    class Meta:
        model = TopAndRecommendedItem
        fields = "__all__"
        depth = 1


class TopAndRecommendedMenuItemPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopAndRecommendedItem
        fields = "__all__"
