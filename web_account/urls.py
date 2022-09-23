from django.urls import path
from . import handler

app_name = "account"

urlpatterns = [
    path("login/", handler.Login.as_view(), name="login"),
    path("logout/", handler.logout, name="logout"),
    path("register/", handler.Register.as_view(), name="register"),
    path("profile/", handler.Profile.as_view(), name="profile"),
    path("reset/", handler.reset, name="reset"),
    path("settings/", handler.SettingView.as_view(), name="settings"),
    path("<pk>/", handler.Detail.as_view(), name="detail"),
]
