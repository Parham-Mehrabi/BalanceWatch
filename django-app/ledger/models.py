from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.


class Wallet(models.Model):

    class Currencies(models.TextChoices):
        EURO = "EUR", "Euro"
        DOLLAR = "USD", "US Dollar"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallets")
    wallet_name = models.CharField(max_length=100, blank=True)

    initial_balance = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    expected_balance = models.DecimalField(max_digits=20, decimal_places=0, default=0)

    foreign_currency = models.CharField(max_length=3, choices=Currencies.choices, default=Currencies.EURO)
    foreign_balance = models.DecimalField(max_digits=20, decimal_places=0, default=0)


    def save(self, *args, **kwargs):
        if not self.wallet_name:
            username = self.user.username or f"user-{self.user.pk}"
            self.wallet_name = f"{username}-{timezone.localdate()}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{super().__str__()} - {self.wallet_name}"
    


class Transaction(models.Model):
    
    class TransactionType(models.TextChoices):
        DEPOSIT = "deposit", "Deposit"
        WITHDRAW = "withdraw", "Withdraw"

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")

    occurred_at = models.DateTimeField(default=timezone.now)

    action = models.CharField(max_length=12, choices=TransactionType.choices)

    amount = models.DecimalField(max_digits=12, decimal_places=0)

    description = models.CharField(max_length=255, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["wallet", "occurred_at"]),
            models.Index(fields=["wallet", "action", "occurred_at"]),
        ]

    def __str__(self):
        sign = "+" if self.action == self.TransactionType.DEPOSIT else "-"
        return f"{self.occurred_at}: {sign}{self.amount}"
