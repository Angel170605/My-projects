from django.urls import path

from . import views

app_name = 'players'

urlpatterns = [
    path('<player_id>/', views.player_info, name='player-info'),
    path('<team_id>/<user_id>/sign/', views.sign_player, name='sign-player'),
    path('<player_id>/edit/', views.edit_player, name='edit-player'),
    path('<player_id>/delete', views.delete_player, name='delete-player')
]