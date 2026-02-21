from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect



class SubExpired(LoginRequiredMixin, TemplateView):
    template_name = "account/sub_expired.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.subscription.is_active:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    