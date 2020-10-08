from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Wallet, Transaction
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .services import deposit_withdraw_virtual_money, \
    enable_or_disable_wallet, initialize_account
from django.db import IntegrityError
from django.urls import resolve


class WalletView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            wallet = Wallet.objects.get(owned_by=request.user)
            if wallet.status == "disabled":
                raise ValueError('Wallet is disabled')
            serializer = WalletSerializer(wallet)
            return Response({
                "status": "success",
                "data": {
                    "wallet": serializer.data
                }
            }, status=200)
        except ObjectDoesNotExist:
            error = "Wallet for the user not initiated"
        except ValueError as e:
            error = str(e)

        return Response({
            "status": "fail",
            "data": {
                "error": error
            }
        }, status=401)

    def post(self, request):
        try:
            wallet = enable_or_disable_wallet(
                user=request.user, set_to="enabled")
            serializer = WalletSerializer(wallet)
            return Response({
                "status": "success",
                "data": {
                    "wallet": serializer.data
                }
            }, status=200)

        except ObjectDoesNotExist:
            error = "Wallet for the user not initiated"
        except ValueError as e:
            error = str(e)

        return Response({
            "status": "fail",
            "data": {
                "error": error
            }
        }, status=401)

    def patch(self, request):
        try:
            wallet = enable_or_disable_wallet(
                user=request.user, set_to="disabled")
            serializer = WalletSerializer(wallet)
            return Response({
                "status": "success",
                "data": {
                    "wallet": serializer.data
                }
            }, status=200)

        except ObjectDoesNotExist:
            error = "Wallet for the user not initiated"
        except ValueError as e:
            error = str(e)

        return Response({
            "status": "fail",
            "data": {
                "error": error
            }
        }, status=401)


class DepositWithdrawVirtualMoney(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        transaction_type = resolve(request.path_info).url_name
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                wallet = request.user.wallet
                if not wallet.status == "enabled":
                    raise ValueError("Wallet is disabled")
                reference_id = request.POST.get('reference_id')
                amount = request.POST.get('amount')
                transactions = Transaction.objects.filter(
                    reference_id=reference_id)
                if transactions:
                    raise ValueError(
                        "Transaction with the reference_id already exists")
                trans_success, trans_details = deposit_withdraw_virtual_money(
                    wallet, int(amount), reference_id,
                    transaction_type=transaction_type)
                if trans_success:
                    trans_serializer = TransactionModelSerializer(
                        trans_details)
                    return Response({
                        "status": "success",
                        "data": {
                            trans_details.transaction_type: trans_serializer.data
                        }
                    }, status=201)
            except ValueError as e:
                error = str(e)
            except ObjectDoesNotExist:
                error = "Wallet for the user not initiated"
        else:
            error = serializer.errors
        return Response({
            "status": "fail",
            "data": {
                "error": error
            }
        }, status=401)


class InitializeAccount(APIView):

    def post(self, request):
        serializer = InitAccountSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = initialize_account(request.POST.get('customer_xid'))
                return Response({
                    "data": {
                        "token": token
                    },
                    "status": "success"
                }, status=201)
            except IntegrityError:
                error = "customer_xid dosent map to a valid User"
        else:
            error = serializer.errors
        return Response({
            "data": {
                "error": error
            },
            "status": "fail"
        }, status=401)
