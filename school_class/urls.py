from django.urls import path, include
from . import handler

app_name = "class"
urlpatterns = [
    path("register/", handler.ClassRegister.as_view(), name="register"),
    path("requests/", handler.StudentClassRequest.as_view(), name="requests"),
    path("<id>/requests/", handler.ClassRequests.as_view(), name="class_requests"),
    path("students/<id>/accept/", handler.accept_class, name="accept"),
    path("students/<id>/delete/", handler.delete_class, name="remove_student"),
    path("<id>/students/", handler.ClassMember.as_view(), name="students"),
    # path('<id>/exit/', handler.exit_class, name='exit_class'),
    path("<pk>/", handler.ClassDetail.as_view(), name="detail"),
]
