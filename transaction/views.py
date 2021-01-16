from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from transaction.models import Transaction
from transaction.serializers import TransactionPOSTSerializer, TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return TransactionPOSTSerializer
        return super(TransactionViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        transaction = self.get_object()
        transaction.delete()
        return Response(
            {"message": "Transaction deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
