from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from users.models import *


# Allow only admin users
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "/account/login/"

    def test_func(self):
        return self.request.user.role == "admin"
    
class DashboardView(TemplateView):
    template_name = "dashboard/index.html"


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


class ProfileView(TemplateView):
    template_name = "dashboard/profile.html"


class RegisterView(TemplateView):
    template_name = "dashboard/register.html"


class SettingsView(TemplateView):
    template_name = "dashboard/settings.html"


class TablesView(TemplateView):
    template_name = "dashboard/tables.html"


class UserDetailsView(TemplateView):
    template_name = "dashboard/user-details.html"


class UsersView(TemplateView):
    template_name = "dashboard/users.html"
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user=User.objects.all()
        context['users']=user
        return context


class Create404View(TemplateView):
    template_name = "dashboard/404.html"


class Create500View(TemplateView):
    template_name = "dashboard/500.html"