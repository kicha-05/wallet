from .models import *
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.db import IntegrityError

def enable_or_disable_wallet(user, set_to):
    wallet = user.wallet
    if wallet.status == set_to:
        raise ValueError('Wallet already ' + set_to)
    wallet.status = set_to
    wallet.enabled_at = timezone.now()
    wallet.save()
    return wallet


def deposit_withdraw_virtual_money(wallet, amount, reference_id, transaction_type):
    try:
        if amount <= 0:
            raise ValueError("Amount should be a positive integer")
        if transaction_type == "deposit":
            wallet.balance += amount
        else:
            if wallet.balance < amount:
                raise ValueError("Insufficient Balance in wallet")
            wallet.balance -= amount
        wallet.save()
        transaction_details = Transaction.objects.create(
            status="success",
            transaction_type=transaction_type,
            wallet=wallet,
            amount=amount,
            transactioned_at=timezone.now(),
            transaction_by=wallet.owned_by,
            reference_id=reference_id
        )
        return True, transaction_details
    except (ValueError, IntegrityError) as exc:
        return False, exc


def initialize_account(customer_xid):
    wallet, _ = Wallet.objects.get_or_create(owned_by_id=customer_xid)
    token, _ = Token.objects.get_or_create(user_id=customer_xid)
    return token.key
