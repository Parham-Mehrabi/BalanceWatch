from django.contrib import admin
from django.contrib.auth import get_user_model
from account.models import Subscription
from django.utils import timezone


UserModel = get_user_model()

# Register your models here.


admin.site.register(UserModel)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "ends_at", "duration", "status")
    search_fields = ("user__username", "user__email", "user__first_name")
    list_filter = ("ends_at",)

    @admin.display(description="Duration", ordering="ends_at")
    def duration(self, obj:Subscription):
        now = timezone.now()
        ends_at = obj.ends_at
        if now > ends_at:
            return f"expired"
        duration = ends_at - now
        return f"{duration.days} days"
    
    @admin.display(description="Status", ordering="ends_at")
    def status(self, obj:Subscription):
        if not obj.ends_at: return "Unlimited"
        return "Active" if obj.is_active else "Inactive"
