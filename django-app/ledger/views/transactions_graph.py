from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum
from django.views.generic import TemplateView
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from ledger.models import Transaction


class TransactionGraphView(LoginRequiredMixin, TemplateView):
    template_name = "ledger/partials/transactions_graph.html"

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        wallet = self.request.user.wallets.first()

        now = timezone.now()
        start_date = (now - relativedelta(months=5)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        result = (Transaction.objects.filter(wallet=wallet, occurred_at__gte=start_date)
                .annotate(month=TruncMonth("occurred_at"))
                .values("month", "action")
                .annotate(transaction_count=Count("id"), total_sum=Sum("amount"))
                ).order_by("month", "action")


        months = []
        cursor = date(start_date.year, start_date.month, 1)
        end_month = date(now.year, now.month, 1)
        while cursor <= end_month:
            months.append(cursor)
            cursor = cursor + relativedelta(months=1)

        labels = [m.strftime("%Y-%m") for m in months]

        total_deposit = {month: 0 for month in labels}
        total_withdraw = {month: 0 for month in labels}
        deposit_count = {month: 0 for month in labels}
        withdraw_count = {month: 0 for month in labels}
        total_transactions = 0
        total_deposit_sum = 0
        total_withdraw_sum = 0
        for row in result:
            month = row["month"].date().strftime("%Y-%m")
            action = row["action"]
            transaction_count = row["transaction_count"] or 0
            amount = int(row["total_sum"] or 0)
            total_transactions += amount
            if action == Transaction.TransactionType.DEPOSIT:
                total_deposit_sum += amount
                total_deposit[month] = amount
                deposit_count[month] = transaction_count
            else: 
                total_withdraw_sum += amount
                total_withdraw[month] = amount
                withdraw_count[month] = transaction_count

        rows = []
        for month in labels:
            rows.append({
                "month": month,
                "total_deposit": total_deposit[month],
                "total_withdraw": total_withdraw[month],
                "deposit_count": deposit_count[month],
                "withdraw_count": withdraw_count[month],
            })

        context["labels"] = labels
        context["total_deposit"] = [total_deposit[l] for l in labels]
        context["total_withdraw"] = [total_withdraw[l] for l in labels]
        context["deposit_count"] = [deposit_count[l] for l in labels]
        context["withdraw_count"] = [withdraw_count[l] for l in labels]
        context["total_transactions"] = total_transactions
        context["total_deposit_sum"] = total_deposit_sum
        context["total_withdraw_sum"] = total_withdraw_sum
        context["data_table"] = rows
        return context
    