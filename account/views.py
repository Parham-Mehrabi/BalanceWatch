from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from account.forms import LoginForm

# Create your views here.


class MyLoginView(LoginView):
    template_name = "account/login.html"
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    