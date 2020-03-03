from django.contrib.auth.models import User
from django.db.models import F
from django.db import transaction

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import APIException, PermissionDenied

from .models import BankTransaction, BankAccount
from .permissions import IsAccountAdminOrReadOnly
from .serializers import (
    UserSerializer, BankTransactionSerializer, BankAccountSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAccountAdminOrReadOnly]


class BankAccountViewSet(viewsets.ModelViewSet):
    """
    API to manage and look for bank accounts
    """
    queryset = BankAccount.objects.all().order_by('owner')
    serializer_class = BankAccountSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        if user:
            if user.is_superuser:
                return super().list(request, *args, **kwargs)
            if user.is_authenticated:
                queryset = self.get_queryset().filter(owner__exact=user)
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)

        raise PermissionDenied()


class BankTransactionViewSet(viewsets.ModelViewSet):
    """
    API to manage and look for users transactions

    API endpoint that allows authenticated users
    to swap money from self-accounts to any account
    """
    queryset = BankTransaction.objects.all().order_by('acc_from')
    serializer_class = BankTransactionSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        if user:
            if user.is_superuser:
                return super().list(request, *args, **kwargs)
            if user.is_authenticated:
                queryset = BankTransaction.objects.annotate(acc_from__owner=F('user'))
                serializer = BankTransactionSerializer(queryset, many=True)
                return Response(serializer.data)

        raise PermissionDenied()

    @staticmethod
    def validate_accounts(user, acc_from, acc_to, transfer_amount):
        acc_from_obj = BankAccount.objects.filter(account_number=acc_from)
        acc_to_obj = BankAccount.objects.filter(account_number=acc_to)
        if len(acc_from_obj) != 1 or len(acc_to_obj) != 1 or acc_from_obj[0].owner != user:
            raise PermissionDenied()

        if acc_from_obj[0].account_balance - transfer_amount < 0:
            raise APIException('Недостаточно средств')

        return acc_from_obj.first(), acc_to_obj.first()

    def create(self, request, *args, **kwargs):
        user = request.user
        if user and user.is_authenticated:
            transfer_amount = int(request.data.get('transfer_amount'))
            acc_from = int(request.data.get('acc_from'))
            acc_to = int(request.data.get('acc_to'))

            acc_from_obj, acc_to_obj = self.validate_accounts(user, acc_from, acc_to, transfer_amount)

            with transaction.atomic():  # TODO (WARNING) check if we can get here a raise condition
                # if this code executed at exact same time for single acc_from_obj
                # two different transactions could be created for same account_balance value
                # in sqlite we can see that so some of transactions was created but account_balance has no changes
                # simple way to reproduce set breakpoint at next line and make two different requests transferring
                # balance from acc1 to acc2 and second one from acc1 to acc3 after both requests hit the breakpoint
                # just run both of them
                BankTransaction.create(transfer_amount=transfer_amount, acc_from=acc_from_obj, acc_to=acc_to_obj)
                acc_from_obj.account_balance -= transfer_amount
                acc_to_obj.account_balance += transfer_amount
                acc_from_obj.save()
                acc_to_obj.save()
                self.validate_accounts(user, acc_from, acc_to, 0)  # <- why is this?
        return Response('OK')
