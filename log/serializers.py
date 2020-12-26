from rest_framework import serializers

from log.models import Log


class LogSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()

    @staticmethod
    def get_timestamp(obj):
        return obj.timestamp.strftime("%b %d, %Y %H:%M:%S")

    class Meta:
        model = Log
        depth = 1
        fields = "__all__"
