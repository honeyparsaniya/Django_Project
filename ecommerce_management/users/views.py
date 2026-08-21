from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import FormView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from datetime import timedelta
import random

from .forms import LoginForm, OTPForm, ProfileUpdateForm
from .models import OTP, LoginHistory


User = get_user_model()


class LoginHistoryManager:

    @staticmethod
    def start(request, user):
        # Create a login history record for the user
        history = LoginHistory.objects.create(
            user=user
        )

        # Store the history ID in the current session
        request.session["login_history_id"] = history.id

        return history

    @staticmethod
    def close(request):
        # Get the current login history ID from the session
        history_id = request.session.get("login_history_id")

        # If there is no history ID or user is not authenticated,
        # remove the session value and stop.
        if not history_id or not request.user.is_authenticated:
            request.session.pop("login_history_id", None)
            return None

        # Find the active login history belonging to
        # the currently logged-in user.
        history = LoginHistory.objects.filter(
            id=history_id,
            user=request.user,
            logout_time__isnull=True,
        ).first()

        if history:
            # Store logout time
            history.logout_time = timezone.now()

            # Calculate session duration
            history.duration = timedelta(
                seconds=int(
                    (
                        history.logout_time
                        - history.login_time
                    ).total_seconds()
                )
            )

            # Save logout time and duration
            history.save(
                update_fields=[
                    "logout_time",
                    "duration"
                ]
            )

        # Remove history ID from session
        request.session.pop(
            "login_history_id",
            None
        )

        return history


# =========================================================
# LOGIN VIEW
# =========================================================

@method_decorator(ensure_csrf_cookie, name="dispatch")
class LoginView(FormView):

    template_name = "login.html"
    form_class = LoginForm

    def form_valid(self, form):

        # =================================================
        # GET FORM DATA
        # =================================================

        username = form.cleaned_data["username"]
        contact_number = form.cleaned_data["contact_number"]


        # =================================================
        # CHECK USER
        # =================================================

        user = User.objects.filter(
            username=username
        ).first()


        # =================================================
        # EXISTING USER
        # =================================================

        if user:

            # Check whether contact number matches
            if user.contact_number != contact_number:

                form.add_error(
                    "contact_number",
                    "Contact number does not match this username."
                )

                return self.form_invalid(form)


        # =================================================
        # NEW USER
        # =================================================

        else:

            user = User.objects.create_user(
                username=username,
                contact_number=contact_number
            )


        # =================================================
        # DELETE OLD UNUSED OTPs
        # =================================================

        OTP.objects.filter(
            user=user,
            is_verified=False
        ).delete()


        # =================================================
        # GENERATE OTP
        # =================================================

        otp_code = str(
            random.randint(100000, 999999)
        )


        # =================================================
        # OTP EXPIRY
        # =================================================

        expires_at = (
            timezone.now()
            + timedelta(minutes=5)
        )


        # =================================================
        # SAVE OTP
        # =================================================

        OTP.objects.create(
            user=user,
            otp=otp_code,
            expires_at=expires_at
        )


        # =================================================
        # STORE USER ID IN SESSION
        # =================================================

        self.request.session["otp_user_id"] = user.id


        # =================================================
        # TEST OTP
        # =================================================

        print()
        print("========================================")
        print("             OTP GENERATED")
        print("========================================")
        print("Username :", user.username)
        print("Contact  :", user.contact_number)
        print("OTP      :", otp_code)
        print("Expires  :", expires_at)
        print("========================================")
        print()


        # =================================================
        # REDIRECT TO OTP PAGE
        # =================================================

        return redirect("verify_otp")
# =========================================================
# OTP VERIFICATION VIEW
# =========================================================
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
@method_decorator(ensure_csrf_cookie, name="dispatch")
class OTPVerifyView(FormView):

    template_name = "OTP.html"
    form_class = OTPForm

    def dispatch(self, request, *args, **kwargs):

        # -------------------------------------------------
        # Check whether user came through Login page
        # -------------------------------------------------

        if "otp_user_id" not in request.session:
            return redirect("login")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        # -------------------------------------------------
        # Get OTP entered by user
        # -------------------------------------------------

        otp_code = form.cleaned_data["otp"]

        # -------------------------------------------------
        # Get user ID from session
        # -------------------------------------------------

        user_id = self.request.session.get("otp_user_id")

        if not user_id:
            return redirect("login")

        # -------------------------------------------------
        # Find user
        # -------------------------------------------------

        try:

            user = User.objects.get(
                id=user_id
            )

        except User.DoesNotExist:

            return redirect("login")

        # -------------------------------------------------
        # Get latest unverified OTP
        # -------------------------------------------------

        otp_obj = OTP.objects.filter(
            user=user,
            is_verified=False
        ).order_by("-created_at").first()

        # -------------------------------------------------
        # OTP does not exist
        # -------------------------------------------------

        if not otp_obj:

            form.add_error(
                "otp",
                "OTP not found. Please login again."
            )

            return self.form_invalid(form)

        # -------------------------------------------------
        # Check OTP expiry
        # -------------------------------------------------

        if timezone.now() > otp_obj.expires_at:

            form.add_error(
                "otp",
                "OTP has expired. Please login again."
            )

            return self.form_invalid(form)

        # -------------------------------------------------
        # Check whether OTP is correct
        # -------------------------------------------------

        if otp_obj.otp != otp_code:

            form.add_error(
                "otp",
                "Invalid OTP. Please try again."
            )

            return self.form_invalid(form)

        # -------------------------------------------------
        # OTP is correct
        # -------------------------------------------------

        otp_obj.is_verified = True
        otp_obj.save()

        # -------------------------------------------------
        # Remove temporary OTP session
        # -------------------------------------------------

        self.request.session.pop(
            "otp_user_id",
            None
        )

        # -------------------------------------------------
        # Login user
        # -------------------------------------------------

        login(
            self.request,
            user
        )

        # -------------------------------------------------
        # Create Login History
        # -------------------------------------------------

        # Store the history ID so the same record can be closed at logout.
        LoginHistoryManager.start(self.request, user)

        print("USER:", self.request.user)  
        print("USER:", self.request.user)
        print("AUTHENTICATED:", self.request.user.is_authenticated)

        # -------------------------------------------------
        # Redirect to home page
        # -------------------------------------------------

        return redirect("index_page")


