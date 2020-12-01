from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from item.models import MenuItem, MenuItemImage, MenuItemType, ItemType
from item.serializers import MenuItemSerializer, MenuItemPOSTSerializer, MenuItemImageSerializer, \
    MenuItemTypeSerializer, ItemTypeSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return MenuItemPOSTSerializer
        return super(MenuItemViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        menu_item = self.get_object()
        menu_item.delete()
        return Response({
            "message": "Menu item deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class MenuItemImageViewSet(viewsets.ModelViewSet):
    queryset = MenuItemImage.objects.all()
    serializer_class = MenuItemImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        menu_item_image = self.get_object()
        menu_item_image.image.delete()
        menu_item_image.delete()
        return Response({
            "message": "Menu item image deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class MenuItemTypeViewSet(viewsets.ModelViewSet):
    queryset = MenuItemType.objects.all()
    serializer_class = MenuItemTypeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        menu_item_type = self.get_object()
        menu_item_type.delete()
        return Response({
            "message": "Menu item type deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        item_type = self.get_object()
        item_type.badge.delete()
        item_type.delete()
        return Response({
            "message": "Menu item type deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)
