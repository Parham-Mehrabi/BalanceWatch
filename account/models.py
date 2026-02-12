from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings


class User(AbstractUser):
    
    pass    # default user would do for now



class Subscription(models.Model):

    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscription")
    ends_at = models.DateTimeField(default=timezone.now)
    
    @property
    def is_active(self) -> bool:
        if self.ends_at:
            return self.ends_at > timezone.now()
        return True
