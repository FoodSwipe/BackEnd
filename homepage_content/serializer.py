from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from backend.settings import (ALLOWED_IMAGES_EXTENSIONS,
                              HOMEPAGE_CONTENT_IMAGE_MAX_SIZE)
from homepage_content.models import HomePageContent
from utils.file import check_size


class HomePageContentSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, read_only=True)

    class Meta:
        model = HomePageContent
        fields = "__all__"


class HomePageContentPOSTSerializer(serializers.ModelSerializer):
    image = serializers.FileField(validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)])

    def get_fields(self, *args, **kwargs):
        fields = super(HomePageContentPOSTSerializer, self).get_fields()
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields['image'].required = False
        return fields

    class Meta:
        model = HomePageContent
        fields = "__all__"

    @staticmethod
    def validate_image(image):
        if image:
            check_size(image, HOMEPAGE_CONTENT_IMAGE_MAX_SIZE)
        return image
