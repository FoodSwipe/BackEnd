from rest_framework import serializers

from log.models import Log


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        depth = 1
