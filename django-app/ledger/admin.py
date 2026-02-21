from django.contrib import admin

from ledger.models import Wallet, Transaction
# Register your models here.


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("wallet_name", "expected_balance", "foreign_balance")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "action", "amount", "occurred_at", "wallet")
    search_fields = ("description", "amount")
    list_filter = "action",
