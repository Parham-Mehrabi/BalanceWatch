from django.shortcuts import redirect


class ForceProfileSetupMiddleware:

    WHITELIST = {
        "account:logout",
        "account:subscription_expired",
        "account:setup_start",
        "account:setup_step",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request): 
        return self.get_response(request)
    
    def process_view(self, request, view_func, view_args, view_kwargs):

        if request.resolver_match.view_name in self.WHITELIST:
            return None
        if request.resolver_match.view_name.startswith("admin"):
            return None

        if request.user.is_authenticated and not request.user.is_onboarded:
            return redirect("account:setup_start")
        return None
    