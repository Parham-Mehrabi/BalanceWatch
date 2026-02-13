from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model


class LoginForm(AuthenticationForm):
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        
        self.fields["username"].widget.attrs.update({
            "class": "input",
            "placeholder": "Username"
        })
        self.fields["password"].widget.attrs.update({
            "class": "input",
            "placeholder": "Password"
        })
  
  

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        
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
            "placeholder": "Optional",
        })    

    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2", "first_name", "last_name", "email")
