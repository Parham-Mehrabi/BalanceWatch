from django.shortcuts import redirect
from django.urls import reverse
from django.core.cache import cache

def check_sub_and_cache(user):
    """
    check if user has an active subscription and cache it
    """
    TTL = 120
    result = cache.get(f"user:{user.id}-SubStatus")
    
    if result is None:
        result = user.subscription.is_active
        cache.set(f"user:{user.id}-SubStatus", result, TTL)
    return result    


class ActiveSubscriptionMiddleware:
    """
    If user is logged without an active subscription, block access except for whitelist URLs.
    """

    WHITELIST = [
        "account:login",
        "account:register",
        "account:subscription_expired"
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request): 
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        resolver_match = request.resolver_match        
        
        if resolver_match.view_name in self.WHITELIST:
            return None
        
        if not request.user.is_authenticated:
            return redirect("account:login")
        if request.user.is_superuser:
            return None
        if check_sub_and_cache(request.user):
            return None
        return redirect(reverse("account:subscription_expired"))
        
        