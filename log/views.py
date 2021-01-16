from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from log.models import Log
from log.serializers import LogSerializer


class LogsListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request):
        logs = Log.objects.all().order_by("-timestamp")
        return Response(
            {"results": LogSerializer(instance=logs, many=True, read_only=True).data},
            status=status.HTTP_200_OK,
        )
