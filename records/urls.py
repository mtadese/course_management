from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("login/", views.student_login, name="login"),
    path("logout/", views.student_logout, name="logout"),
    path("courses/", views.course_list, name="courses"),
    path("students/", views.student_list, name="students"),
    path("results/", views.results_by_course, name="results"),
    path(
        "results/enrollment/<int:enrollment_id>/",
        views.record_result,
        name="record_result",
    ),
]