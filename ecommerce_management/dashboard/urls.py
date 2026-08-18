from django.urls import path
from .views import *

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),

    path("add-user/", AddUserView.as_view(), name="add_user"),
    path("alerts/", AlertsView.as_view(), name="alerts"),
    path("blank/", BlankView.as_view(), name="blank"),
    path("charts/", ChartsView.as_view(), name="charts"),
    path("components/", ComponentsView.as_view(), name="components"),
    path("create-agent/", CreateAgentView.as_view(), name="create_agent"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("forms/", FormsView.as_view(), name="forms"),
   
    path("modals/", ModalsView.as_view(), name="modals"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("register/", RegisterView.as_view(), name="register"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("tables/", TablesView.as_view(), name="tables"),
    path("user-details/", UserDetailsView.as_view(), name="user_details"),
    path("users/", UsersView.as_view(), name="users"),

    path("404/", Create404View.as_view(), name="404"),
    path("500/", Create500View.as_view(), name="500"),
]