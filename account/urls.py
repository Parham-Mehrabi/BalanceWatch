from django.urls import path
from account.views import MyLoginView

app_name = "account"

urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
]
