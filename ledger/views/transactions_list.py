from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ledger.models import Transaction


class ListTransactionsView(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = "transactions"
    paginate_by = 10

    def get_queryset(self):
        return Transaction.objects.filter(wallet__user=self.request.user).order_by("-occurred_at")

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ['ledger/partials/transactions_list.html']
        return ['ledger/transactions_list.html']
