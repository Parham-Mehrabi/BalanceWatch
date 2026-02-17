from django.urls import path
from ledger.views import TransactionGraphView, ListTransactionsView, RetrieveTransaction, DeleteTransactionView


app_name = "ledger"

urlpatterns = [
    path("transactions_graph/", TransactionGraphView.as_view(), name="transactions_graph"),
    path("transactions/", ListTransactionsView.as_view(), name="list_transactions"),
    path("transactions/<int:pk>/", RetrieveTransaction.as_view(), name="transaction_detail"),
    path("transactions/<int:pk>/delete/", DeleteTransactionView.as_view(), name="transaction_delete"),
]