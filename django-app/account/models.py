from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings


class User(AbstractUser):
    
    is_onboarded = models.BooleanField(default=False)
    daily_goal_transaction = models.DecimalField(max_digits=12, default=0, decimal_places=0)
    
    balance_goal = models.DecimalField(max_digits=20, decimal_places=0, default=0)

    email = models.EmailField(unique=True, blank=False, null=False)
    email_verified = models.BooleanField(default=False)


class Subscription(models.Model):

    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscription")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ends_at = models.DateTimeField(default=timezone.now)
        
    @property
    def is_active(self) -> bool:
        if self.ends_at:
            return self.ends_at > timezone.now()
        return True


class OnboardingProgress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="setup_step")
    completed_steps = models.PositiveSmallIntegerField(default=0)
