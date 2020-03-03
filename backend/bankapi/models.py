from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class BankAccount(models.Model):
    """
    Info about every bank account including number(code),
    balance(roubles) (both integer, safety from 0 to 2147483647)
    and owner(human)
    """
    account_number = models.PositiveIntegerField(
        primary_key=True,
        validators=[MinValueValidator(0), MaxValueValidator(2147483647)],
    )
    account_balance = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2147483647)],
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return 'Account {0} has balance {1} and belongs to {2}'.format(
            self.account_number, self.account_balance, self.owner,
        )


class BankTransaction(models.Model):
    """
    Info about money transfer between bank accounts
    """
    acc_from = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING,
                                 related_name='account_from')
    acc_to = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING,
                               related_name='account_to')
    transfer_amount = models.PositiveIntegerField()

    @classmethod
    def create(cls, transfer_amount=transfer_amount, acc_from=acc_from, acc_to=acc_to):
        entity = cls(transfer_amount=transfer_amount, acc_from=acc_from, acc_to=acc_to)
        entity.save()

    def __str__(self):
        return 'Transact {0} roubles from {1} to {2} account'.format(
            self.transfer_amount, self.acc_from, self.acc_to,
        )
