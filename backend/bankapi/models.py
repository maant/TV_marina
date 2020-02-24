from django.db import models
from django.conf import settings

class BankBill(models.Model):
    bank_account_number = models.PositiveIntegerField(primary_key=True)
    account_balance = models.PositiveIntegerField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
