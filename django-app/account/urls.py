from django.urls import path
from account.views import (MyLoginView,
                            SubExpired,
                            ProfileView,
                            RegisterView,
                            SetupStartView,
                            SetupStepView,
                            MyPasswordResetView,
                            MyLogoutView,
                            MyPasswordResetDoneView,
                            MyPasswordResetConfirmView,
                            MyPasswordResetCompleteView,
                        )



app_name = "account"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),

    path("password_rest/", MyPasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),



    path("sub_expired/", SubExpired.as_view(), name="subscription_expired"), 
    path("profile/", ProfileView.as_view(), name="details"),


    path("profile/setup/", SetupStartView.as_view(), name="setup_start"),
    path("profile/setup/step/", SetupStepView.as_view(), name="setup_step")

]

