from django.contrib import admin
from .models import User, LoginHistory, OTP


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "username",
        "email",
        "contact_number",
        "role",
        "is_active",
        "read_terms_and_conditions",
        "date_joined",
    )

    list_filter = (
        "role",
        "is_active",
        "read_terms_and_conditions",
        "date_joined",
    )

    search_fields = (
        "username",
        "email",
        "contact_number",
    )


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "username",
        "login_time",
        "logout_time",
        "duration",
    )

    list_filter = (
        "login_time",
        "logout_time",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__contact_number",
    )
    @admin.display(description="Username")
    def username(self, obj):
        return obj.user.username if obj.user_id else "-"


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "otp",
        "created_at",
        "expires_at",
        "is_verified",
    )

    list_filter = (
        "is_verified",
        "created_at",
        "expires_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__contact_number",
    )