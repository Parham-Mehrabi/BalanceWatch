from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db import transaction as db_transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
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


class RetrieveTransaction(LoginRequiredMixin, DetailView):

    template_name = 'ledger/partials/transaction_retrieve.html'
    def get_object(self, queryset=None):
        return get_object_or_404(
            Transaction,
            pk=self.kwargs['pk'],
            wallet__user=self.request.user
        )


class DeleteTransactionView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy('ledger:list_transactions')

    def get_object(self, queryset = ...):
        return get_object_or_404(
            Transaction,
            pk=self.kwargs['pk'],
            wallet__user=self.request.user
        )

    def post(self, request, *args, **kwargs):
        transaction = self.get_object()
        wallet = transaction.wallet

        with db_transaction.atomic():
            if transaction.action == Transaction.TransactionType.DEPOSIT:
                wallet.expected_balance -= transaction.amount
            if transaction.action == Transaction.TransactionType.WITHDRAW:
                wallet.expected_balance += transaction.amount
            
            wallet.save(update_fields=["expected_balance"])
            transaction.delete()

        if request.headers.get("HX-Request"):
            response = HttpResponse(status=204)
            response["HX-trigger"] = "transaction-deleted" 
            return response

        return HttpResponse(204)   
    