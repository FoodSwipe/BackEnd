from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import RegistrationMonthlyCount
from accounts.serializers.user import (
    AddUserSerializer,
    RegisterUserSerializer,
    RegistrationMonthlyCountSerializer,
    UpdateUserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserWithProfileSerializer,
)
from log.models import Log


class RegisterUser(APIView):
    @staticmethod
    def post(request):
        """
        Creates a brand new user-member(x)
        """
        serializer = RegisterUserSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            user = serializer.save()
            Log.objects.create(mode="create", actor=user, detail="User registration")
            return Response(
                UserWithProfileSerializer(user).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    @staticmethod
    def post(request):
        """
        Creates a brand new user-member(x)
        """
        serializer = AddUserSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()
            Log.objects.create(
                mode="create", actor=request.user, detail="Added a new user."
            )
            return Response(
                UserCreateSerializer(user).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserWithProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(get_user_model(), pk=pk)

    def put(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User updated successfully.",
                    "data": UserCreateSerializer(self.get_object(pk)).data,
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUser(APIView):
    """
    View to list all users in the system.
    * Only staff users are able to access this view.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request):
        """
        Return a list of all users.
        """
        users = get_user_model().objects.all()
        return Response(
            UserWithProfileSerializer(users, many=True).data, status=status.HTTP_200_OK
        )

    @staticmethod
    def post(request):
        """
        Creates a brand new user-member(x)
        """
        serializer = UserCreateSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response(
                UserCreateSerializer(user).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    User Detailed Operations
    * Only staff users are able to access this view.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(get_user_model(), pk=pk)

    def get(self, request, pk):
        """
        Returns single user by pk
        """
        user = self.get_object(pk)
        serializer = UserWithProfileSerializer(
            instance=user, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Updates user by pk
        """
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(
            user, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User updated successfully.",
                    "data": UserCreateSerializer(self.get_object(pk)).data,
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Modifies user by pk
        """
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User patched successfully.",
                    "data": UserCreateSerializer(self.get_object(pk)).data,
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        Log.objects.create(
            mode="delete",
            actor=request.user,
            detail="Removed user {}".format(user.username),
        )
        return Response(
            {"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


class ToggleSuperUserStatus(APIView):
    """
    User Detailed Operations
    * Only staff users are able to access this view.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(get_user_model(), pk=pk)

    def post(self, request, pk):
        user = self.get_object(pk)
        user.is_superuser = not user.is_superuser
        user.save()
        Log.objects.create(
            mode="update", actor=request.user, detail="User superuser status toggled."
        )
        return Response(
            {"message": "User superuser status toggled successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ToggleStaffUserStatus(APIView):
    """
    User Detailed Operations
    * Only staff users are able to access this view.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(get_user_model(), pk=pk)

    def post(self, request, pk):
        user = self.get_object(pk)
        user.is_staff = not user.is_staff
        Log.objects.create(
            mode="update", actor=request.user, detail="User superuser status toggled."
        )
        user.save()
        return Response(
            {"message": "User staff status toggled successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class RegistrationSummaryListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        current_year = timezone.datetime.now().strftime("%Y")
        current_month_number = timezone.datetime.now().strftime("%m")
        current_month_name = timezone.datetime.now().strftime("%B")

        this_month_summary, created = RegistrationMonthlyCount.objects.get_or_create(
            year=current_year, month=current_month_name
        )

        this_month_users = get_user_model().objects.filter(
            date_joined__year=current_year, date_joined__month=current_month_number
        )

        this_month_summary.count = this_month_users.count()
        this_month_summary.save()

        total_summary = RegistrationMonthlyCount.objects.all()
        serializer = RegistrationMonthlyCountSerializer(
            instance=total_summary, many=True, read_only=True
        )
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)
