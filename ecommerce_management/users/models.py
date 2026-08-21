from django.contrib.auth.models import AbstractUser
from django.db import models


# ============================================================
# CUSTOM USER MODEL
# ============================================================

class User(AbstractUser):

    # User roles
    ROLE_CHOICES = (
        ("user", "User"),
        ("admin", "Admin"),
    )

    # Role of the user
    # Default role is "user"
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="user"
    )

    # User contact number
    contact_number = models.CharField(
        max_length=15,
        blank=True
    )

    # Whether the user has accepted the terms and conditions
    read_terms_and_conditions = models.BooleanField(
        default=False
    )

    # User profile image
    image = models.ImageField(
        upload_to="users-profile/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.contact_number


# ============================================================
# LOGIN HISTORY MODEL
# ============================================================
# This model stores login/logout history for ALL users.
#
# It can store:
#     - Admin login history
#     - Normal user login history
#
# We do NOT need separate models for admin and user.
# The "user" ForeignKey tells us whose login history it is.
# ============================================================

class LoginHistory(models.Model):

    # The user who created this login session
    #
    # Example:
    #     Admin login  -> user = admin
    #     User login   -> user = normal user
    #
    # related_name="login_history" allows:
    #     request.user.login_history.all()
    #
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="login_history"
    )

    # Date and time when the user logged in
    login_time = models.DateTimeField(
        auto_now_add=True
    )

    # Date and time when the user logged out
    #
    # NULL/blank means the session is still active
    logout_time = models.DateTimeField(
        null=True,
        blank=True
    )

    # Total duration of the login session
    #
    # Example:
    #     0:25:30
    #     1:10:45
    duration = models.DurationField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"


# ============================================================
# OTP MODEL
# ============================================================
# Stores OTP generated for users during authentication/
# verification.
# ============================================================

class OTP(models.Model):

    # User for whom this OTP was generated
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="otps"
    )

    # Six-digit OTP
    otp = models.CharField(
        max_length=6
    )

    # Time when OTP was created
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Time after which OTP expires
    expires_at = models.DateTimeField()

    # Whether OTP has already been verified
    is_verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.user.username} - {self.otp}"