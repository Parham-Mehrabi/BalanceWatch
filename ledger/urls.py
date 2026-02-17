from django.urls import path
from ledger.views import TransactionGraphView


app_name = "ledger"

urlpatterns = [
    path("transactions_graph", TransactionGraphView.as_view(), name="transactions_graph"),
]