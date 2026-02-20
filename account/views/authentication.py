from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth import login
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeDoneView

from account.forms import LoginForm, RegisterForm, MyPasswordResetForm, MySetPasswordForm


class MyLoginView(LoginView):
    template_name = "account/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True



class RegisterView(FormView):
    template_name = 'account/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("account:setup_start")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("account:login")


class MyPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("account:password_reset_done")

    template_name = "account/password_reset/reset_password.html"
    email_template_name = "account/password_reset/email_template.html"
    form_class = MyPasswordResetForm

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = "account/password_reset/password_reset_done.html"

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("account:password_reset_complete")
    template_name = "account/password_reset/password_reset_confirm.html"
    form_class = MySetPasswordForm

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "account/password_reset/reset_password_complete.html"

