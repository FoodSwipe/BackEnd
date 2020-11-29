from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.user import UserCreateSerializer, UserUpdateSerializer


class ListUser(APIView):
    """
    View to list all users in the system.
    * Only staff users are able to access this view.
    """
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    @staticmethod
    def get(request):
        """
        Return a list of all users.
        """
        users = get_user_model().objects.all()
        return Response(UserCreateSerializer(users, many=True).data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        """
        Creates a brand new user-member(x)
        """
        serializer = UserCreateSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response(UserCreateSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    User Detailed Operations
    * Only staff users are able to access this view.
    """
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(get_user_model(), pk=pk)

    def get(self, request, pk):
        """
        Returns single user by pk
        """
        user = self.get_object(pk)
        return Response(UserCreateSerializer(user).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Updates user by pk
        """
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(
            user, data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User updated successfully.",
                "data"   : UserCreateSerializer(self.get_object(pk)).data
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Modifies user by pk
        """
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User patched successfully.",
                "data"   : UserCreateSerializer(self.get_object(pk)).data
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response({
            "message": "User deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)