from django.urls import path

from . import views


urlpatterns = [

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "register/",
        views.register_student,
        name="register"
    ),

    path(
        "tutor/",
        views.tutor_chat,
        name="tutor"
    ),

    path(
        "quiz/",
        views.quiz,
        name="quiz"
    ),

    path(
        "quiz/review/",
        views.quiz_review,
        name="quiz_review"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),
]