from django.urls import path

from . import views

app_name = 'players'

urlpatterns = [
    path('<team_id>/<user_id>/sign/', views.sign_player, name='sign-player'),
]