from django.utils import timezone
from account.models import Subscription

def subscription_context(request):
    if not request.user.is_authenticated:
        print(11)
        return {}
    
    sub = Subscription.objects.filter(user=request.user).first()
    if not sub:
        sub = {
            "remaining": 0,
            "is_active": False
        }
    
    context = {
        "remaining_days": (sub.ends_at - timezone.now()).days,
        "is_active": sub.is_active

    }
    return context
