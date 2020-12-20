from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from item_group.models import MenuItemGroup
from item_group.serializers import MenuItemGroupSerializer, MenuItemGroupPOSTSerializer, ItemGroupSerializer


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
        menu_item_group.image.delete()
        menu_item_group.delete()
        return Response({
            "message": "Menu item group deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class MenuItemGroupsWithItemListView(APIView):

    def get(self, request):
        try:
            menu_item_group = MenuItemGroup.objects.all()
            serializer = ItemGroupSerializer(
                instance=menu_item_group,
                many=True,
                context={"request": request}
            )
            return Response({
                "results": serializer.data
            }, status=status.HTTP_200_OK)
        except MenuItemGroup.DoesNotExist:
            return Response({
                "message": "Menu item group not found."
            }, status=status.HTTP_404_NOT_FOUND)
