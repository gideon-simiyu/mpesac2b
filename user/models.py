from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4

class Account(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    paybill = models.CharField(max_length=50)
    api_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    api_secret = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


from django.db import models


class Transaction(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=20, unique=True)
    transaction_time = models.DateTimeField()
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    business_short_code = models.CharField(max_length=10)
    bill_ref_number = models.CharField(max_length=50)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    org_account_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    third_party_trans_id = models.CharField(max_length=20, blank=True, null=True)
    msisdn = models.CharField(max_length=15)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.trans_amount}'
