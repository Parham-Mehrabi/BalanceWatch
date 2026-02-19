from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth import login
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from account.forms import LoginForm, RegisterForm
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView



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



class MyPasswordResetDoneView(PasswordResetDoneView):
    pass

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    pass

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    pass
