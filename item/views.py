from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from item.models import MenuItem, ItemType
from item.serializers import MenuItemSerializer, MenuItemPOSTSerializer, ItemTypeSerializer, OrderNowListSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all().order_by('created_at')
    serializer_class = MenuItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return MenuItemPOSTSerializer
        return super(MenuItemViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        menu_item = self.get_object()
        menu_item.image.delete()
        menu_item.delete()
        return Response({
            "message": "Menu item deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all().order_by('id')
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


class OrderNowItemsListView(APIView):

    def get(self, request):
        menu_items = MenuItem.objects.all().order_by("name")
        serializer = OrderNowListSerializer(
            instance=menu_items,
            many=True,
            context={"request": request}
        )
        for item in serializer.data:
            item["avatar"] = item.pop("image")
        return Response({
            "results": serializer.data
        }, status=status.HTTP_200_OK)
