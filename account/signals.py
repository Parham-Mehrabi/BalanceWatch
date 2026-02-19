from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


from account.models import Subscription
from ledger.models import Wallet



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_sub_for_new_users(sender, instance, created, **kwargs):

    if not created: return  # this signal is for new users only

    trial = settings.DEFAULT_TRIAL_DURATION
    now = timezone.now()

    Subscription.objects.get_or_create(user=instance, defaults={"ends_at": now + trial})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet_for_new_users(sender, instance, created, **kwargs):

    if not created: return  # this signal is for new users onl

    Wallet.objects.get_or_create(user=instance)
