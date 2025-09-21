from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_in, name="login"),
    path('register',views.register , name="register"),
    path('home', views.home, name="home"),
    path('logout',views.logout , name = "logout"),
    path('about_us',views.about_us , name="about_us"),
]