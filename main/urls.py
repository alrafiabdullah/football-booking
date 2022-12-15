from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('player/register', views.register_player, name='player_register'),
    path('player/login', views.login_player, name='player_login'),
    path('player/logout', views.logout_player, name='player_logout'),
]
