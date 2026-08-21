from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from users.forms import ProfileUpdateForm
from users.models import *
from django.utils import timezone


# Allow only admin users
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "/account/login/"

    def test_func(self):
        return self.request.user.role == "admin"
    
class DashboardView(TemplateView):

    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Admin ko chhod kar saare users
        users = User.objects.exclude(
            role="admin"
        )
        context["users"] = users

        return context

class AddUserView(TemplateView):
    template_name = "dashboard/add-user.html"
    


class AlertsView(TemplateView):
    template_name = "dashboard/alerts.html"


class BlankView(TemplateView):
    template_name = "dashboard/blank.html"


class ChartsView(TemplateView):
    template_name = "dashboard/charts.html"


class ComponentsView(TemplateView):
    template_name = "dashboard/components.html"


class CreateAgentView(TemplateView):
    template_name = "dashboard/create-agent.html"


class ForgotPasswordView(TemplateView):
    template_name = "dashboard/forgot-password.html"


class FormsView(TemplateView):
    template_name = "dashboard/forms.html"


class LoginView(TemplateView):
    template_name = "dashboard/login.html"


class ModalsView(TemplateView):
    template_name = "dashboard/modals.html"

class ProfileView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

    template_name = "dashboard/profile.html"

    login_url = "/account/login/"

    def test_func(self):
        return self.request.user.role == "admin"

    # ==========================================
    # GET REQUEST
    # ==========================================

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Current logged-in admin
        admin = self.request.user

        # Profile form
        form = ProfileUpdateForm(
            instance=admin
        )

        # Admin login history
        login_history = LoginHistory.objects.filter(
            user=admin
        ).order_by("-login_time")

        context["form"] = form
        context["login_history"] = login_history

        return context

    # ==========================================
    # POST REQUEST
    # ==========================================

    def post(self, request, *args, **kwargs):

        # Current logged-in admin
        admin = request.user

        # Submit profile form
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=admin
        )

        # ======================================
        # FORM VALID
        # ======================================

        if form.is_valid():

            # Save profile data
            user = form.save(commit=False)

            # Keep these fields controlled by
            # the logged-in admin account
            user.username = admin.username
            user.contact_number = admin.contact_number
            user.role = admin.role

            user.save()

            # Success message
            from django.contrib import messages

            messages.success(
                request,
                "Profile updated successfully."
            )

            # Redirect to same profile page
            return redirect("profile")

        # ======================================
        # FORM INVALID
        # ======================================

        login_history = LoginHistory.objects.filter(
            user=admin
        ).order_by("-login_time")

        context = {
            "form": form,
            "login_history": login_history,
        }

        return render(
            request,
            self.template_name,
            context
        )


class RegisterView(TemplateView):
    template_name = "dashboard/register.html"


class SettingsView(TemplateView):
    template_name = "dashboard/settings.html"


class TablesView(TemplateView):
    template_name = "dashboard/tables.html"


class UserDetailsView(TemplateView):
    template_name = "dashboard/user-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs["user_id"]
        user = User.objects.get(id=user_id)
        context["user"] = user

        # Get user's login history
        login_history = user.login_history.all().order_by(
            "-login_time"
        )

         # Send login history
        context["login_history"] = login_history
        return context


class UsersView(TemplateView):
    template_name = "dashboard/users.html"
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        users = User.objects.exclude(
                role="admin"
        )
        context["total_users"] = users.count()
        context["active_users"] = users.filter(is_active=True).count()
        context["admin_users"] = users.filter(is_superuser=True).count()

        now = timezone.now() 
        context["new_users"] = users.filter(
            date_joined__year=now.year,
            date_joined__month=now.month
        ).count()
        context["users"] = users
        return context


class Create404View(TemplateView):
    template_name = "dashboard/404.html"


class Create500View(TemplateView):
    template_name = "dashboard/500.html"