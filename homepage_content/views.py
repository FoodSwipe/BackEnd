from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from homepage_content.models import HomePageContent
from homepage_content.serializer import (
    HomePageContentPOSTSerializer,
    HomePageContentSerializer,
)


class HomePageContentListView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        all_content = HomePageContent.objects.all()
        serializer = HomePageContentSerializer(
            instance=all_content,
            many=True,
            read_only=True,
            context={"request": request},
        )
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)


class HomepageContentViewSet(viewsets.ModelViewSet):
    queryset = HomePageContent.objects.all()
    serializer_class = HomePageContentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return HomePageContentPOSTSerializer
        return super(HomepageContentViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        homepage_content = self.get_object()
        homepage_content.image.delete()
        homepage_content.delete()
        return Response(
            {"message": "Homepage content item deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
