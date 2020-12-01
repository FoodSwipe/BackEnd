from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from item_group.models import MenuItemGroup, MenuItemGroupImage
from item_group.serializers import MenuItemGroupSerializer, MenuItemGroupPOSTSerializer, MenuItemGroupImageSerializer


class MenuItemGroupViewSet(viewsets.ModelViewSet):
    queryset = MenuItemGroup.objects.all()
    serializer_class = MenuItemGroupSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return MenuItemGroupPOSTSerializer
        return super(MenuItemGroupViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        menu_item_group = self.get_object()
        menu_item_group.delete()
        return Response({
            "message": "Menu item group deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class MenuItemGroupImageViewSet(viewsets.ModelViewSet):
    queryset = MenuItemGroupImage.objects.all()
    serializer_class = MenuItemGroupImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        menu_item_group_photo = self.get_object()
        menu_item_group_photo.image.delete()
        menu_item_group_photo.delete()
        return Response({
            "message": "Menu item group image deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)