# =========================================================
# LOGOUT VIEW
# =========================================================
def LogoutView(request):

    print("\n========== LOGOUT DEBUG ==========")
    print("USER:", request.user)
    print("AUTHENTICATED:", request.user.is_authenticated)
    print("HISTORY ID:", request.session.get("login_history_id"))

    history = LoginHistoryManager.close(request)

    print("HISTORY:", history)

    if history:
        print("LOGOUT TIME:", history.logout_time)
        print("DURATION:", history.duration)
    else:
        print("❌ HISTORY WAS NOT CLOSED")

    print("==================================\n")

    logout(request)

    return redirect("index_page")


# =========================================================
# MY ACCOUNT VIEW
# =========================================================

# Import required for protecting the page
from django.contrib.auth.decorators import login_required

# Required to use login_required with a class-based view
from django.utils.decorators import method_decorator

# TemplateView is used to display the My Account HTML page
from django.views.generic import TemplateView


# =========================================================
# MY ACCOUNT
# =========================================================

# Allow access only to logged-in users
# If user is not logged in, redirect to login page
@method_decorator(
    login_required(login_url="login"),
    name="dispatch"
)
class MyAccountView(TemplateView):

    # HTML template that will be displayed
    template_name = "myAccount.html"

    # Send logged-in user's information to the template
    def get_context_data(self, **kwargs):

        # Get the existing context
        context = super().get_context_data(**kwargs)


        # Get currently logged-in user
        context["account_user"] = self.request.user

        # Return the context to the template
        return context
# =========================================================
# EDIT PROFILE VIEW
# =========================================================

@method_decorator(
    login_required(login_url="login"),
    name="dispatch"
)
class ProfileUpdateView(FormView):

    # Admin profile template
    template_name = "editProfile.html"

    # Admin profile form
    form_class = ProfileUpdateForm

    


    # =====================================================
    # GET
    # =====================================================

    def get(self, request, *args, **kwargs):

        # Create form using currently logged-in admin
        form = self.form_class(
            instance=request.user
        )

        return self.render_to_response(
            self.get_context_data(
                form=form
            )
        )


    # =====================================================
    # POST
    # =====================================================

    def post(self, request, *args, **kwargs):

        # Create form with submitted data
        form = self.form_class(
            request.POST,
            request.FILES,
            instance=request.user
        )

        # Check form validation
        if form.is_valid():

            # Save changes to current logged-in admin
            form.save()

            # Go back to profile page
            return redirect("my_account")

        # If validation fails
        return self.render_to_response(
            self.get_context_data(
                form=form
            )
        )


    # =====================================================
    # CONTEXT DATA
    # =====================================================

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Current logged-in user
        user = self.request.user

        # Get login history of ONLY this user
        login_history = LoginHistory.objects.filter(
            user=user
        ).order_by(
            "-login_time"
        )

        # Send login history to template
        context["login_history"] = login_history

        return context
    # =====================================================
    # CONTEXT DATA
    # =====================================================

    def get_context_data(self, **kwargs):

        # Get existing context
        context = super().get_context_data(**kwargs)

        # Get login history of currently logged-in user
        context["login_history"] = LoginHistory.objects.filter(
            user=self.request.user
        ).order_by("-login_time")

        return context
# =========================================================
# RESEND OTP VIEW
# =========================================================

class ResentOtp(FormView):

    def get(self, request, *args, **kwargs):
        

        # -------------------------------------------------
        # Get user ID from session
        # -------------------------------------------------

        user_id = request.session.get("otp_user_id")

        # If user ID is not available,
        # send user back to login page
        if not user_id:
            return redirect("login")

        # -------------------------------------------------
        # Find user
        # -------------------------------------------------

        try:

            user = User.objects.get(
                id=user_id
            )

        except User.DoesNotExist:

            return redirect("login")

        # -------------------------------------------------
        # Delete old unused OTP
        # -------------------------------------------------

        OTP.objects.filter(
            user=user,
            is_verified=False
        ).delete()

        # -------------------------------------------------
        # Generate new OTP
        # -------------------------------------------------

        otp_code = str(
            random.randint(100000, 999999)
        )

        # -------------------------------------------------
        # Set OTP expiry time
        # -------------------------------------------------

        expires_at = (
            timezone.now()
            + timedelta(minutes=5)
        )

        # -------------------------------------------------
        # Save new OTP
        # -------------------------------------------------

        OTP.objects.create(
            user=user,
            otp=otp_code,
            expires_at=expires_at
        )

        # -------------------------------------------------
        # Print OTP for testing
        # -------------------------------------------------

        print()
        print("========================================")
        print("           OTP RESENT")
        print("========================================")
        print("Username :", user.username)
        print("Contact  :", user.contact_number)
        print("OTP      :", otp_code)
        print("Expires  :", expires_at)
        print("========================================")
        print()

        # -------------------------------------------------
        # Redirect back to OTP page
        # -------------------------------------------------

        return redirect("verify_otp")

