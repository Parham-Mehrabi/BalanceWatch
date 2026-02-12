from django.contrib import admin
from django.contrib.auth import get_user_model
from account.models import Subscription

UserModel = get_user_model()

# Register your models here.


admin.site.register(UserModel)
admin.site.register(Subscription)
