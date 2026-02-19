from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from ledger.models import Wallet, Transaction

class statView(LoginRequiredMixin, TemplateView):
    template_name = 'ledger/partials/stat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        wallet:Wallet = user.wallets.first()
        context['wallet'] = wallet
        today_transactions_sum = 0
        
        if wallet:
            today = timezone.localdate()
            result = Transaction.objects.filter(wallet=wallet, occurred_at__date=today).aggregate(total_sum=Sum("amount"))
            today_transactions_sum = result["total_sum"] or 0
            wallet_balance = wallet.expected_balance
        else:
            wallet.balance = 0

        context["today_transactions_sum"] = today_transactions_sum
        context["goal_per_cent"] = round(((wallet_balance / (user.balance_goal + 1)) * 100), 2)
        context["daily_goal_percent"] = round(((today_transactions_sum / (user.daily_goal_transaction + 1)) * 100), 2)

        return context