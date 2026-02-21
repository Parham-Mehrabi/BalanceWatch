from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ledger.models import Wallet
from balance_watch.turnstile import verify_turnstile


class LoginForm(AuthenticationForm):
    turnstile_token = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "input",
            "placeholder": "Username"
        })
        self.fields["password"].widget.attrs.update({
            "class": "input",
            "placeholder": "Password"
        })

    def clean(self):
        cleaned = super().clean()
        token = cleaned.get("turnstile_token")
        remote_ip = self.request.META.get("REMOTE_ADDR")
        if not token or not verify_turnstile(token=token, remoteip=remote_ip):
            raise ValidationError(
                "Human verification Failed. Please try again.")

        return cleaned


class RegisterForm(UserCreationForm):

    turnstile_token = forms.CharField(widget=forms.HiddenInput())

    def __init__(self,  *args, **kwargs):
        self.request = kwargs.pop("request", None)

        super().__init__(*args, **kwargs)
        input_classes = "block min-w-0 grow bg-transparent py-1.5 pr-3 pl-1 text-base text-white placeholder:text-gray-500 focus:outline-none sm:text-sm/6"
        input_classes2 = "block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6"
        self.fields["username"].widget.attrs.update({
            "class": input_classes,
            "placeholder": "Required",
        })

        self.fields["password1"].widget.attrs.update({
            "class": input_classes,
            "placeholder": "Required",
        })

        self.fields["password2"].widget.attrs.update({
            "class": input_classes,
            "placeholder": "Required",
        })
        self.fields["first_name"].widget.attrs.update({
            "class": input_classes2,
            "placeholder": "Optional",
        })
        self.fields["last_name"].widget.attrs.update({
            "class": input_classes2,
            "placeholder": "Optional",
        })
        self.fields["email"].widget.attrs.update({
            "class": input_classes2,
            "placeholder": "Required",
        })

    def clean(self):
        cleaned = super().clean()
        token = cleaned.get("turnstile_token")
        remote_ip = self.request.META.get("REMOTE_ADDR")
        if not token or not verify_turnstile(token=token, remoteip=remote_ip):
            raise ValidationError(
                "Human verification Failed. Please try again.")

        return cleaned

    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2",
                  "first_name", "last_name", "email")


class Step1Form(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ("foreign_currency", "foreign_balance")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["foreign_currency"].widget.attrs.update({
            "class": "input input-secondary",
        })
        self.fields["foreign_currency"].help_text = (
            "tell BalanceWatch how to calculate your foreign balance "
            "based on the selected currency"
        )

        self.fields["foreign_balance"].widget.attrs.update({
            "class": "input input-secondary",
            "step": 500
        })
        self.fields["foreign_balance"].help_text = "how much of your balance would be in this form"


class Step2Form(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ("initial_balance",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["initial_balance"].widget.attrs.update({
            "class": "input input-secondary",
            "step": 100_000_000
        })
        self.fields["initial_balance"].help_text = (
            "how much money you already have in your account "
            "declare that based on tomans"
        )


class Step3Form(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["daily_goal_transaction", "balance_goal"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["daily_goal_transaction"].widget.attrs.update({
            "class": "input input-secondary",
            "step": 1_000_000
        })
        self.fields["daily_goal_transaction"].help_text = (
            "the amount of total transaction you are going to make daily; "
            "this goal would be fulfilled daily by making a enough transactions"
        )
        self.fields["balance_goal"].widget.attrs.update({
            "class": "input input-secondary",
            "step": 100_000_000
        })
        self.fields["balance_goal"].help_text = (
            "the amount of balance you are going to reach at the end of period "
        )


class MyPasswordResetForm(PasswordResetForm):
    turnstile_token = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({
            "class": "input",
            "placeholder": "Email"
        })

    def clean(self):
        cleaned = super().clean()
        token = cleaned.get("turnstile_token")
        remote_ip = self.request.META.get("REMOTE_ADDR")
        if not token or not verify_turnstile(token=token, remoteip=remote_ip):
            raise ValidationError(
                "Human verification Failed. Please try again.")


class MySetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(user, *args, **kwargs)

        self.fields["new_password1"].widget.attrs.update({
            "class": "input",
            "placeholder": "password"
        })
        self.fields["new_password2"].widget.attrs.update({
            "class": "input",
            "placeholder": "Confirm Password"
        })
