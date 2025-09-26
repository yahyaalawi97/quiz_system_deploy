from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('register',views.register , name="register"),
    path('home', views.home, name="home"),
    path('logout',views.logout , name = "logout"),
    path('about_us',views.about_us , name="about_us"),
    path('create_quiz',views.create_quiz , name="create_quiz"),
    path('edit_quiz/<int:quiz_id>/',views.editquiz , name="edit_quiz"),
    path('delete_quiz/<int:quiz_id>/',views.deletequiz , name="delete_quiz"),
    path('do_quiz/<int:quiz_id>/',views.doquiz , name="do_quiz"),
]