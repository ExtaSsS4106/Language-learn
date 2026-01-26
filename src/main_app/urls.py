from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="home"),
    path('home', views.home, name="home"),
    path('sign-up', views.sign_up, name='sign_up'),
    path('logout', views.logout_view, name='logout'),
]
