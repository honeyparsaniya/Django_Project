from django.urls import path
from .views import LoginView, OTPVerifyView, LogoutView,MyAccountView,ResentOtp,ProfileUpdateView


urlpatterns = [

    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

    path(
        "verify-otp/",
        OTPVerifyView.as_view(),
        name="verify_otp"
    ),
     path(
        "logout/",
        LogoutView,
        name="logout"
    ),
    path(
    "my-account/",
    MyAccountView.as_view(),
    name="my_account"
),
 path(
    "resent-otp/",
    ResentOtp.as_view(),
    name="resent_otp"
),
path(
    "edit-profile/",
    ProfileUpdateView.as_view(),
    name="edit_profile"
),

]