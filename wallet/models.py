from django.db import models
from django.contrib.auth.models import User
from .constants import TRANSACTION_STATUS_CHOICES, TRANSACTION_TYPE_CHOICES, \
    WALLET_STATUS_CHOICES


class Wallet(models.Model):
    owned_by = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=WALLET_STATUS_CHOICES,
                              default="disabled")
    balance = models.PositiveIntegerField(default=0)
    enabled_at = models.DateTimeField(auto_now=False, blank=True, null=True)
    disabled_at = models.DateTimeField(auto_now=False, blank=True, null=True)

    def __str__(self):
        return str(self.owned_by)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=TRANSACTION_STATUS_CHOICES,
                              default=None,
                              null=True, blank=True)
    reference_id = models.TextField(max_length=50, unique=True)
    amount = models.PositiveIntegerField(default=0)
    transaction_type = models.CharField(max_length=100,
                                        choices=TRANSACTION_TYPE_CHOICES,
                                        default=None, null=True, blank=True)
    transaction_by = models.ForeignKey(User, on_delete=models.CASCADE)
    transactioned_at = models.DateTimeField(
        auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.reference_id
