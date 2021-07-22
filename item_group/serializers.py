from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE
from item.models import MenuItem
from item_group.models import MenuItemGroup
from log.models import Log
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
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime("%Y/%m/%d %H:%M:%S")

    @staticmethod
    def get_updated_at(obj):
        return obj.updated_at.strftime("%Y/%m/%d %H:%M:%S")

    class Meta:
        model = MenuItemGroup
        fields = "__all__"
        depth = 1


class MenuItemGroupPOSTSerializer(serializers.ModelSerializer):
    image = serializers.FileField(
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)]
    )

    @staticmethod
    def validate_image(image):
        if image:
            check_size(image, MAX_UPLOAD_IMAGE_SIZE)
        return image

    class Meta:
        model = MenuItemGroup
        fields = "__all__"

    def get_fields(self, *args, **kwargs):
        fields = super(MenuItemGroupPOSTSerializer, self).get_fields()
        request = self.context.get("request", None)
        if request and getattr(request, "method", None) == "PUT":
            fields["image"].required = False
        return fields

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        Log.objects.create(
            mode="create",
            actor=validated_data["created_by"],
            detail="New menu item group added. ({})".format(validated_data["name"]),
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)
