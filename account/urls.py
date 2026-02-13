from django.urls import path
from django.contrib.auth.views import LogoutView
from account.views import MyLoginView, SubExpired, ProfileView, RegisterView

app_name = "account"

urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page="account:login"), name="logout"),
    path("profile/", ProfileView.as_view(), name="details"),

    path("sub_expired/", SubExpired.as_view(), name="subscription_expired"), 
]

