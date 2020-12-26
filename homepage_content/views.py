from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from homepage_content.models import HomePageContent
from homepage_content.serializer import HomePageContentSerializer, HomePageContentPOSTSerializer


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
        return Response({
            "message": "Homepage content item deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)