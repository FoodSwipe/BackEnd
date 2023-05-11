from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from item.models import ItemType, MenuItem, TopAndRecommendedItem
from item.serializers import (ItemTypeSerializer, MenuItemPOSTSerializer,
                              MenuItemSerializer, OrderNowListSerializer,
                              TopAndRecommendedMenuItemPostSerializer,
                              TopAndRecommendedMenuItemSerializer)
from log.models import Log


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all().order_by("created_at")
    serializer_class = MenuItemSerializer
    filterset_fields = ["is_veg", "item_type", "is_bar_item", "menu_item_group"]
    search_fields = ["name", "ingredients", "menu_item_group__name"]

    def get_serializer_class(self):
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            return MenuItemPOSTSerializer
        return super(MenuItemViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        menu_item = self.get_object()
        menu_item.image.delete()
        menu_item.delete()
        Log.objects.create(
            mode="delete",
            actor=request.user,
            detail="Menu item deleted. ({})".format(menu_item.name),
        )
        return Response(
            {"message": "Menu item deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all().order_by("id")
    serializer_class = ItemTypeSerializer
    search_fields = ["name"]

    def get_permissions(self):
        if self.action == "list":
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        item_type = self.get_object()
        item_type.badge.delete()
        item_type.delete()
        return Response(
            {"message": "Menu item type deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class OrderNowItemsListView(APIView):

    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        menu_items = MenuItem.objects.order_by("name")
        serializer = OrderNowListSerializer(
            instance=menu_items, many=True, context={"request": request}
        )
        for item in serializer.data:
            item["avatar"] = item.pop("image")
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)


class TopRecommendedMenuItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    serializer_class = TopAndRecommendedMenuItemSerializer
    queryset = TopAndRecommendedItem.objects.all().order_by("-menu_item__created_at")

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return TopAndRecommendedMenuItemPostSerializer
        return super(TopRecommendedMenuItemViewSet, self).get_serializer_class()


class TopItemsListView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        all_items = TopAndRecommendedItem.objects.filter(top=True).order_by(
            "-menu_item__created_at"
        )
        serializer = TopAndRecommendedMenuItemSerializer(
            instance=all_items, many=True, read_only=True, context={"request": request}
        )
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)


class RecommendedItemsListView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        all_items = TopAndRecommendedItem.objects.filter(recommended=True).order_by(
            "-menu_item__created_at"
        )
        serializer = TopAndRecommendedMenuItemSerializer(
            instance=all_items, many=True, read_only=True, context={"request": request}
        )
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)
