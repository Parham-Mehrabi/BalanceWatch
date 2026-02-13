from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from account.forms import LoginForm, RegisterForm
# Create your views here.


class MyLoginView(LoginView):
    template_name = "account/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True

    

class SubExpired(LoginRequiredMixin, TemplateView):
    template_name = "account/sub_expired.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.subscription.is_active:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

class RegisterView(FormView):
    template_name = 'account/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
