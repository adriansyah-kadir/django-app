from django.urls import path
from . import handler

app_name = "core"
urlpatterns = [
    path("", handler.index, name="index"),
    path("settings/", handler.SettingView.as_view(), name="settings"),
]
