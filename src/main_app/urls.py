from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="home"),
    path('api', views.start_task, name='start_task'),
    
    path('home', views.home, name="home"),
    path('sign-up', views.sign_up, name='sign_up'),
    path('logout', views.logout_view, name='logout'),
    path('choose-lang', views.choose_langs, name='choose_lang'),
    path('language/<str:language_name>/', views.lang_levels, name='lang_levels'),
    path('language/<str:language_name>/<str:level>', views.lang_tasks, name='lang_tasks'),
    
    
]
