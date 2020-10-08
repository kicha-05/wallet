from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('init', InitializeAccount.as_view(), name='init'),
    path('wallet', WalletView.as_view(), name='wallet'),
    path('wallet/deposit', DepositWithdrawVirtualMoney.as_view(), name='deposit'),
    path('wallet/withdraw', DepositWithdrawVirtualMoney.as_view(), name='withdraw')
]
