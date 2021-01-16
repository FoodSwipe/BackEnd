from django.contrib.auth.models import AnonymousUser
from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE
from reviews.models import Review
from utils.file import check_size


class ReviewSerializer(serializers.ModelSerializer):
    reviewed_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Review
        depth = 1
        fields = "__all__"

    @staticmethod
    def get_reviewed_at(obj):
        return obj.reviewed_at.strftime("%Y/%m/%d %H:%M:%S")

    @staticmethod
    def get_updated_at(obj):
        return obj.updated_at.strftime("%Y/%m/%d %H:%M:%S")


class ReviewPostSerializer(serializers.ModelSerializer):
    image = serializers.FileField(
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)], required=False
    )

    class Meta:
        model = Review
        fields = "__all__"

    @staticmethod
    def validate_image(image):
        check_size(image, MAX_UPLOAD_IMAGE_SIZE)
        return image

    def create(self, validated_data):
        reviewer = self.context.get("request").user
        if isinstance(reviewer, AnonymousUser):
            validated_data["reviewer"] = None
        else:
            validated_data["reviewer"] = reviewer
        return super().create(validated_data)
