from django.urls import path
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('player/register', views.register_player, name='player_register'),
    path('player/login', views.login_player, name='player_login'),
    path('player/logout', views.logout_player, name='player_logout'),
    path('player/activate/<uidb64>/<token>',
         views.verify_activation_url, name='player_activate'),

    path('about', views.about, name='about'),
    path('profile', views.player_profile, name='player_profile'),
]
