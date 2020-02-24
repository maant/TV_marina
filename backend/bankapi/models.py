from django.db import models

class BankBill(models.Model):
    bill_number = models.PositiveIntegerField(primary_key=True)
