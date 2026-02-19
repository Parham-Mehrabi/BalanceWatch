from datetime import timedelta
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView, FormView, View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.http import HttpResponseBadRequest, HttpResponse
from django.db import transaction
from django.db.models import Sum
from account.forms import LoginForm, RegisterForm, Step1Form, Step2Form, Step3Form
from account.models import OnboardingProgress
from ledger.models import Wallet, Transaction
# Create your views here.


TOTAL_SETUP_STEPS = 3



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

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = self.request.user

        wallet:Wallet = user.wallets.first()
        context['wallet'] = wallet
        last_transactions = []
        today_transactions_sum = 0
        
        if wallet:
            last_transactions = Transaction.objects.filter(wallet=wallet).order_by("-occurred_at")[:10]
            today = timezone.localdate()
            result = Transaction.objects.filter(wallet=wallet, occurred_at__date=today).aggregate(total_sum=Sum("amount"))
            today_transactions_sum = result["total_sum"] or 0
            wallet_balance = wallet.expected_balance
        else:
            wallet.balance = 0

        context["last_transactions"] = last_transactions
        context["today_transactions_sum"] = today_transactions_sum
        context["goal_per_cent"] = round(((wallet_balance / (user.balance_goal + 1)) * 100), 2)
        context["daily_goal_percent"] = round(((today_transactions_sum / (user.daily_goal_transaction + 1)) * 100), 2)


        return context

class RegisterView(FormView):
    template_name = 'account/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("account:setup")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)



class SetupStartView(LoginRequiredMixin, TemplateView):
    
    template_name = "account/setup/start_setup.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_onboarded:
            return redirect("account:details")
        
        OnboardingProgress.objects.get_or_create(user=request.user)
        return super().dispatch(request, *args, **kwargs)


class SetupStepView(LoginRequiredMixin, View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_onboarded:
            return redirect("account:details")
        
        self.progress, _ = OnboardingProgress.objects.get_or_create(user=request.user)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if request.headers.get("HX-Request") != "true":
            return HttpResponseBadRequest("HTMX Required")
        step = self.progress.completed_steps + 1
        form = self._get_relevant_form_for_step(step=step)
        if form is None:
            return HttpResponseBadRequest("Invalid Step")
        return self._render_step(request, step, form)
    
    def post(self, request, *args, **kwargs):
        if request.headers.get("HX-Request") != "true":
            return HttpResponseBadRequest("HTMX Required")
        
        step = self.progress.completed_steps + 1
        form = self._get_relevant_form_for_step(step=step, data=request.POST)
        if form is None:
            return HttpResponseBadRequest("Invalid Step")
        
        if not form.is_valid():
            return self._render_step(request, step, form=form)

        with transaction.atomic():
            form.save()

            next_step = step + 1
            if next_step > TOTAL_SETUP_STEPS:
                request.user.is_onboarded = True
                request.user.save(update_fields=["is_onboarded"])
                self.progress.delete()

                response = HttpResponse(status=204)
                response["HX-Redirect"] = reverse("account:details")
                return response

            self.progress.completed_steps = step
            self.progress.save(update_fields=["completed_steps"])
            form = self._get_relevant_form_for_step(step=next_step)
            return self._render_step(request=request, step=next_step, form=form)


    def _get_relevant_form_for_step(self, step, data=None):
        if step == 1:
            wallet = Wallet.objects.filter(user=self.request.user)[0]
            return Step1Form(data=data, instance=wallet)
        
        if step == 2:
            wallet = Wallet.objects.filter(user=self.request.user)[0]
            return Step2Form(data=data, instance=wallet)
        
        if step == 3:
            return Step3Form(data=data, instance=self.request.user)
        
        return None
    
    def _render_step(self, request, step, form):
        context = {
            "step": step,
            "total_steps": TOTAL_SETUP_STEPS,
            "form": form
        }
        return TemplateResponse(request, "account/setup/setup_step.html", context)
