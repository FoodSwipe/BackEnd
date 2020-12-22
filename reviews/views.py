from rest_framework import viewsets, status
from rest_framework.response import Response

from reviews.models import Review
from reviews.serializers import ReviewSerializer, ReviewPostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ReviewPostSerializer
        return super(ReviewViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        review.image.delete()
        review.delete()
        return Response({
            "message": "Menu item type deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)
