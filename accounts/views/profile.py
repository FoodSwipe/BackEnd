from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from accounts.serializers.profile import (ProfileContactOnlySerializer,
                                          ProfilePOSTSerializer,
                                          ProfileSerializer)
from utils.helper import generate_url_for_media_resources


class ListProfiles(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        serializer = generate_url_for_media_resources(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        """
        Return a profile of a user
        """
        user = get_object_or_404(get_user_model(), pk=pk)
        profile = Profile.objects.get(user=user)
        return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)


class ProfileDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Profile, pk=pk)

    def get(self, request, pk):
        """
        Returns particular profile
        """
        profile = self.get_object(pk)
        return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Updates provided member by pk
        """
        profile = self.get_object(pk)
        serializer = ProfilePOSTSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Profile updated successfully.",
                    "data": ProfileSerializer(self.get_object(pk)).data,
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Modifies provided member by pk
        """
        profile = self.get_object(pk)
        serializer = ProfilePOSTSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Profile patched successfully.",
                    "data": ProfileSerializer(self.get_object(pk)).data,
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileContactListView(generics.ListAPIView):
    serializer_class = ProfileContactOnlySerializer

    def get_queryset(self):
        return Profile.objects.all().order_by("user__date_joined")
