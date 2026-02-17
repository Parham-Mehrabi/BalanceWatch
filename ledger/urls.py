from django.urls import path
from ledger.views import TransactionGraphView, ListTransactionsView


app_name = "ledger"

urlpatterns = [
    path("transactions_graph/", TransactionGraphView.as_view(), name="transactions_graph"),
    path("list_transactions/", ListTransactionsView.as_view(), name="list_transactions"),
]